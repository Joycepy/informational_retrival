import json
# logging模块定义的函数和类为应用程序和库的开发实现了一个灵活的事件日志系统
import logging

import math
import whoosh.index as index
# flask是一个使用Python编写的轻量级Web应用框架
from flask import Flask, request, render_template, redirect, url_for, Response
# 查询解析器将用户提交的查询字符串转换为查询对象
from whoosh.qparser import QueryParser
from whoosh.query import *

logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='new.log',
                    filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(message)s'
                    # 日志格式
                    )
pg = []


def func(x, y):
    # 让每一项的大小比较转换为他们各自的按照PR值比较
    if pg[x['href']] < pg[y['href']]:
        return -1
    if pg[x['href']] == pg[y['href']]:
        return 0
    else:
        return 1


def resort(buf, f):
    if f == 0:
        global pg
        with open('PRInfo/pageGraph.json', 'r', encoding='UTF-8') as f:
            pg = json.load(f)
        f.close()
        # 进行重载
        sorted(buf, func)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        sent = request.form['query']
        target = request.form['type']
        try:
            isLogic = request.form['check']
        except:
            isLogic = '0'
        return redirect(url_for('search_result', sent=sent, target=target, isLogic=isLogic, page=1))
    else:
        return render_template('hello.html')


buffer = []


# 使用route()修饰器注明通过什么样的url可以访问定义的函数，
# 同时在函数中返回要显示在浏览器中的信息，
# 相当于是MVC中的Contoller
@app.route('/<sent>')
# <sent>会被传来的参数替换，组成函数的路由
def search_result(sent):
    global buffer
    if sent == 'favicon.ico':
        with open("./static/images/icon.png", 'rb') as f:
            image = f.read()
        return Response(image, mimetype='image/png')
    page = int(request.args.get('page'))
    details = []
    target = request.args.get('target')
    isLogic = request.args.get('isLogic')

    if page != 1:  # 说明已经查询过，直接从缓存
        if page < 1:
            page = 1
        max_page = min(int(math.ceil(len(buffer) / 3.0)), 7)
        if page > max_page:
            page = max_page
        tmp = max(0, page - 1)
        print('一共发现%d份文档。' % len(buffer), page)
        for i in range(tmp * 3, min(min(tmp * 3 + 3, 20), len(buffer))):
            details.append(buffer[i].fields())  # details中的每一项是一个词典，包含一个人的除简介外的所有信息
            print(i, " : ", json.dumps(buffer[i].fields(), ensure_ascii=False))
    else:
        myindex = index.open_dir("indexdir")
        # 按域搜索，搜的类型为target，值为sent
        qp = QueryParser(target, schema=myindex.schema)

        if isLogic == '1':
            # 逻辑查询
            if 'OR' in sent:
                or_terms = sent.split('OR')
                q = Or([Term(target, or_terms[0]), Term(target, or_terms[1])])
        else:
            q = qp.parse(sent)
        searcher = myindex.searcher()
        buffer = searcher.search(q, limit=20)
        print(buffer)
        for i in range(min(3, len(buffer))):
            buffer[i].highlights("intro")
            details.append(buffer[i].fields())  # details中的每一项是一个词典，包含一个人的除简介外的所有信息
            print(json.dumps(buffer[i].fields(), ensure_ascii=False))

        # PageRank算法排序
        resort(buffer, 1)
    max_page = min(int(math.ceil(len(buffer) / 3.0)), 7)
    if page > max_page:
        page = max_page
    return render_template('search_result.html', sent=sent, target=target, page=page, max_page=max_page,
                           details=details)


if __name__ == '__main__':
    # if __name__==’__main__’的意思是如果此文件是直接运行的
    # 才会执行app.run()这个方法，如果是通过import在其它py文件中调用的话是不会执行的
    app.run()
