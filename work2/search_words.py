import json
import jieba
from tkinter import *
import tkinter as tk  # 使用Tkinter前需要先导入
from PIL import Image, ImageTk
from itertools import count


class ImageLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 250

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def internal_term(each, BiWdIndex):
    ws = jieba.lcut(each)
    tmp_ids = BiWdIndex.get(ws[0], [])
    tm = tmp_ids
    if len(ws) > 1:
        # 对该词项进行分词，然后将每两个相邻的单词组合成一个词项
        for ww in range(len(ws) - 1):
            tmp_ids = []
            obj = ws[ww] + ws[ww + 1]  # 构造双词结构
            tmp_ids.extend(BiWdIndex.get(obj, []))

            ss = set(tmp_ids)
            tmp_ids = list(ss)
            tmp_ids.sort()
            # 对每个词的结果要取交集
            # 如果不在当前tmp_ids中出现，则删去
            if len(ws) == 2:
                return tmp_ids
            for tid in reversed(tm):
                # 反向删除
                if tid not in tmp_ids:
                    tm.remove(tid)
    return tm


def merge_vector(vec1, vec2, vec3):
    # not_ids, and_ids, or_ids
    print("in merge_vector(): not_ids, and_ids, or_ids: ")
    not_list = list(set(vec1))
    not_list.sort()
    print(not_list)
    and_list = list(set(vec2))
    and_list.sort()
    print(and_list)
    or_list = list(set(vec3))
    or_list.sort()
    print(or_list)

    len2 = len(not_list)
    len1 = len(and_list)
    res = []
    p1 = 0
    p2 = 0
    if len2 == 0 and len1 == 0:
        print("仅 or 短语组合")
        return or_list
    # 求差集
    while p1 < len1 and p2 < len2:
        while p1 < len1 and p2 < len2 and and_list[p1] < not_list[p2]:
            res.append(and_list[p1])
            p1 += 1
        while p2 < len2 and p1 < len1 and and_list[p1] > not_list[p2]:
            p2 += 1
        if p2 < len2 and p1 < len1 and and_list[p1] == not_list[p2]:
            p1 += 1
            p2 += 1
    while p1 < len1:
        res.append(and_list[p1])
        p1 += 1

    len3 = len(res)
    len4 = len(or_list)
    p3 = 0
    p4 = 0
    res_list = []
    # 列表求并集
    while p3 < len3 and p4 < len4:
        while res[p3] < or_list[p4] and p3 < len3:
            res_list.append(res[p3])
            p3 += 1
        while res[p3] > or_list[p4] and p4 < len4:
            res_list.append(or_list[p4])
            p4 += 1
        if res[p3] == or_list[p4]:
            res_list.append(res[p3])
            p3 += 1
            p4 += 1
    if p3 == len3:
        while p4 < len4:
            res_list.append(or_list[p4])
            p4 += 1
    else:
        while p3 < len3:
            res_list.append(res[p3])
            p3 += 1

    return res_list


def merge_with_pos(words, index):
    # words是同一种关系中的单词
    print("in merge_with_pos, input words: ")
    print(words)

    c_word = len(words)
    print("c_word: ")
    print(c_word)

    # 每次取一个单词，用字典存储它涉及到的诗词ID及对应的偏移信息
    # 以文章id为主键，值为列表，列表中存储关键词出现过的位置
    # 以第一个单词为基准，每次将当前第m个单词的字典与它的字典进行对比
    # 若在两个字典中，对于同一篇文章，得到的两个列表中出现位置相差为m，证明当前id符合条件
    tmp_dict = {}
    p = index.get(words[0], [])
    print("for each word, take out the poemID-postion-list : ")
    for li in p:
        print(li)
        if li[0] not in tmp_dict:
            tmp_dict[li[0]] = []
        for i in range(1, len(li)):
            tmp_dict[li[0]].append(li[i])
    pids = list(tmp_dict.keys())
    if c_word >= 2:
        m = 1
        while m < c_word:
            p = index.get(words[m], [])
            tmp_dict1 = {}
            # print("for each word, take out the poemID-postion-list : ")
            for li in p:
                #     print(li)
                if li[0] not in tmp_dict1:
                    tmp_dict1[li[0]] = []
                for i in range(1, len(li)):
                    tmp_dict1[li[0]].append(li[i])
            t2 = list(tmp_dict1.keys())
            for i in reversed(pids):
                # 反向删除
                if i not in t2:
                    pids.remove(i)
            for pid in reversed(pids):
                tmp_list = tmp_dict[pid]
                tmp_list.sort()
                tmp_list1 = tmp_dict1[pid]
                tmp_list1.sort()
                j = 0
                flag = 0
                for tid in tmp_list:
                    while j < len(tmp_list1):
                        if tid == tmp_list1[j] - m:  # m表示第m个词，同时也是与第一个词的间距
                            flag = 1
                            break
                        j += 1
                    if flag == 1:  # PoemID得到了确认
                        break
                if flag == 0:
                    pids.remove(pid)
            m += 1
    return pids


