import json
import os
import re
os.environ['CUDA_VISIBLE_DEVICES']='2,3'
os.environ['PYTORCH_CUDA_ALLOC_CONF']='expandable_segments:True'
import torch
from transformers import AutoModel, AutoTokenizer

#PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
torch.set_grad_enabled(False)
print(torch.cuda.is_available())
# init model and tokenizer
model = AutoModel.from_pretrained('/InternLM-XComposer/Shanghai_AI_Laboratory/internlm-xcomposer-7b', trust_remote_code=True).cuda().eval()
tokenizer = AutoTokenizer.from_pretrained('/InternLM-XComposer/Shanghai_AI_Laboratory/internlm-xcomposer-7b', trust_remote_code=True)
model.tokenizer = tokenizer
def InternLM_XComposer(img, question):

    response = model.generate(question,img)
    with open('Intern-XComposer_OutPut.txt', 'a', encoding='utf-8') as file:
        file.write('answer:' + str(response) + '\n')
    print(response)
    print(re.search(r'\d+(\.\d+)?(?=\D*$)', response).group(0))
    return re.search(r'\d+(\.\d+)?(?=\D*$)', response).group(0)

flag=0
correct=0
total=0
j=0
for pid in range(1021):
    # if j<460:
    #     j=j+1
    #     continue
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
            with open('Intern-XComposer_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('ID:' + str(total) + '\n' + 'picturePath:' + image_file + '\n')
            res=InternLM_XComposer(image_file,data['problem_text'])
            ans=data['choices'][flag]
            if res == ans:
                correct = correct + 1
            with open('Intern-XComposer_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('answer:' + res + '\n' + 'correct answer:' + ans + '\n' + "total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total) + '\n' + '------------------------------------------------------------------------------------' + '\n')
            print("total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total))
            print(image_file)
    except (AttributeError, UnboundLocalError, ConnectionError,KeyError,ValueError):
        j=j+1