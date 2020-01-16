# 现在索引按照文件夹分别存在不同而文件里，需要对词频进行对数和归一化处理
# 归一化即除以向量长度
# 最后将处理过的数据存入一个文件中作为最终的索引
import json
import math


# 把文件字典写入磁盘
def wf(path, obj):
    desti = open(path, 'w', encoding='utf-8')
    desti.write(json.dumps(obj, sort_keys=True, indent=4))
    desti.close()


def normalize(from_path, to_path):
    # 读入要处理的词频文件
    with open(from_path, 'r', encoding='UTF-8') as f:
        load_dict = json.load(f)
    # 改变权重——做对数处理
    for k in load_dict:
        for v in load_dict[k]:
            v[1] = 1 + math.log(v[1], 10)

    # 计算向量长度，文档-长度平方 词典
    doc_len = dict()
    for k in load_dict:
        for v in load_dict[k]:
            if v[0] in doc_len.keys():
                doc_len[v[0]] += v[1] * v[1]
            else:
                doc_len[v[0]] = v[1] * v[1]
    # 归一化
    for k in load_dict:
        print(k)
        for j in load_dict[k]:  # j[0]为文章id，j[1]为词频
            # 位数过多会增大文件体积
            j[1] = round(j[1] / math.sqrt(doc_len[j[0]]), 4)
            print(j)

    wf(to_path, load_dict)
    return load_dict


try:
    # normalize('dict_a_d.json', 'tf_a_d.json')
    normalize('dict_e_j.json', 'tf_e_j.json')
    normalize('dict_k_p.json', 'tf_k_p.json')
    normalize('dict_q_s.json', 'tf_q_s.json')
    normalize('dict_t_z.json', 'tf_t_z.json')
except:
    print("Writing Files Failed")