def search_poem(quiry, prefix):
    or_terms = []
    and_terms = []
    not_terms = []
    # 考虑优先级的关系，提取查询信息
    # 先利用“or”拆分字符串，把拆分结果记录在or_terms列表中
    or_terms.extend(quiry.split('or'))
    for each in or_terms:
        print(each)
        and_terms.extend(each.split('and'))
        # 对于其中的每一项，继续用“and”拆分，若该词项中不含“and”，则不做操作；
        if 'and' in each:
            # 若该词项中含有“and”，则将拆分的结果记录在and_terms列表中，并且从or_terms中删去该词项
            or_terms.remove(each)
        else:
            and_terms.remove(each)
    for each in and_terms:
        # 对于and_terms中的每一项，用“not”进行拆分，若该词项中不含“not”，则不做操作
        if 'not' in each:
            # 若该词项中含有“not”，则将拆分的结果记录在not_terms列表中，并且从and_terms中删去该词项
            not_terms.append(each.replace('not', ''))
            and_terms.remove(each)

    print(or_terms)
    print(and_terms)
    print(not_terms)

    filepath = prefix + "_poem_BiWordIndex.json"
    # 先进行双词索引
    with open(filepath, 'r', encoding='UTF-8') as f:
        BiWdIndex = json.load(f)
    f.close()
    # 要保证插入的id是有序且不重复的，集合（set）是一个无序的不重复元素序列
    not_ids = []
    ni = 0
    nm = [[], [], []]
    for each in not_terms:
        nm[ni] = internal_term(each, BiWdIndex)
        not_ids.extend(nm[ni])
        ni += 1

    tm = [[], [], []]
    ai = 0
    # 两层求交集操作
    for each in and_terms:
        tm[ai] = internal_term(each, BiWdIndex)
        ai += 1
    and_ids = tm[0]
    ii = 1
    while ii < 3 and len(tm[ii]) > 0:
        for i in reversed(and_ids):
            # 反向删除
            if i not in tm[ii]:
                and_ids.remove(i)
        ii += 1

    or_ids = []
    oi = 0
    om = [[], [], []]
    for each in or_terms:
        om[oi] = internal_term(each, BiWdIndex)
        or_ids.extend(om[oi])
        oi += 1

    poemIDs = merge_vector(not_ids, and_ids, or_ids)
    count = len(poemIDs)
    print("poemIDs: ")
    print(poemIDs)

    # 如果需要的话再进行位置索引
    if count == 0:
        # if flag == 1:
        print("----In PosIndex----")
        filepath2 = prefix + "_poem_PosIndex.json"
        with open(filepath2, 'r', encoding='UTF-8') as f:
            PosIndex = json.load(f)
        f.close()

        not_ids2 = []
        for each in not_terms:
            ws = jieba.lcut(each)
            not_ids2.extend(merge_with_pos(ws, PosIndex))

        and_ids2 = []
        cn = len(and_terms)
        if cn > 0:
            ws = jieba.lcut(and_terms[0])
            and_ids2.extend(merge_with_pos(ws, PosIndex))
            ind = 1
            while ind < cn:
                and_ids3 = []
                ws = jieba.lcut(and_terms[ind])
                and_ids3.extend(merge_with_pos(ws, PosIndex))
                for i in reversed(and_ids2):
                    # 反向删除
                    if i not in and_ids3:
                        and_ids2.remove(i)
                ind += 1

        or_ids2 = []
        for each in or_terms:
            ws = jieba.lcut(each)
            or_ids2.extend(merge_with_pos(ws, PosIndex))

        return merge_vector(not_ids2, and_ids2, or_ids2)
    else:
        return poemIDs


