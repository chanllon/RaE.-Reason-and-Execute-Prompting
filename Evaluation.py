# -*- coding:utf-8 -*-
import os
import json
from Process import GEOSread,G3Kread,GeoQAread,GeoQa_read
from Process.isnumeric import is_numeric
import random
from Prompting.RaE import GPT4RaE,QwenplusRaE,GeminRaE
from Prompting.PAL import GPT4PAL,QwenplusPAL,GeminPAL
from Prompting.CoT import GPT4CoT,QwenplusCoT,GeminCoT
from Prompting.Ori import GPT4,Qwenplus,Gemin
from Process.Samplenumber import Sampel

# # 自定义转换函数
# def convert_to_json_serializable(obj):
#     if isinstance(obj, float):
#         return str(obj)  # 将 float 转换为字符串
#     else:
#         raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def save_dict_to_json(dict_data, json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump(dict_data, json_file)


def evaluation(model,datass, Prompt,Tran,Num,Sam):
    folder_path = os.path.join("D:\Pythonfile\MGeo-MLLMs\Data",datass)
    dataset=''
    if datass=='GEOS':
        dataset=GEOSread.read_files_in_folder(folder_path,Tran)
    elif datass=='Geometry3K':
        dataset=G3Kread.read_files_in_folder(folder_path,Tran)
    elif datass=='GeoQa+':
        dataset=GeoQa_read.read_files_in_folder(folder_path,Tran)
    elif datass=='GeoQAA+':
        dataset=GeoQAread.read_files_in_folder(folder_path,Tran)
    else:
        print('')
    j=0
    total=0
    correct=0
    mistake=0
    error=0
    iscorrect=0
    results=[ ]
    if Sam:
        dataa=Sampel(dataset)
        # print(dataa)
    else:
        dataa=random.sample(dataset, Num)

    for data in dataa:
        try:
            total = total + 1
            question=data['question']
            ans = data['correctans']
            if model=='GPT4':
                if Prompt=='RaE':
                    res = GPT4RaE(data['imge_path'], question)
                elif Prompt=='PAL':
                    res = GPT4PAL(data['imge_path'], question)
                elif Prompt=='CoT':
                    res = GPT4CoT(data['imge_path'], question)
                else:
                    res = GPT4(data['imge_path'], question)
            elif model=='Qwenplus':
                if Prompt == 'RaE':
                    res = QwenplusRaE(data['imge_path'], question)
                elif Prompt == 'PAL':
                    res = QwenplusPAL(data['imge_path'], question)
                elif Prompt == 'CoT':
                    res = QwenplusCoT(data['imge_path'], question)
                else:
                    res = Qwenplus(data['imge_path'], question)
            elif model=='Gemin':
                if Prompt == 'RaE':
                    res = GeminRaE(data['imge_path'], question)
                elif Prompt == 'PAL':
                    res = GeminPAL(data['imge_path'], question)
                elif Prompt=='CoT':
                    res = GeminCoT(data['imge_path'], question)
                else:
                    res = Gemin(data['imge_path'], question)
            else:
                print('')
            if is_numeric(res) and ans:
                if float(res) == float(ans):
                    correct += 1
                    iscorrect=1
                    print(correct)
                else:
                    mistake += 1

            else:
                error += 1
            result={ "total": total, "answer": str(res),"iscorrect": iscorrect, "correct": correct, "mistake":mistake, "error":
                    error, "acc ":float(correct / total),"mis":float(mistake / total),"err":float(error / total)}
            datas=data.copy()
            datas.update(result)

            results.append(datas)
            print("total:" + str(total) + "  correct:" + str(correct) + "  mistake:" + str(
                mistake) + "  error:" + str(error) + "  acc:" + str(correct / total))
            # savefile=os.path.join('D:\Pythonfile\MGeo-MLLMs\Temp',model+datass+Prompt+'.json')
            # # with open(savefile, 'a') as json_file:
            # #     json.dump(results, json_file)
        except (AttributeError, UnboundLocalError, ConnectionError,KeyError,ValueError):
            j=j+1
    print('',results)
    return results