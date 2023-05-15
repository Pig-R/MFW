# -*- coding: utf-8 -*-
# 该文件用以生成词云
import wordcloud
from wordcloud import WordCloud, ImageColorGenerator
from tfidf import names  # 词频的变量
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image      # 读取图片的包
import matplotlib.image as mpimg
for i in range(len(names)):  # (2, 3)
    """下面两段为了生成字典"""
    f = open(r"..\TFIDF\tfidf_"+names[i]+"_1.txt", "r", encoding='utf-8')
    line = f.readline()
    # 重新整一个txt放吧（关键字，TFIDF权重），一行一行来，不然难处理
    dict_path = r'..\datadict\tfidf_'+names[i]+r'_dict.txt'
    with open(dict_path, 'w', encoding='utf-8') as fr:
        while line:
            a = line.strip().strip("[").strip("]").strip('(').strip(')').replace('), (', '\n')
            fr.write(a.__str__() + '\n')
            line = f.readline()
    fr.close()

    # 首先生成一个字典dict_view,如果碰到重复的关键词，放TFIDF值大的那个进去
    dict_f = open(dict_path, 'r', encoding='utf-8')
    dict_view = {}
    keys = []  # 用来存储读取的顺序
    for line in dict_f:
        v = line.replace("'", '').strip().split(', ')  # ['一家', '0.07577536430126272'] len:2
        v[1] = float(v[1])
        if v[0] not in dict_view:
            dict_view[v[0]] = v[1]
        else:
            dict_view[v[0]] = max(dict_view[v[0]], v[1])
        keys.append(v[0])
    dict_f.close()
    # 纪念馆设置一下黑底白字
    #if names[i] == "纪念馆":bgcolor = 'black'; c_f = 'lambda *args, **kwargs: white'
    # 设置词云图相关参数
    wc = WordCloud(width=300,
                   font_path="STXINGKA.TTF",
                   scale=2,          # 按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍。
                   mode="RGBA",      # 当参数为“RGBA”并且background_color不为空时，背景为透明。
                   background_color='white',
                   # background_color='black',
                   # color_func = lambda *args, **kwargs: 'white'
    )
    wc.generate_from_frequencies(dict_view)  # 利用生成的dict文件制作词云图
    wc.to_file(r'..\ciyunImg\ciyun'+names[i]+r'.png')








# print(dict_view)
# print(dict_view['话说回来'])
# print(len(dict_view))
# print(dict_view['一家'], type(dict_view['一家']))

# l = [(1,'2'), (3,'4'), (5,6)]
# print(type(l))
# print(type(l[1][1]))  # str
# print(type(l[1][0]))  # int