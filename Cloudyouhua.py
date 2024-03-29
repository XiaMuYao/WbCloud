# - * - coding: utf - 8 -*-
from os import path

from pkg_resources._vendor.appdirs import unicode
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
# jieba.load_userdict("txt\userdict.txt")
# 添加用户词库为主词典,原词典变为非主词典
from wordcloud import WordCloud, ImageColorGenerator

# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
# d = path.dirname('.')
d = path.dirname(__file__)

stopwords = {}
isCN = 1 #默认启用中文分词
# back_coloring_path = "stormtrooper_mask.png" # 设置背景图片路径
text_path = '45185521.txt' #设置要分析的文本路径
font_path = 'DroidSansFallbackFull.ttf' # 为matplotlib设置中文字体路径没
imgname1 = "WordCloudDefautColors.png" # 保存的图片名字1(只按照背景图片形状)
imgname2 = "WordCloudColorsByImg.png"# 保存的图片名字2(颜色按照背景图片颜色布局生成)

# back_coloring = imread(path.join(d, back_coloring_path))# 设置背景图片

# 设置词云属性
wc = WordCloud(font_path=font_path,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=1000,  # 词云显示的最大词数
               # mask=back_coloring,  # 设置背景图片
               max_font_size=100,  # 字体最大值
               random_state=500,
               width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
               )

# 添加自己的词库分词
def add_word(list):
    for items in list:
        jieba.add_word(items)

text = open(path.join(d, text_path),encoding='utf-8').read()

wc.generate(text)

plt.figure()
# 以下代码显示图片
plt.imshow(wc)
plt.axis("off")
plt.show()
# 绘制词云

# 保存图片
wc.to_file(path.join(d, imgname1))

# image_colors = ImageColorGenerator(back_coloring)

# plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
# 绘制背景图片为颜色的图片
plt.figure()
# plt.imshow(back_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
# 保存图片
wc.to_file(path.join(d, imgname2))