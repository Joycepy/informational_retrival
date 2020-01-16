import json
import os.path
# Whoosh是用于索引文本，然后搜索索引的类和函数的库
# 建立索引的过程中需要对获取的内容进行分词，whoosh默认的分词对中文不太友好，
from jieba.analyse import ChineseAnalyzer
from whoosh.fields import Schema, ID, TEXT
from whoosh.index import create_in

analyzer = ChineseAnalyzer()

# 创建schema, stored为True表示能够被检索
schema = Schema(
    name=TEXT(stored=True, analyzer=analyzer),
    e_mail=ID(stored=True),
    href=ID(stored=True),
    collage=TEXT(stored=True, analyzer=analyzer),
    category=TEXT(stored=True, analyzer=analyzer),
    direction=TEXT(stored=True, analyzer=analyzer),
    department=TEXT(stored=True, analyzer=analyzer),
    intro=TEXT(stored=True, analyzer=analyzer),
)

# 解析数据文件
with open('TeacherInfo/finance.json', 'r', encoding='utf-8') as f:
    allLists = json.load(f)
f.close()
with open('TeacherInfo/computer.json', 'r', encoding='utf-8') as f:
    allLists.extend(json.load(f))
f.close()
with open('TeacherInfo/history.json', 'r', encoding='utf-8') as f:
    allLists.extend(json.load(f))
f.close()
# 存储schema信息至indexdir目录
indexdir = 'indexdir/'
if not os.path.exists(indexdir):
    os.mkdir(indexdir)
ix = create_in(indexdir, schema)

# 按照schema定义信息，增加需要建立索引的文档
writer = ix.writer()

for i in allLists:
    name = i.get('name', '')
    e_mail = i.get('e_mail', '')
    cate = i.get('cate', '')
    href = i.get('href', '')
    collage = i.get('collage', '')
    intro = i.get('intro', '')
    direction = i.get('direct', '')
    department = i.get('depart', '')
    writer.add_document(name=name, e_mail=e_mail, href=href, collage=collage, category=cate, intro=intro,
                        direction=direction, department=department)
writer.commit()

