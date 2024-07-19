import random

def Sampel(data):
    # 按形状分类
    shape_data = {}
    for entry in data:
        shapes = entry["shape"]
        shapesnum=entry['shapenum']
        if shapesnum==1:
            for shape in shapes:
                if shape not in shape_data:
                    shape_data[shape] = []
                shape_data[shape].append(entry)

    # 计算每个形状的数量
    shape_counts = {shape: len(entries) for shape, entries in shape_data.items()}
    min_shape=min(shape_counts.values())
    print('', shape_counts)
    # average_count = sum(shape_counts.values()) // len(shape_counts)

    # 抽取样本
    sampled_data = []
    for shape, entries in shape_data.items():
        sample_size = min(min_shape,10)
        sampled_entries = random.sample(entries, sample_size)
        sampled_data.extend(sampled_entries)
    return sampled_data
