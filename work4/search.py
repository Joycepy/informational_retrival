import json
import os
import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter import *

import jieba
import numpy as np
from playsound import playsound

from feature_extractors import tfidf_extractor

namelist = []
tmp = 0


def wf(path, obj):
    file = open(path, 'w', encoding='utf-8')
    file.write(json.dumps(obj, sort_keys=True, indent=4))
    file.close()


def read_corpus(file):
    with open(file, 'r', encoding='utf8', errors='ignore') as f:
        list = []
        lines = f.readlines()
        for i in lines:
            list.append(i)
    return list


questions = read_corpus('./Ques.txt')
answers = read_corpus('./Ans.txt')


def filter_out_category(input):
    new_input = re.sub('[\u4e00-\u9fa5]{2,5}\\/', '', input)
    return new_input


def filter_out_punctuation(input):
    new_input = re.sub('([a-zA-Z0-9])', '', input)
    new_input = ''.join(e for e in new_input if e.isalnum())
    return new_input


def word_segmentation(input):
    new_input = ','.join(jieba.cut(input))
    return new_input


def preprocess_text(data):
    new_data = []
    for q in data:
        q = filter_out_category(q)
        q = filter_out_punctuation(q)
        q = word_segmentation(q)
        new_data.append(q)
    return new_data


qlist = preprocess_text(questions)  # 更新后的


def conver2tfidf(data):
    new_data = []
    for q in data:
        new_data.append(q)
    tfidf_vectorizer, tfidf_X = tfidf_extractor(new_data)
    return tfidf_vectorizer, tfidf_X


tfidf_vectorizer, tfidf_X = conver2tfidf(qlist)


def idx_for_largest_cosine_sim(input, questions):
    list = []
    input = (input.toarray())[0]
    for question in questions:
        question = question.toarray()
        num = float(np.matmul(question, input))
        denom = np.linalg.norm(question) * np.linalg.norm(input)

        if denom == 0:
            cos = 0.0
        else:
            cos = num / denom

        list.append(cos)

    best_idx = list.index(max(list))
    return best_idx


def answer_tfidf(input):
    input = filter_out_punctuation(input)
    input = word_segmentation(input)
    bow = tfidf_vectorizer.transform([input])
    best_idx = idx_for_largest_cosine_sim(bow, tfidf_X)
    return answers[best_idx]


teacher_dict = dict()


def write_teacher():
    filedir = os.getcwd() + '\index'
    filenames = os.listdir(filedir)

    for filename in filenames:
        filepath = filedir + '\\' + filename
        with open(filepath, encoding='utf-8')as f:
            cp_list = json.load(f)
        count = 0
        for cp_dict in cp_list:
            name = cp_dict["name"]
            print(name)
            namelist.append(name)
            teacher_dict[name] = [count, filename]
            count = count + 1
    wf('teacher_dict.json', teacher_dict)
    wf('namelist.json', namelist)


def find_teacher(name):
    list = teacher_dict[name]
    return list


def find_more(list, line):
    num, url = list
    filedir = os.getcwd() + r'\index'
    filepath = filedir + '\\' + url
    with open(filepath, encoding='utf-8')as f:
        cp_list = json.load(f)
    now_list = cp_list[num]
    find = now_list[line]
    return find


def play_sound(answer):
    from aip import AipSpeech

    """ 你的 APPID AK SK """
    APP_ID = '18013674'
    API_KEY = 'vy91NRWxtpYq0XPdRIGXEopp'
    SECRET_KEY = 'A1BBTZI159XVFs5rubMH517fhcP53nhW'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result = client.synthesis(answer, 'zh', 1, {
        'vol': 5,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        global tmp
        tmp += 1
        file = r'audio/' + str(tmp) + '.mp3'
        with open(file, 'wb') as f:
            f.write(result)

        playsound(file)


def search_teacher(str):
    s1 = str[0:3]
    n1 = str[0:2]
    s2 = str[3:]
    try:
        if s1 in namelist or n1 in namelist:
            # 教师相关
            if s1 in namelist:
                name = s1
            else:
                name = n1
            find_line = answer_tfidf(s2)
            line = find_line.strip('\n')
            finder = find_teacher(name)
            final_answer = find_more(finder, line)
            print(name, final_answer)
            play_sound(final_answer)
            return final_answer
        else:
            find_line = answer_tfidf(s2)
            line = find_line.strip('\n')
            if line[3] == 'n':
                final_answer = '并行与分布式软件实验室，数据库与信息系统实验室，南开大学计算机视觉实验室，南开大学媒体计算实验室，南开大学智能计算系统研究室'
                print(final_answer)
                play_sound(final_answer)
                return final_answer

            else:
                n = int(line[3])
                with open('lab.json', encoding='utf-8')as fl:
                    lab = json.load(fl)
                    final_answer = lab[n]
                    print(final_answer)
                    play_sound(final_answer)
                    return final_answer
    except:
        # 没有该项信息
        final_answer = '抱歉，这个问题我暂时不知道呢'
        print(final_answer)
        play_sound(final_answer)
        return final_answer


if __name__ == '__main__':
    # write_teacher()
    with open('teacher_dict.json', encoding='utf-8')as f:
        teacher_dict = json.load(f)
    with open('namelist.json', encoding='utf-8')as f:
        namelist = json.load(f)
    # 实例化object，建立窗口window
    window = tk.Tk()
    # 给窗口的可视化起名字
    window.title('我是南小开，难小开就是我')
    # 设定窗口的大小(长 * 宽)
    window.geometry('500x300')
    # 增加背景图片
    photo = tk.PhotoImage(file="bg.png")
    theLabel = tk.Label(window, image=photo, compound=tk.CENTER, fg="white")  # 前景色
    theLabel.pack()

    var_from = tk.StringVar()
    entry_from = tk.Entry(window, textvariable=var_from, font=('Arial', 14))
    entry_from.place(width=270, x=110, y=50)

    t = tk.Text(window, height=7)
    scroll = Scrollbar()
    scroll.place(x=98, y=173)
    scroll.config(command=t.yview)
    t.config(yscrollcommand=scroll.set)
    t.place(width=270, height=130, x=110, y=150)


    def hit_btn():
        # 定义一个函数功能供点击Button按键时调用，调用命令参数command=函数名
        e_from = var_from.get()
        text = search_teacher(e_from)
        t.delete(0.0, END)
        t.insert(INSERT, text)


    btn_search = tk.Button(window, text='OK', font=('Arial', 12), width=4, height=1, command=hit_btn)
    btn_search.place(x=220, y=87)

    # 主窗口循环显示，让window不断的刷新
    window.mainloop()