if __name__ == '__main__':
    total = 1
    ans_ids = []
    tmp_num = 0

    # 实例化object，建立窗口window
    window = tk.Tk()
    # 给窗口的可视化起名字
    window.title('古诗词检索系统')
    # 设定窗口的大小(长 * 宽)
    window.geometry('720x500')

    # 加载image
    canvas1 = tk.Canvas(window, width=80, height=45)
    image_file1 = tk.PhotoImage(file='img.png')
    image1 = canvas1.create_image(220, 0, anchor='n', image=image_file1)
    canvas1.pack(anchor="nw", ipadx=80)

    # 输入信息
    tk.Label(window, text='Search:', font=('Arial', 14)).place(x=10, y=50)
    tk.Label(window, text='Result:', font=('Arial', 14)).place(x=10, y=150)

    var_from = tk.StringVar()
    entry_from = tk.Entry(window, textvariable=var_from, font=('Arial', 14))
    entry_from.place(width=300, x=100, y=50)

    t = tk.Text(window, height=7)
    scroll = Scrollbar()
    scroll.place(x=405, y=170)
    scroll.config(command=t.yview)
    t.config(yscrollcommand=scroll.set)
    t.place(width=300, height=250, x=100, y=155)


    def hit_btn():
        # 定义一个函数功能供点击Button按键时调用，调用命令参数command=函数名
        # 搜索结果总数
        global total
        # 搜索结果
        global ans_ids
        # 当前展示的诗词的计数
        global tmp_num

        # 获取用户输入的信息
        e_from = var_from.get()
        print(e_from)
        ans_ids = search_poem(e_from, "song")
        total = len(ans_ids)
        # if total == 0:
        #     ans_ids = search_poem(e_from, "tang")
        tmp_num = 0
        if total > 0:
            t.delete(0.0, END)
            # 对应到文件名
            file_id = int(ans_ids[0] / 1000) * 1000
            print("The first fileID and poemID-in-file to be show is")
            print(file_id)
            num = ans_ids[0] - file_id
            print(num)
            # 由于唐诗和宋词是分块建的索引，所以要先判断需要加载哪个文件
            if ans_ids[0] < 255000:
                # 宋词
                path = "E:\ir\chinesepoetry\poet.song." + str(file_id) + ".json"
            else:
                # 唐诗
                path = "E:\ir\chinesepoetry\poet.tang." + str(file_id) + ".json"

            with open(path, 'r', encoding='UTF-8') as f:
                tp = json.load(f)
            f.close()
            # 将搜索结果中的第一首诗词信息展示在文本框中
            poem_dict = tp[num]
            author = poem_dict["author"]
            para = poem_dict["paragraphs"]
            title = poem_dict["title"]
            t.insert(INSERT, title + "\n")
            t.insert(INSERT, author + "\n")
            for i in para:
                t.insert(INSERT, i + "\n")
        else:
            t.delete(0.0, END)
            t.insert(INSERT, "未搜索到相关内容\n")


    def show_btn():
        # 搜索结果总数
        global total
        # 搜索结果
        global ans_ids
        # 当前展示的诗词的计数
        global tmp_num

        if total > 0:
            tmp_num = (tmp_num + 1) % total
            print("clicked show-btn , total num and tempID : ")
            print(total)
            tmp_id = ans_ids[tmp_num]
            t.delete(0.0, END)
            file_id = int(tmp_id / 1000) * 1000
            num = tmp_id - file_id
            print(tmp_id)
            if tmp_id < 255000:
                # 宋词
                path = "E:\ir\chinesepoetry\poet.song." + str(file_id) + ".json"
            else:
                path = "E:\ir\chinesepoetry\poet.tang." + str(file_id) + ".json"

            with open(path, 'r', encoding='UTF-8') as f:
                tp = json.load(f)
            f.close()
            poem_dict = tp[num]
            author = poem_dict["author"]
            para = poem_dict["paragraphs"]
            title = poem_dict["title"]
            t.insert(INSERT, title + "\n")
            t.insert(INSERT, author + "\n")
            for i in para:
                t.insert(INSERT, i + "\n")


    btn_search = tk.Button(window, text='Go', font=('Arial', 12), width=6, height=1, command=hit_btn)
    btn_search.place(x=200, y=85)

    btn_show = tk.Button(window, text='Next', font=('Arial', 12), width=6, height=1, command=show_btn)
    btn_show.place(x=200, y=420)

    lbl = ImageLabel(window)
    lbl.pack(anchor="ne", ipadx=30, ipady=0)
    lbl.load('pic/1.gif')
    # 主窗口循环显示，让window不断的刷新
    window.mainloop()
