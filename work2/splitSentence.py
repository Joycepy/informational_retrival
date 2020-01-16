# 对于测试数据，先将每一首古诗对应到一个ID
# 借鉴作业一中的递归读取文件、将字典写入文件的函数
# 把文件字典写入磁盘
import json
import os
import jieba


def wf(path, obj):
    file = open(path, 'w', encoding='utf-8')
    file.write(json.dumps(obj, sort_keys=True, indent=4))
    file.close()


def rf(path, obj):
    # 返回的应该是一个长度为1000的列表，每一项是当前文档内的一首古诗的内容分词结果
    tmp_file = open(path, 'r', encoding='utf-8')
    tmp_list = json.loads(tmp_file.read())
    for j in range(1000):
        # 对于每首诗词，先提取正文部分
        sentence_list = tmp_list[j]["paragraphs"]
        poet = tmp_list[j]["author"]
        poem_index.poets.append(poet)  # 便于完成附加功能里的数据统计分析
        word_count = 0
        # 每首诗词的单词信息用列表存储，列表的每一项是单词和位置偏移构成的元组
        single_poem = []
        for sentence in sentence_list:
            # 使用jieba的精确模式进行分词，把结果放入obj
            words = jieba.lcut(sentence)
            for word in words:
                # 过滤掉符号等无用信息
                if word not in ['，', '。', '！', '？', '：', '{', '}', '/', '（', '）']:
                    # 给每个词附加位置偏移信息
                    single_poem.append((word, word_count))
                    word_count += 1
        obj.append(single_poem)
    tmp_file.close()


class Index():
    def __init__(self):
        self.PosDict = dict()  # 位置索引
        self.BiWord = dict()  # 双词索引
        # 统计诗人和单词的信息
        self.Bag = list()
        self.poets = list()

    # 将每篇文章得到的单词集合插入索引
    def add_index(self, poem_id, word_tuples):
        temp = "$"
        # words是一个元素为元组的列表
        for k in word_tuples:
            # k=(word,pos)
            self.Bag.append(k[0])
            if len(k[0]) >= 2:
                if k[0] in self.BiWord:
                    id_list = self.BiWord[k[0]]
                    if poem_id not in id_list:
                        id_list.append(poem_id)
                else:
                    self.BiWord[k[0]] = [poem_id]
            # 添加双词索引，
            # 将每两个连续的词组成一个词项放到词典中
            binary = temp + k[0]
            # 会有三种情况：
            # (1)	该词项在双词索引中尚未出现，那么，加入{词项，[PoemID]}的键值对；
            # (2)	该词项已在双词索引中出现，但词项对应的列表中没有当前的PoemID，那么，在该列表中加入PoemID；
            # (3)	该词项已在双词索引中出现，并且词项对应的列表中含有当前的PoemID，那么，直接处理下一个词项。
            if binary in self.BiWord:
                id_list = self.BiWord[binary]
                if poem_id not in id_list:
                    id_list.append(poem_id)
            else:
                self.BiWord[binary] = [poem_id]

            # 添加位置索引
            # key为词项，value是一个双层的列表，内层列表表示一首诗词关于该词项的位置信息，
            # 0 号元素存放诗词ID，后续的元素是key在该诗词中的偏移量
            if k[0] in self.PosDict:
                # term是已经存在的关键字
                poetry = self.PosDict[k[0]]
                # 在poetry列表中找编号id的列表，并加入位置信息
                flag = 0  # 0表示 poem_id 不在当前的列表中
                for item in poetry:
                    if item[0] == poem_id:
                        # 对应的列表中的某个内层列表的0号元素是PoemID，那么，在内层列表中追加元素pos
                        flag = 1
                        item.append(k[1])
                        break
                if flag == 0:
                    # 对应的列表中未出现PoemID，那么，在现有列表中附加一个列表[PoemID，pos]
                    poetry.append([poem_id, k[1]])
            else:
                # term不属于PosIndex的关键字，那么，加入key为term，value为[[PoemID,pos]]的键值对；
                self.PosDict[k[0]] = [[poem_id, k[1]]]


poem_index = Index()
if __name__ == '__main__':
    base1 = 0
    base2 = 255000
    try:
        for root, dirs, files in os.walk("E:\\ir_song"):
            for file in files:
                f_path = os.path.join(root, file)
                # 路径中的数字
                file_id = ''.join([x for x in file if x.isdigit()])
                file_id = int(file_id)
                print(f_path)
                file_id += base1
                # file_id += base2
                poem_list = []
                rf(f_path, poem_list)
                for i in range(1000):
                    poem_words = poem_list[i]
                    # 利用文件名和数组下标对诗词进行编号
                    p_id = file_id + i
                    poem_index.add_index(p_id, poem_words)
        # 将索引写入磁盘
        wf('song_poem_PosIndex.json', poem_index.PosDict)
        wf('song_poem_BiWordIndex.json', poem_index.BiWord)
        wf('song_words_bag.json', poem_index.Bag)
        wf('song_poets.json', poem_index.poets)
    except:
        print("Failed")
