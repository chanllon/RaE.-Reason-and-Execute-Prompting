import json
from Process.isnumeric import is_numeric


file_path = 'Geometry3K20-14-43.json'
with open(file_path, 'r') as file:
    data = json.load(file)



# 按形状分类
shape_data = {}
for entry in data:
    shapes = entry["shape"]
    for shape in shapes:
        if shape not in shape_data:
            shape_data[shape] = {"total":0,"correct":0}
        shape_data[shape]["total"] += 1
        print(entry["correctans"])
        print((entry["answer"]))
        print('-------------')
        if is_numeric(entry["correctans"]) == is_numeric(entry["answer"]):
            shape_data[shape]["correct"] += 1
print(shape_data)
# 计算准确率
accuracy_data = {}
for shape, stats in shape_data.items():
    if stats["total"] > 0:
        accuracy = stats["correct"] / stats["total"]
    else:
        accuracy = 0
    accuracy_data[shape] = accuracy

# 打印结果
for shape, accuracy in accuracy_data.items():
    print(f"Shape: {shape}, Accuracy: {accuracy}")
