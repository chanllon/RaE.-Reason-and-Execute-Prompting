import json
import os
import re

import torch
from PIL import Image
from transformers import TextStreamer

from mplug_owl2.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from mplug_owl2.conversation import conv_templates, SeparatorStyle
from mplug_owl2.model.builder import load_pretrained_model
from mplug_owl2.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria
os.environ['CUDA_VISIBLE_DEVICES']='2,3'
os.environ['PYTORCH_CUDA_ALLOC_CONF']='expandable_segments:True'

model_path = ''

model_name = get_model_name_from_path(model_path)
tokenizer, model, image_processor, context_len = load_pretrained_model(model_path, None, model_name, load_8bit=False, load_4bit=False, device="cuda")

#conv = conv_templates["mplug_owl2"].copy()
#roles = conv.roles


def mPLUG(query,image_file):
    conv = conv_templates["mplug_owl2"].copy()
    roles = conv.roles
    image = Image.open(image_file).convert('RGB')
    max_edge = max(image.size)  # We recommand you to resize to squared image for BEST performance.
    image = image.resize((max_edge, max_edge))

    image_tensor = process_images([image], image_processor)
    image_tensor = image_tensor.to(model.device, dtype=torch.float16)

    inp = DEFAULT_IMAGE_TOKEN + query
    conv.append_message(conv.roles[0], inp)
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()

    input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(
        model.device)
    stop_str = conv.sep2
    keywords = [stop_str]
    stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    temperature = 0.7
    max_new_tokens = 512

    #with torch.inference_mode():
    output_ids = model.generate(
    input_ids,
    images=image_tensor,
    do_sample=True,
    temperature=temperature,
    max_new_tokens=max_new_tokens,
    streamer=streamer,
    use_cache=True,
    stopping_criteria=[stopping_criteria])

    outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:]).strip()
    # print(outputs)
    with open('mPLUG-0wl2_OutPut.txt', 'a', encoding='utf-8') as file:
        file.write('answer:' + str(outputs) + '\n')
    print(outputs)
    print(re.search(r'\d+(\.\d+)?(?=\D*$)', outputs).group(0))
    return re.search(r'\d+(\.\d+)?(?=\D*$)', outputs).group(0)


allImages=[]
allQuestions=[]
allAnswers=[]
j=0
flag=0
total=608
correct=18
for pid in range(1021):
    if j<608:
       j=j+1
       continue
    try:
        total=total+1
        # whole problem text and annotated logic forms
        with open(os.path.join('', str(pid), 'data.json'), 'r') as f:
            image_file=os.path.join('', str(pid), 'img_diagram.png')
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
            with open('mPLUG-0wl2_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('ID:' + str(total) + '\n' + 'picturePath:' + image_file + '\n')
            res=mPLUG(data['problem_text'],image_file)
            ans=data['choices'][flag]
            if res == ans:
                correct = correct + 1
            with open('mPLUG-0wl2_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('answer:' + res + '\n' + 'correct answer:' + ans + '\n' + "total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total) + '\n' + '------------------------------------------------------------------------------------' + '\n')
            print("total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total))
            print(image_file)
    except (AttributeError):
        j=j+1