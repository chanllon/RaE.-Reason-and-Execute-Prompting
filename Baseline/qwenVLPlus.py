import base64
import os
import re
import time
import json
import random
from http import HTTPStatus
import dashscope
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
dashscope.api_key=''
def simple_multimodal_conversation_call(img, question):
    messages = [
        # {
        #     'role': 'system',
        #     'content': [{
        #         'text': 'You are a helpful assistant.'
        #     }]
        # },
        {
            "role": "user",
            "content": [
                # {"text":"Solve the problem step by step (do not over-divide the steps)"},
                # {"text":"Take out any queries that can be asked through Python (for example, any calculations or equations that can be calculated)"},
                {"image": 'file://'+img},
                {"text": question},
                # {"text": "After all the queries are run and you get the answer, put the answer in \\boxed{}"}
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
                                                     messages=messages)
    with open('qwenVLPlus_OutPut.txt', 'a', encoding='utf-8') as file:
        file.write('answer:' + str(response.output.choices[0].message.content[0]['text']) + '\n')
    print(response.output.choices[0].message.content[0]['text'])
    print(re.search(r'\d+(\.\d+)?(?=\D*$)', response.output.choices[0].message.content[0]['text']).group(0))
    return re.search(r'\d+(\.\d+)?(?=\D*$)', response.output.choices[0].message.content[0]['text']).group(0)
#key='AIzaSyCdfI5BPIj1gps8pNK8XzE_JV2cQAWz964'
flag=0
correct=70
total=788
j=0
for pid in range(1021):
    if j<789:
        j=j+1
        continue
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
            with open('qwenVLPlus_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('ID:' + str(total) + '\n' + 'picturePath:' + image_file + '\n')
            res=simple_multimodal_conversation_call(image_file,data['problem_text'])
            ans=data['choices'][flag]
            if res == ans:
                correct = correct + 1
            with open('qwenVLPlus_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('answer:' + res + '\n' + 'correct answer:' + ans + '\n' + "total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total) + '\n' + '------------------------------------------------------------------------------------' + '\n')
            print("total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total))
            print(image_file)
    except (AttributeError):
        j=j+1