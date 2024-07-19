# coding=gbk
import json
import os
import re
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, LlamaTokenizer
from accelerate import init_empty_weights, infer_auto_device_map, load_checkpoint_and_dispatch
print(torch.cuda.device_count())
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:100'
os.environ['PYTORCH_CUDA_ALLOC_CONF']='expandable_segments:True'


tokenizer = LlamaTokenizer.from_pretrained('lmsys/vicuna-7b-v1.5')

with init_empty_weights():
    model = AutoModelForCausalLM.from_pretrained(
        'THUDM/cogvlm-chat-hf',
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
device_map = infer_auto_device_map(model, max_memory={1:'20GiB',3:'20GiB','cpu':'16GiB'}, no_split_module_classes=['CogVLMDecoderLayer', 'TransformerLayer'])
model = load_checkpoint_and_dispatch(
    model,
    'THUDM/cogvlm-chat-hf',   # typical, '~/.cache/huggingface/hub/models--THUDM--cogvlm-chat-hf/snapshots/balabala'
    device_map=device_map,
)
model = model.eval()

# # check device for weights if u want to
# for n, p in model.named_parameters():
#     print(f"{n}: {p.device}")


def cogvlm(query,image):
    # chat example

    image = Image.open(image).convert('RGB')
    inputs = model.build_conversation_input_ids(tokenizer, query=query, history=[], images=[image])  # chat mode
    inputs = {
        'input_ids': inputs['input_ids'].unsqueeze(0).to('cuda'),
        'token_type_ids': inputs['token_type_ids'].unsqueeze(0).to('cuda'),
        'attention_mask': inputs['attention_mask'].unsqueeze(0).to('cuda'),
        'images': [[inputs['images'][0].to('cuda').to(torch.bfloat16)]],
    }
    gen_kwargs = {"max_length": 2048, "do_sample": False}

    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        print(tokenizer.decode(outputs[0]))
    with open('CogVLM_OutPut.txt', 'a', encoding='utf-8') as file:
        file.write('answer:' + str(tokenizer.decode(outputs[0])) + '\n')
    print(tokenizer.decode(outputs[0]))
    print(re.search(r'\d+(\.\d+)?(?=\D*$)', tokenizer.decode(outputs[0])).group(0))
    return re.search(r'\d+(\.\d+)?(?=\D*$)', tokenizer.decode(outputs[0])).group(0)


allImages=[]
allQuestions=[]
allAnswers=[]
j=0
flag=0
total=0
correct=0
for pid in range(1021):
    try:
        total=total+1
        # whole problem text and annotated logic forms
        with open(os.path.join('train', str(pid), 'data.json'), 'r') as f:
            image_file=os.path.join('train', str(pid), 'img_diagram.png')
            data = json.load(f)
            # print(image_file)
            # print(data['problem_text'])
            if data['answer'] == 'A':
                flag = 0
            elif data['answer'] == "B":
                flag = 1
            elif data['answer'] == "C":
                flag = 2
            elif data['answer'] == "D":
                flag = 3
            with open('CogVLM_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('ID:' + str(total) + '\n' + 'picturePath:' + image_file + '\n')
            res=cogvlm(data['problem_text'],image_file)
            ans=data['choices'][flag]
            if res == ans:
                correct = correct + 1
            with open('CogVLM_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('answer:' + res + '\n' + 'correct answer:' + ans + '\n' + "total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total) + '\n' + '------------------------------------------------------------------------------------' + '\n')
            print("total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total))
            print(image_file)
    except (AttributeError):
        j=j+1