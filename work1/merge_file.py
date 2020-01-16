# 当前是按照邮件编号，将td和df存在不同的文件中
# 需要将这些文件进行合并，按照单词字母排序，存入不同的文件中
import json


# 把文件字典写入磁盘
def wf(path, obj):
    desti = open(path, 'w', encoding='utf-8')
    desti.write(json.dumps(obj, sort_keys=True, indent=4))
    desti.close()


load_dict = [{}, {}, {}, {}, {}]


def mergeDF():
    df_path = ['df_a_d.json', 'df_e_j.json', 'df_k_p.json', 'df_q_s.json', 'df_t_z.json']
    for i in range(5):
        with open(df_path[i], 'r', encoding='UTF-8') as f:
            load_dict[i] = json.load(f)
    for i in range(1, 5):
        for k in load_dict[i]:
            if k not in load_dict[0].keys():
                load_dict[0][k] = load_dict[i][k]
            else:
                load_dict[0][k] += load_dict[i][k]
    wf('DF.json', load_dict[0])


TF_beforeD = dict()
TF_EtoJ = dict()
TF_KtoP = dict()
TF_QtoS = dict()
TF_TtoZ = dict()


def mergeTF():
    # TF文件体积较大，考虑按照单词首字母，分块存储，提高查询效率
    tf_path = ['tf_a_d.json', 'tf_e_j.json', 'tf_k_p.json', 'tf_q_s.json', 'tf_t_z.json']
    for i in range(5):
        print(i)
        with open(tf_path[i], 'r', encoding='UTF-8') as f:
            load_dict[i] = json.load(f)
    for i in load_dict:
        for k in i:
            # k是字典i中的关键字，即单词
            if k < "e":
                if k in TF_beforeD.keys():
                    # 追加文章id及tf
                    TF_beforeD[k].extend(i[k])
                else:
                    # 新增单词
                    print(k)
                    TF_beforeD[k] = i[k]
            elif k < "k":
                if k in TF_EtoJ.keys():
                    TF_EtoJ[k].extend(i[k])
                else:
                    print(k)
                    TF_EtoJ[k] = i[k]
            elif k < "q":
                if k in TF_KtoP.keys():
                    TF_KtoP[k].extend(i[k])
                else:
                    print(k)
                    TF_KtoP[k] = i[k]
            elif k < "t":
                if k in TF_QtoS.keys():
                    TF_QtoS[k].extend(i[k])
                else:
                    print(k)
                    TF_QtoS[k] = i[k]
            else:
                if k in TF_TtoZ.keys():
                    TF_TtoZ[k].extend(i[k])
                else:
                    print(k)
                    TF_TtoZ[k] = i[k]
    wf("TF_beforeD.json", TF_beforeD)
    wf("TF_EtoJ.json", TF_EtoJ)
    wf("TF_KtoP.json", TF_KtoP)
    wf("TF_QtoS.json", TF_QtoS)
    wf("TF_TtoZ.json", TF_TtoZ)


ID_dict = {}


def mergeID():
    id_path = ['id_a_d.json', 'id_e_j.json', 'id_k_p.json', 'id_q_s.json', 'id_t_z.json']
    for i in range(5):
        with open(id_path[i], 'r', encoding='UTF-8') as f:
            load_dict[i] = json.load(f)
        for k in load_dict[i]:
            ID_dict[load_dict[i][k]] = k
    wf("ID.json", ID_dict)


try:
    # mergeID()
    mergeTF()
    # mergeDF()
except:
    print("Writing File Failed.")
