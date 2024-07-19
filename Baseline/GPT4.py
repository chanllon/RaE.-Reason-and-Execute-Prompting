import base64
import os

import json
import re

import openai
import requests

# 设置您的API密钥
openai.api_key = ''
# file='image/1.png'
# encoded_image = base64.b64encode(open(file, 'rb').read()).decode('ascii')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
}

def gpt_4_vision(image_path,text):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 3000
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    res = response.json()
    # print(res['choices'][0]['message']['content'])  # 打印生成的文本响应
    with open('gpt_4OutPut.txt', 'a', encoding='utf-8') as file:
        file.write('answer:' + str(res['choices'][0]['message']['content']) + '\n')
    print(res['choices'][0]['message']['content'])
    print(re.search(r'\d+(\.\d+)?(?=\D*$)', res['choices'][0]['message']['content']).group(0))
    return re.search(r'\d+(\.\d+)?(?=\D*$)', res['choices'][0]['message']['content']).group(0)

# key='AIzaSyCdfI5BPIj1gps8pNK8XzE_JV2cQAWz964'
# text='如图,直线a⊥直线c,直线b⊥直线c,若∠1=70°,则∠2=()'
# image='image/4.png'
# gemini_pro_vision(key,text,image)
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
            with open('gpt_4OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('ID:' + str(total) + '\n' + 'picturePath:' + image_file + '\n')
            res=gpt_4_vision(image_file,data['problem_text'])
            ans=data['choices'][flag]
            if res == ans:
                correct = correct + 1
            with open('gpt_4OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('answer:' + res + '\n' + 'correct answer:' + ans + '\n' + "total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total) + '\n' + '------------------------------------------------------------------------------------' + '\n')
            print("total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total))
            print(image_file)
    except (AttributeError, UnboundLocalError, ConnectionError,KeyError,ValueError):
        j=j+1