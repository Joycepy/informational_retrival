import json
import re
from time import sleep

# 用来解析 HTML 文本，可以获取爬到的 HTML 文本中的各个项的属性
from bs4 import BeautifulSoup
# 可以模拟浏览器获取异步数据或者执行点击操作
from selenium import webdriver

# 模拟火狐浏览器执行点击操作
browser = webdriver.Firefox()


def wf(path, obj):
    file = open(path, 'w', encoding='utf-8')
    file.write(json.dumps(obj, sort_keys=True, indent=4))
    file.close()


# 不同老师有的信息可能并不展示，需要使用try-catch结构，将没有找到的项置为空
def get_cc_data(t_info, url):
    urlset = set()  # 用于判断是否重复
    try:
        # 使用剖析器为html.parser
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        allList = soup.select('tr')
        Len = len(allList)
        cc = ['name', 'sex', 'department', 'position', 'title', 'degree', 'major', 'telephone', 'email', 'direction',
              'introduction']
        for i in range(1, Len):
            a = allList[i].select('td')[0].select('a')
            try:  # 如果抛出异常就代表为空
                href = a[0]['href']
                if not href.startswith('http'):
                    href = r'http://cc.nankai.edu.cn' + href
                browser.get(href)
                if href in urlset:
                    continue
                else:
                    urlset.add(href)
                    intro = browser.find_element_by_class_name('text').text
                    info = {}
                    for each in range(1, 11):
                        x_path = r'/html/body/div[2]/div[1]/div/div[1]/div[1]/p[%d]/span[2]' % each
                        info[cc[each - 1]] = browser.find_element_by_xpath(x_path).text
                    print(info)
                    info[cc[10]] = (intro[0:min(len(intro), 200)] + ' ……')
                    sleep(1)
                    t_info.append(info)
            except:
                href = ''
    except Exception as e:
        print(e)


def computercol():
    info = []
    urls = [r'http://cc.nankai.edu.cn/jswyjy/list.htm', r'http://cc.nankai.edu.cn/fjswfyjy/list.htm',
            r'http://cc.nankai.edu.cn/js/list.htm', r'http://cc.nankai.edu.cn/syjxdw/list.htm']
    for url in urls:
        browser.get(url)
        get_cc_data(info, url)
    # 写入
    wf('TeacherInfo/computer.json', info)


def get_ai_data(t_info, href):
    aii = ['name', 'sex', 'department', 'position', 'title', 'degree', 'major', 'telephone', 'email', 'direction',
           'introduction']
    browser.get(href)
    try:
        intro = browser.find_element_by_xpath(
            r'/html/body/div[3]/div/div/div/div/div/div/form/div/div/div/div[2]/div[2]/div/div').text
    except:
        intro = ''
    info = {}
    try:
        for each in range(1, 11):
            x_path = r'/html/body/div[3]/div/div/div/div/div/div/form/div/div/div/div[1]/div[2]/div/div/p[%d]/span' % (
                    each + 1)
            info[aii[each - 1]] = browser.find_element_by_xpath(x_path).text
        info[aii[10]] = (intro[0:min(len(intro), 200)] + ' ……')
    except:
        return
    print(info)
    sleep(1)
    t_info.append(info)


def ai():
    info = []
    for num in range(2794, 2801):
        href = r'https://ai.nankai.edu.cn/info/1033/%d.htm' % num
        get_ai_data(info, href)
    for num in range(2802, 2821):
        href = r'https://ai.nankai.edu.cn/info/1034/%d.htm' % num
        get_ai_data(info, href)
    # 写入
    wf('TeacherInfo/ai.json', info)


def get_his_data(t_info, url):
    urlset = set()  # 用于判断是否重复
    try:
        # 使用剖析器为html.parser
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        allList = soup.find_all(name='li', attrs={"class": "teacher_list_unit cl"})
        Len = len(allList)
        for i in range(1, Len):
            a = allList[i].select('a')
            infoList = re.sub('\s', '', allList[i].text)
            pos1 = infoList.find(u'职务：')
            pos2 = infoList.find(u'专业：')
            pos3 = infoList.find(u'研究方向')
            try:  # 如果抛出异常就代表为空
                href = a[0]['href']
                if not href.startswith('http'):
                    href = r'https://history.nankai.edu.cn/' + href
                browser.get(href)
                if href in urlset:
                    continue
                else:
                    urlset.add(href)
            except:
                href = ''
            try:
                intro = browser.find_element_by_class_name('tabbox-page').text
                intro = intro[0:min(len(intro), 200)] + ' ……'
                sleep(1)
            except:
                intro = ''
            # 把爬取到的每条数据组合成一个字典用于数据库数据的插入
            new_dict = {
                "name": infoList[1:pos1],
                "title": infoList[pos1 + 3:pos2],
                'department': infoList[pos2 + 3:pos3],
                'direction': infoList[pos3 + 5:len(infoList)],
                "introduction": intro
            }

            t_info.append(new_dict)
            print(new_dict)

    except Exception as e:
        print(e)


def get_fin_data(t_info, url):
    urlset = set()  # 用于判断是否重复
    try:
        # 使用剖析器为html.parser
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        allList = soup.select('.shiziListBox')
        for teacher in allList:
            a = teacher.select('a')
            try:  # 如果抛出异常就代表为空
                href = a[0]['href']
                browser.get('http://finance.nankai.edu.cn' + href)
                if href in urlset:
                    continue
                else:
                    urlset.add(href)
                intro = browser.find_element_by_class_name('teacherDetail').text
                intro = intro[0:min(len(intro), 200)] + ' ……'
                sleep(1)
            except:
                href = ''
            try:  # 如果抛出异常就代表为空
                e_mail = a[1].text
            except:
                e_mail = ''

            text = teacher.select('p')[0].text.split()
            name = text[0]
            if len(text) < 2:
                cate = ''
            else:
                cate = text[1]
            # 把爬取到的每条数据组合成一个字典用于数据库数据的插入
            new_dict = {
                "name": name,
                "title": cate,
                "email": e_mail,
                "introduction": intro
            }
            t_info.append(new_dict)
            print(new_dict)
    except Exception as e:
        print(e)


def finance():
    info = []
    urls = [r'http://finance.nankai.edu.cn/f/teacher/teacher/qzjs',
            r'http://finance.nankai.edu.cn/f/teacher/teacher/jzds',
            r'http://finance.nankai.edu.cn/f/teacher/teacher/rxjs']
    for url in urls:
        browser.get(url)
        get_fin_data(info, url)
    # 写入
    wf('TeacherInfo/finance.json', info)


def history():
    info = []
    urls = [r'https://history.nankai.edu.cn/16054/list.htm',
            r'https://history.nankai.edu.cn/16055/list.htm',
            r'https://history.nankai.edu.cn/16056/list.htm']
    for url in urls:
        browser.get(url)
        get_his_data(info, url)
    # 写入
    wf('TeacherInfo/history.json', info)


if __name__ == "__main__":
    #  computercol()
    # ai()
    history()
    finance()