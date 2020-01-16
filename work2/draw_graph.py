from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json


def draw_graph():
    with open("song_words_bag.json") as f:
        mytext1 = json.load(f)
    f.close()
    wl = " ".join(mytext1)
    # 加载背景图片
    # cloud_mask = np.array(Image.open("cloud.png"))
    # 设置词云
    wc = WordCloud(background_color="white",  # 设置背景颜色
                   # mask=cloud_mask,  # 设置背景图片
                   max_words=2000,  # 设置最大显示的字数
                   # stopwords = "", #设置停用词
                   font_path="FangZhengHeiTiFanTi-1.ttf",
                   # 设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
                   max_font_size=50,  # 设置字体最大值
                   random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                   )
    myword = wc.generate(wl)  # 生成词云

    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    # 存储图片
    wc.to_file('a4.png')

if __name__ == '__main__':
    draw_graph()
