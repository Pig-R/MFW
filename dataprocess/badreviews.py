# coding=utf-8
# 差评
# 将八个景点差评分词以txt文件形式保存，和全部评论分开显得好看
from wordcloud import WordCloud
from gensim import corpora, models, similarities
import xlrd
from fencitxt import remove_urls, stopwordslist, seg_depart
xlsx_path = r"..\mafengwo\spiders\NanjingHuai.xlsx"
workbook = xlrd.open_workbook(xlsx_path, 'utf-8')
sheet1 = workbook.sheet_by_index(0)  # 第一个工作簿
savePath = r"..\BadRes\\"
names = ['总统府', '中山陵', '纪念馆', '钟山风景区', '夫子庙-秦淮河', '博物院', '玄武湖', '鸡鸣寺']
mark = 1  # excel第一行
seq = 0   # names第几个元素


# 写入txt文件的分词文本
def WriteFenciTxt(M, S):   # M初始值是1 M控制行，S控制写入哪个文件
    sentence = remove_urls(sheet1.cell(M, 2).value)
    words = seg_depart(sentence)
    txt = open(savePath + names[S] + r'.txt', mode='a+', encoding='utf-8')  # 先写第一行
    txt.write(words + '\n')  # \n 换行符
    for i in range(M+1, sheet1.nrows):      # 写每个景点首行之外的其他行
        if len(sheet1.cell(i, 0).value) == 0:
            sentence = remove_urls(sheet1.cell(i, 2).value)
            words = seg_depart(sentence)
            txt.write(words + '\n')  # \n 换行符
        else:
            M = i  # 一个景点最后一行空的
            WriteFenciTxt(M, S + 1)   # 递归调用自己，去写下一个景点
            break


# 将分完词的文档加载成符合gensim文格式的输入
def createTFIDFdict():
    for i in range(len(names)):
        train = []
        with open(r'..\BadRes\\'+names[i] + r'.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = [word.strip() for word in line.split()]
                train.append(line)
        # 构造词典
        dictionary = corpora.Dictionary(train)
        corpus = [dictionary.doc2bow(text) for text in train]
        tfidf_model = models.TfidfModel(corpus)
        with open(r'..\BadRes\tfidf_' + names[i] + r'_1.txt', 'w', encoding='utf-8') as idftxt:  # 另外的文本，有中文，清晰一点
            for doc in tfidf_model[corpus]:
                a = []
                for j in range(len(doc)):
                    # print(dict(dictionary.items())[doc[i][0]], doc[i][1])
                    l = (dict(dictionary.items())[doc[j][0]], doc[j][1])
                    a.append(l)
                idftxt.write(a.__str__() + '\n')


def word_cloud(name_str):
        f = open(r"..\BadRes\tfidf_" + name_str + "_1.txt", "r", encoding='utf-8')
        line = f.readline()
        # 重新整一个txt放吧（关键字，TFIDF权重），一行一行来，不然难处理
        dict_path = r'..\BadRes\tfidf_' + name_str + r'_dict.txt'
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
        # 设置词云图相关参数
        wc = WordCloud(width=300,
                       font_path="STXINGKA.TTF",
                       scale=2,  # 按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍。
                       mode="RGBA",  # 当参数为“RGBA”并且background_color不为空时，背景为透明。
                       background_color='white',
                       )
        wc.generate_from_frequencies(dict_view)  # 利用生成的dict文件制作词云图
        wc.to_file(r'..\BadRes\词云1' + name_str + r'.png')


# WriteFenciTxt(mark, seq)
# createTFIDFdict()  # 计算tfidf并写入文件
# for i in range(len(names)): word_cloud(names[i])
word_cloud(names[0])
