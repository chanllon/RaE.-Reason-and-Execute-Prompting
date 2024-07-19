import base64
import os
import re
import time
from transformers import BitsAndBytesConfig
import torch
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM
# from modelscope import (
#     snapshot_download, AutoModelForCausalLM, AutoTokenizer, GenerationConfig
# )
import json
import random
from http import HTTPStatus
import dashscope
from dashscope import Generation, MultiModalConversation
from dashscope.api_entities.dashscope_response import Role
# dashscope.api_key='sk-a096dc567929434d98f8941bf59fc868'

revision = 'v1.0.0'

# model_dir = snapshot_download('D:\qwen\Qwen-VL-Chat')
# torch.manual_seed(1234)

tokenizer = AutoTokenizer.from_pretrained('Qwen-VL-Chat', trust_remote_code=True)
# if not hasattr(tokenizer, 'model_dir'):
#     tokenizer.model_dir = model_dir
model = AutoModelForCausalLM.from_pretrained("Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()

def simple_multimodal_conversation_call(img, question):
    query = tokenizer.from_list_format([
        {'image': img},
        # Either a local path or an url
        {'text': question},
    ])
    response, history = model.chat(tokenizer, query=query, history=None)
    print(response)
    with open('qwenVLChat_OutPut.txt', 'a', encoding='utf-8') as file:
        file.write('answer:' + str(response) + '\n')
    print(response)
    print(re.search(r'\d+(\.\d+)?(?=\D*$)', response).group(0))
    return re.search(r'\d+(\.\d+)?(?=\D*$)', response).group(0)
# key='AIzaSyCdfI5BPIj1gps8pNK8XzE_JV2cQAWz964'
flag=0
correct=0
total=0
j=0
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
            with open('qwenVLChat_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('ID:' + str(total) + '\n' + 'picturePath:' + image_file + '\n')
            res=simple_multimodal_conversation_call(image_file,data['problem_text'])
            ans=data['choices'][flag]
            if res == ans:
                correct = correct + 1
            with open('qwenVLChat_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('answer:' + res + '\n' + 'correct answer:' + ans + '\n' + "total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total) + '\n' + '------------------------------------------------------------------------------------' + '\n')
            print("total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total))
            print(image_file)
    except (AttributeError):
        j=j+1