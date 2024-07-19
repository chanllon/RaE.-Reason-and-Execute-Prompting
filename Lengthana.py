import json
import os
from Process.isnumeric import is_numeric

# 存储所有列表的列表
all_lists = []

# 遍历文件夹中的所有.json文件
folder_path = ''

# 初始化一个空列表，用于存储所有的json数据
json_data = []

# 遍历文件夹中的所有文件
for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
            # 将json数据添加到列表中
                    json_data.extend(data)
# with open(folder_path, 'r') as file:
#         data = json.load(file)


# 按形状分类
shape_data = {}
for entry in json_data:
    shapes = entry["length"]
    if shapes not in shape_data:
        shape_data[shapes] = {"total": 0, "correct": 0}
    shape_data[shapes]["total"] += 1
    if is_numeric(entry["correctans"]) == is_numeric(entry["answer"]):
        shape_data[shapes]["correct"] += 1

# 计算准确率
accuracy_data = {}
for shape, stats in shape_data.items():
    if stats["total"] > 0:
        accuracy = stats["correct"] / stats["total"]
    else:
        accuracy = 0
    accuracy_data[shape] = accuracy

print(len(accuracy_data))
# 打印结果
for shape, accuracy in sorted(accuracy_data.items(), reverse=False):
    # print(shape)
    # print('长度：',shape,'准确：',accuracy)
    print(accuracy)
