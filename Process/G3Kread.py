import os
from Process.isnumeric import is_numeric
import json
from collections import Counter
from googletrans import Translator
translator = Translator()
# 指定目录路径（请根据您实际的路径进行修改）
import random

def read_files_in_folder(folder_path,Trans):
    dataset = []

    for root, dirs, files in os.walk(folder_path):
        image_path = ''
        id=''
        question_text=''
        correctans=''
        word_count=''
        shape=''
        shapenum=''

        for file_name in files:
            if file_name=='data.json':
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    data = json.loads(file.read())
                    id=data["id"]
                    choice=data["choices"]
                    answer=data["answer"]
                    if answer=="A":
                       correctans= is_numeric(choice[0])
                    if answer=="B":
                       correctans= is_numeric(choice[1])
                    if answer=="C":
                       correctans= is_numeric(choice[2])
                    if answer=="D":
                       correctans= is_numeric(choice[3])
                    question_text=data["problem_text"]
                    shape=data["problem_type_graph"]
                    shapenum=len(shape)
                    word_count = len(question_text.split())
                    if Trans:
                        question_text = translator.translate(question_text, src='en', dest='zh-cn').text
                        print(question_text)
                        word_count = len(question_text)
            elif file_name=='img_diagram.png':
                image_path = os.path.join(root, file_name)
            else:
                continue
        if correctans:
            ddata = {'id': id, 'question': question_text, 'imge_path': str(image_path), 'correctans': correctans,
                     'length': word_count, 'shape': shape, 'shapenum': shapenum}
            dataset.append(ddata)
        else:
            continue
    # print(dataset)
    # for data in random.sample(dataset, 10):
    #     print(data)
    return dataset

# # 读取指定文件夹下的数据
# folder_path = 'D:\Pythonfile\MGeo-MLLMs\Data\Geometry3K'
# read_files_in_folder(folder_path,Trans=False)

# 输出随机选择的1000条数据

