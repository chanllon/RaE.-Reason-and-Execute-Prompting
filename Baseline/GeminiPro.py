import os

import json
import re

import google.generativeai as genai
import PIL.Image

def gemini_pro_vision(apikey, text, image_path):

    genai.configure(api_key=apikey,transport="rest")
    model = genai.GenerativeModel('gemini-pro-vision')
    img = PIL.Image.open(image_path)
    response = model.generate_content([img,text], stream=False)
    response.resolve()
    with open('GeminiPro_OutPut.txt', 'a', encoding='utf-8') as file:
        file.write('answer:' + str(response.text) + '\n')
    print(response.text)
    print(re.search(r'\d+(\.\d+)?(?=\D*$)', response.text).group(0))
    return re.search(r'\d+(\.\d+)?(?=\D*$)', response.text).group(0)

key=''
flag=0
correct=49
total=459
j=0
for pid in range(1021):
    if j<460:
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
            with open('GeminiPro_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('ID:' + str(total) + '\n' + 'picturePath:' + image_file + '\n')
            res=gemini_pro_vision(key,data['problem_text'],image_file)
            ans=data['choices'][flag]
            if res == ans:
                correct = correct + 1
            with open('GeminiPro_OutPut.txt', 'a', encoding='utf-8') as file:
                file.write('answer:' + res + '\n' + 'correct answer:' + ans + '\n' + "total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total) + '\n' + '------------------------------------------------------------------------------------' + '\n')
            print("total:" + str(total) + "  correct:" + str(correct) + "  acc:" + str(correct / total))
            print(image_file)
    except (AttributeError, UnboundLocalError, ConnectionError,KeyError,ValueError):
        j=j+1