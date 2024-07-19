import random

def Sampel(data):
    # 按形状分类
    shape_data = {}
    for entry in data:
        shapesnum=entry['knownum']
        if shapesnum!=5:
            if shapesnum not in shape_data:
                shape_data[shapesnum] = []
            shape_data[shapesnum].append(entry)
        else:
            continue

    # 计算每个形状的数量
    shape_counts = {shape: len(entries) for shape, entries in shape_data.items()}
    min_shape=min(shape_counts.values())
    print('', shape_counts)
    # average_count = sum(shape_counts.values()) // len(shape_counts)

    # 抽取样本
    sampled_data = []
    for shape, entries in shape_data.items():
        sample_size = 1
        sampled_entries = random.sample(entries, sample_size)
        sampled_data.extend(sampled_entries)
    return sampled_data
