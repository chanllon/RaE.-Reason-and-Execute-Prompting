import os
import ast
import json
from collections import Counter
import re
from Process.isnumeric import is_numeric
from googletrans import Translator
translator = Translator()

def find_keyword(sentence, keywords):

    regex = r"\b(?:" + "|".join(keywords) + r")\b"

    match = re.search(regex, sentence, flags=re.IGNORECASE)
    if match:
        return match.group()
    else:
        return None

def Shapee(sentence):
    import re

    # sentence = "In circle O, diameter Rhombus AB is Line perpendicular to chord CD at E."
    keywords = ['Triangle', 'circle', 'line', 'Rhombus', 'Parallelogram', 'Rectangle', 'Trapezoid', 'Square']


    matches = re.findall(r'\b\w+\b', sentence)


    matches_lower = [word.lower() for word in matches]
    keywords_lower = [keyword.lower() for keyword in keywords]


    found_keywords = [word for word in matches_lower if word in keywords_lower]

    if found_keywords:
        return  list(set(found_keywords))
    else:
        return ['other']




def read_files_in_folder(folder_path,Trans):
    dataset = []
    # shape=['Triangle','Circle','Line','mixup','Rhombus','Parallelogram','Rectangle','Trapezoid','Square' ]
    for root, dirs, files in os.walk(folder_path):
        image_path = ''
        id = ''
        question_text = ''
        correctans = ''
        word_count = ''
        shape = [ ]
        shapenum = ''
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.loads(file.read())
                    id = os.path.splitext(os.path.basename(file_path))[0]
                    question_text = data["text"]
                    shape = Shapee(question_text)
                    shapenum = len(shape)
                    word_count = len(question_text.split())
                    if Trans:
                        question_text = translator.translate(question_text, src='en', dest='zh-cn').text
                        word_count=len(question_text)
                    option=data["answer"]
                    if len(data["choices"])==0:
                        correctans = is_numeric(option)
                    else:
                        correctans = is_numeric(data["choices"][option])
            if file_name.endswith('.png'):
                image_path=os.path.join(root, file_name)
                if correctans:
                    ddata = {'id': id, 'question': question_text, 'imge_path': str(image_path), 'correctans': correctans,
                             'length': word_count, 'shape': shape, 'shapenum': shapenum}
                    dataset.append(ddata)
                else:
                    continue
    # print(dataset)
    return dataset
    # print(len(dataset))


# folder_path = 'D:\Pythonfile\MGeo-MLLMs\Data\GEOS'
# read_files_in_folder(folder_path,Trans=True)
