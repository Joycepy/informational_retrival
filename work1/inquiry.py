# 读取用户的查询要求，构建向量计算余弦相似度，并返回查询结果
from nltk.stem import PorterStemmer
import json
import math
import numpy as np
from tkinter import *
import tkinter as tk  # 使用Tkinter前需要先导入

N = 517401


def search_id(strs, locs, file_num):
    with open("DF.json", 'r', encoding='UTF-8') as f:
        df = json.load(f)
    f.close()
    # 记录已被加载进来的索引
    f_set = set()
    index = {}
    # 提取单词词干
    words = []
    count = len(strs)
    # 计算查询单词的tf
    quiry_tf = {}
    for i in range(count):
        tmp = PorterStemmer().stem(strs[i]) + locs[i]
        words.append(tmp)
        if tmp not in quiry_tf:
            quiry_tf[tmp] = 1
        else:
            quiry_tf[tmp] += 1
    # 查询去重
    word_set = set(words)
    for word in word_set:
        # 选择文件夹
        if word < "e":
            f_set.add("TF_beforeD.json")
        elif word < "k":
            f_set.add("TF_EtoJ.json")
        elif word < "q":
            f_set.add("TF_KtoP.json")
        elif word < "t":
            f_set.add("TF_QtoS.json")
        else:
            f_set.add("TF_TtoZ.json")
    for i in f_set:
        with open(i, 'r', encoding='UTF-8') as f:
            index.update(json.load(f))

    # 构建文章向量，放在一个词典里，key是文章id，value是向量
    vec_f = {}
    not_found = []
    i = 0
    for name in word_set:
        if name in index:
            for tuple in index[name]:
                if tuple[0] not in vec_f:
                    # 如果文章id（tuple[0]）已存在，那么直接改当前单词tf的值
                    # 对于新出现的每一篇文章
                    # 需要给他先初始化一个长度为集合大小的全0数组
                    vec_f[tuple[0]] = np.ones(len(word_set)) * 0
                    # vec_f[tuple[0]][i]是在id为tuple[0]的文章向量中，单词name的位置
                vec_f[tuple[0]][i] = tuple[1]
            i += 1
        else:
            # 若这个单词不在邮件中，那么所有文章的评分都不会受到它的影响，可以去掉这一个单词
            not_found.append(name)

    # 计算查询向量
    vec_q = []
    for word in word_set:
        if word not in not_found:
            # 出现在tf字典里的单词，一定也会出现在df字典里
            vec_q.append((1 + math.log(quiry_tf[word], 10)) * (math.log(N / df[word], 10)))

    # 算分，key为文章id，value是得分
    score = {}
    for i in vec_f:
        score[i] = (np.array(vec_f[i])) @ (np.array(vec_q))
    # 排序，返回的结果是列表，元素为元组（fileID，score），得分由高到低
    # score.items()未出处理时是一个array，所以会报错，需要在前面改变向量乘法
    score_list = sorted(score.items(), key=lambda x: x[1], reverse=True)
    res = []
    if file_num > len(score_list):
        # 如果用户给出的数字超过id总数的话，展示全部.
        # 注意把整形转为字符串，因为ID字典中的key是字符串
        file_num = 0
    if file_num == 0:
        for i in score_list:
            res.append(str(i[0]))
    else:
        for i in range(file_num):
            res.append(str(score_list[i][0]))
    return res


def find_path(file_id):
    with open("ID.json", 'r', encoding='UTF-8') as f:
        # id字典中key是文章编号,注意这里是字符串，value是路径
        id = json.load(f)
    f.close()
    paths = []
    if len(file_id) == 0:
        paths.append("未找到相关内容！")
    else:
        for i in file_id:
            paths.append(id[i])
    return paths


if __name__ == '__main__':
    # 实例化object，建立窗口window
    window = tk.Tk()
    # 给窗口的可视化起名字
    window.title('邮件检索系统')
    # 设定窗口的大小(长 * 宽)
    window.geometry('500x500')

    # 加载image
    canvas = tk.Canvas(window, width=400, height=73)
    image_file = tk.PhotoImage(file='img.png')
    image = canvas.create_image(220, 0, anchor='n', image=image_file)
    canvas.pack(side='top')
    tk.Label(window, text='每项查询若有多个单词，请用空格分开', font=('Arial', 8)).pack()

    # 输入信息
    tk.Label(window, text='From:', font=('Arial', 14)).place(x=10, y=95)
    tk.Label(window, text='To:', font=('Arial', 14)).place(x=10, y=135)
    tk.Label(window, text='Subject:', font=('Arial', 14)).place(x=10, y=175)
    tk.Label(window, text='Content:', font=('Arial', 14)).place(x=10, y=215)
    tk.Label(window, text='Number:', font=('Arial', 14)).place(x=10, y=255)
    tk.Label(window, text='Result:', font=('Arial', 14)).place(x=10, y=345)

    var_from = tk.StringVar()
    entry_from = tk.Entry(window, textvariable=var_from, font=('Arial', 14))
    entry_from.place(width=300, x=120, y=100)

    var_to = tk.StringVar()
    entry_to = tk.Entry(window, textvariable=var_to, font=('Arial', 14))
    entry_to.place(width=300, x=120, y=140)

    var_sub = tk.StringVar()
    entry_sub = tk.Entry(window, textvariable=var_sub, font=('Arial', 14))
    entry_sub.place(width=300, x=120, y=180)

    var_con = tk.StringVar()
    entry_con = tk.Entry(window, textvariable=var_con, font=('Arial', 14))
    entry_con.place(width=300, x=120, y=220)

    var_num = tk.StringVar()
    var_num.set("0")
    entry_con = tk.Entry(window, textvariable=var_num, font=('Arial', 14))
    entry_con.place(width=300, x=120, y=260)

    tk.Label(window, text='Number为显示邮件数，输入0则展示全部', font=('Arial', 8)).place(x=120, y=285)

    t = tk.Text(window, height=7)
    scroll = Scrollbar()
    scroll.place(x=405, y=380)
    scroll.config(command=t.yview)
    t.config(yscrollcommand=scroll.set)
    t.place(width=300, x=120, y=340)


    # 定义一个函数功能供点击Button按键时调用，调用命令参数command=函数名
    def hit_btn():
        # 获取用户输入的信息
        e_from = var_from.get()
        e_to = var_to.get()
        e_sub = var_sub.get()
        e_con = var_con.get()
        e_num = var_num.get()

        # 0——From，1——To，2——Subject，3——Content
        q = []
        q.append(e_from)
        q.append(e_to)
        q.append(e_sub)
        q.append(e_con)

        file_num = int(e_num)

        locs = []
        strs = []
        for i in range(4):
            words = q[i].split()
            for word in words:
                strs.append(word)
                locs.append(str(i))

        file_id = search_id(strs, locs, file_num)
        paths = find_path(file_id)
        for i in paths:
            t.insert(INSERT, i + "\n")

        # 在窗口界面设置放置Button按键


    btn_search = tk.Button(window, text='Search', font=('Arial', 12), width=10, height=1, command=hit_btn)
    btn_search.place(x=200, y=305)

    # 主窗口循环显示，让window不断的刷新
    window.mainloop()
