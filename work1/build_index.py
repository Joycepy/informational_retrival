# 分块构建索引
import codecs
import os
import json
from email.parser import Parser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import math

r1 = u'[0-9’!"#$%&\'()*+,-./:;<=>?，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
base1 = 0
base2 = 98192
base3 = 198895
base4 = 366483
base5 = 472413
base6 = 517401


class Email():
    def __init__(self, e_id, e_path):
        self.words = []
        self.e_id = e_id
        self.e_path = e_path

    # 邮件内容预处理（包括删除停用词、词干化。邮件的收发件人不需要进行预处理）
    # 这里的参数不应该是
    def proc_text(self, text):
        word_tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_text = []
        # 删除停用词
        for w in word_tokens:
            if w not in stop_words:
                filtered_text.append(w)
        # 词干化
        Stem_words = []
        ps = PorterStemmer()
        for w in filtered_text:
            rootWord = ps.stem(w)
            Stem_words.append(rootWord)
        return Stem_words

    def get_words(self):
        # 以仅读的方式打开文件
        f = codecs.open(self.e_path, 'r', 'Windows-1252')
        fc = f.read()
        f.close()
        email = Parser().parsestr(fc)
        # 提取单词，并给不同位置的单词加上后缀
        # 0——From，1——To，2——Subject，3——Content
        # 邮件的发件人和收件人格式比较简单，不用做过多的处理，用,直接分割，并且不要修改大小写
        if email['From'] is not None:
            fm_token = email['From'].split(',')  # 以','分割当前文档的from邮箱号
            for i in fm_token:
                i = i.strip() + '0'
                self.words.append(i)
        # .strip()去空格（包括'\n', '\r', '\t', ' ')
        if email['To'] is not None:
            to_token = email['To'].split(',')
            for i in to_token:
                i = i.strip() + '1'
                self.words.append(i)
        # 邮件主题和内容中存在特殊符号、大小写、不同时态、单复数等，
        # 用正则表达式过滤特殊符号，掉包删除停用词，以及对单词进行标准化
        if email['Subject'] is not None:
            sb_filter = re.sub(r1, '', email['Subject'])
            sb_token = self.proc_text(sb_filter)
            for i in sb_token:
                i = i.lower() + '2'
                self.words.append(i)
        # 文章内容
        if email.get_payload() is not None:
            tx_filter = re.sub(r1, '', email.get_payload())
            tx_token = self.proc_text(tx_filter)
            for i in tx_token:
                i = i.lower() + '3'
                self.words.append(i)


class Index():
    def __init__(self):
        self.Dict = dict()
        self.DF = dict()

    # 将每篇文章得到的单词集合插入索引
    def addIndex(self, words, e_id):
        # 遍历此封邮件的单词，统计词频，用字典记录，key为单词，value为词频
        tf = dict()
        for i in words:
            if i in tf.keys():
                tf[i] += 1
            else:
                tf[i] = 1
        word_set = set(words)  # 去重
        for i in word_set:
            # 记录文档频率
            if i in self.DF.keys():
                self.DF[i] += 1
            else:
                self.DF[i] = 1
            # 向索引中加入这封邮件的信息
            if i not in self.Dict.keys():
                self.Dict[i] = [(e_id, tf[i])]  # 在这里加[]，将value变成一个list，方便后面的append
                print("log")
            else:  # 这个单词已经在词典中（使用set去重，该邮件id在之前一定未出现过，所以这一点不用考虑）
                self.Dict[i].append((e_id, tf[i]))


# 把文件字典写入磁盘
def wf(path, obj):
    desti = open(path, 'w', encoding='utf-8')
    desti.write(json.dumps(obj, sort_keys=True, indent=4))
    desti.close()


fid = base1
file_id = {}
doc_index = Index()
if __name__ == '__main__':
    try:
        for root, dirs, files in os.walk("E:\\a_d"):
            for file in files:
                fid += 1
                f_path = os.path.join(root, file)
                print(f_path, fid)
                file_id[f_path] = fid
                email = Email(fid, f_path)
                email.get_words()
                doc_index.addIndex(email.words, fid)
        wf('id_t_z.json', file_id)
        wf('dict_a_d.json', doc_index.Dict)
        wf('df_t_z.json', doc_index.DF)
    except:
        print("Failed")
