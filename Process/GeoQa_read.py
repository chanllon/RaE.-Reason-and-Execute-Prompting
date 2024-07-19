import os
import ast
import json
from collections import Counter
import re
from Process.isnumeric import is_numeric
from googletrans import Translator
translator = Translator()
# 指定目录路径（请根据您实际的路径进行修改）

def read_files_in_folder(folder_path,Trans):
    dataset = []
    # shape=['Triangle','Circle','Line','mixup','Rhombus','Parallelogram','Rectangle','Trapezoid','Square' ]
    for root, dirs, files in os.walk(folder_path):
        image_path = ''
        id = ''
        question_text = ''
        correctans = ''
        word_count = ''
        know = [ ]
        knownum = ''
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.loads(file.read())
                    id = data["id"]
                    question_text = data["subject"]
                    know=data["formal_point"]
                    knownum=len(know)
                    word_count = len(question_text)
                    if Trans:
                        question_text = translator.translate(question_text, src='zh-cn', dest='en').text
                        print(question_text)
                        word_count = len(question_text)
                    correctans = is_numeric(data["choices"][data["lable"]-1])
            if file_name.endswith('.png'):
                image_path=os.path.join(root, file_name)
                if correctans:
                    ddata = {'id': id, 'question': question_text, 'imge_path': str(image_path), 'correctans': correctans,
                             'length': word_count, 'know': know, 'knownum': knownum}
                    dataset.append(ddata)
                else:
                    continue
    # print(dataset)
    return dataset
    # print(len(dataset))

# 读取指定文件夹下的数据
# folder_path = 'D:\Pythonfile\MGeo-MLLMs\Data\GeoQa+'
# read_files_in_folder(folder_path,Trans=True)
