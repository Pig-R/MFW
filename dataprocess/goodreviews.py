# coding=utf-8
# 好评,跟差评代码完全一样。重复写只是为了好区分
# 本代码实现好评差评作为LDA的输入
from gensim import corpora, models, similarities
import xlrd
import warnings
warnings.filterwarnings('ignore')
import pyLDAvis.gensim_models
from gensim.models import LdaModel
import codecs
import wordcloud
import cv2
import matplotlib.pyplot as plt
from fencitxt import remove_urls, seg_depart
import matplotlib
from gensim.models.coherencemodel import CoherenceModel
xlsx_path = r"..\mafengwo\spiders\NanjingHao.xlsx"
workbook = xlrd.open_workbook(xlsx_path, 'utf-8')
sheet1 = workbook.sheet_by_index(0)  # 第一个工作簿
savePath = r"..\GoodRes\\"
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


def conecttxt():  # 将好评差评写入同一个文件下
    for i in names:
        Path1 = r'..\BadRes\\' + i + '.txt'
        Path2 = r'..\GoodRes\\' + i +'.txt'
        with open(Path1, 'r', encoding='utf-8') as f1:
            for line in f1.readlines():
                with open(Path2, 'a+', encoding='utf-8') as f2:
                    f2.write(line)
            f2.close()


# 将分完词的文档加载成符合gensim文格式的输入 旧的代码，不用了
def TFIDF_And_LDA():
    train = []   # 8个景点全部评论的分词结果都加到这里面。
    for i in range(len(names)):
        with open(savePath + names[i] + r'.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = [word.strip() for word in line.split()]
                train.append(line)
        # 构造词典
    dictionary = corpora.Dictionary(train)
    corpus = [dictionary.doc2bow(text) for text in train]
    lda = models.LdaModel(corpus=corpus, id2word=dictionary,
                          num_topics=8, iterations=30, passes=50,
                          random_state=42)   # iterations迭代次数
    topic_list = lda.print_topics()
    print("8个主题的单词分布为：\n")
    for topic in topic_list:
        print(topic)

    # 对每条新闻文本进行主题推断
    for i, doc in enumerate(corpus):
        # print(lda[doc], doc)
        topic = sorted(lda[doc], key=lambda x: x[1], reverse=True)[0][0]
        print('文本编号：{}，主题编号：{}'.format(i, topic))
    d = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, mds='pcoa', sort_topics=True)
    pyLDAvis.save_html(d, 'lda_show.html')  # 将结果保存为html文件


def LDA(K):
    train = []  # 所有样本
    for i in range(len(names)):
        with open(savePath + names[i] + r'.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = [word.strip() for word in line.split()]
                train.append(line)
    dictionary = corpora.Dictionary(train)  # """构建词频矩阵，训练LDA模型"""
    corpus = [dictionary.doc2bow(text) for text in train]
    tfidf = models.TfidfModel(corpus)  # 统计tfidf
    corpustfidf = tfidf[corpus]  # 得到每个文本的tfidf向量，稀疏矩阵

    lda = LdaModel(corpus=corpustfidf, id2word=dictionary, minimum_probability=pow(0.01, 1000),
                   num_topics=K, alpha='auto', eta='auto', iterations=1000, gamma_threshold=0.001, random_state=1)
    # 取主题下的关键词#
    keyword = codecs.open(r'..\LDAoutput\TopicKeyword' + str(K) + '.txt', 'w', encoding='utf8')
    i = 0  # 第i个主题
    for topic in lda.print_topics(num_topics=K, num_words=40):
        print('----Topic ' + str(i) + '-----:')
        keyword.write('----Topic ' + str(i) + '-----:' + '\n')
        print(topic)
        topic = str(topic).split(',')[1]
        topic = topic.strip('\')')
        topiclist = str(topic).split('+')
        word_list = []
        for topic in topiclist:
            topic = topic.replace('\'', '').strip('\r\n')
            topic = topic.replace('*', ' ').strip('\r\n')
            topic = topic.replace('"', '').strip('\r\n')
            topic = topic.strip(' ')
            topic = topic.split(' ')
            weight = topic[0]
            word = topic[1]
            word_list.append(word)
            print('word and weight:', word, weight)
            keyword.write(word + ' ' + str(float(weight)) + '\n')
        i = i + 1
        text = " ".join(word_list)
        w = wordcloud.WordCloud(width=1000, height=800, background_color="white", max_words=70,
                                font_path=r"simkai.ttf")
        w.generate(text)  # 生成每个主题包含的关键词云图
        image = r"..\LDAoutput\Topic" + str(i) + "_wordcloud.png"
        w.to_file(image)  # 保存云图
        img_bgr = cv2.imread(image)  # BGR通道
        img_rgb = img_bgr[:, :, ::-1]  # python中::-1代表反转，也就是将BGR通道变成RGB通道
        plt.imshow(img_rgb)
        # plt.show()
    dictionary.token2id  # 查看dictionary中词频
    doc_topic = lda.get_document_topics(corpustfidf)  # doc_topic是经过LDA训练后的文档-主题矩阵#文档-主题概率分布
    # 打印每篇文档最高概率主题
    TopicIDList = []  # 提取概率最大值为topic
    for prolist in lda.get_document_topics(corpustfidf)[:]:
        # print('prolist:',prolist)
        listj = []
        for pro in prolist:
            # print('pro:',pro)
            listj.append(pro[1])
        Index = listj.index(max(listj))  # 最大的Topic
        # print('Topic Index:',Index)
        TopicIDList.append((int(Index)) + 162)
    lda.save(r'..\LDAoutput\lda.model')  # 保存lda模型
    lda = models.ldamodel.LdaModel.load(r'..\LDAoutput\lda.model')






# # 计算coherence
# def coherence(num_topics):
#     dictionary = corpora.Dictionary(train1)  # """构建词频矩阵，训练LDA模型"""
#     corpus = [dictionary.doc2bow(text) for text in train1]
#     tfidf = models.TfidfModel(corpus)  # 统计tfidf
#     corpustfidf = tfidf[corpus]  # 得到每个文本的tfidf向量，稀疏矩阵
#
#     lda = LdaModel(corpus=corpustfidf, id2word=dictionary, minimum_probability=pow(0.01, 1000),
#                    num_topics=num_topics, alpha='auto', eta='auto', iterations=1000,
#                    gamma_threshold=0.001, random_state=1)
#     ldacm = CoherenceModel(model=lda, texts=train1, dictionary=dictionary, coherence='c_v')
#     return ldacm.get_coherence()
# # 这里得有if __name__ == '__main__':一句
# if __name__ == '__main__':
#     train1 = []
#     for i in range(len(names)):
#         with open(savePath + names[i] + r'.txt', 'r', encoding='utf-8') as f:
#             for line in f.readlines():
#                 line = [word.strip() for word in line.split()]
#                 train1.append(line)
#     x = range(1, 11)
#     y = [coherence(i) for i in x]
#     plt.plot(x, y)
#     plt.xlabel('主题数目')
#     plt.ylabel('Coherence Score')
#     plt.rcParams['font.sans-serif'] = ['SimHei']
#     matplotlib.rcParams['axes.unicode_minus'] = False
#     plt.title('主题-coherence变化情况')
#     plt.savefig("主题个数变化", dpi=1500)
#     plt.show()

# 首次运行把151及152行注释拿掉
# WriteFenciTxt(mark, seq)
# conecttxt()
# TFIDF_And_LDA()  之前的写的方法，可以不要了，与LDA方法实现的功能一样
LDA(K=10)  # K= 主题数量










"""  放到42行
# tfidf_model = models.TfidfModel(corpus)
        # with open(r'..\GoodRes\tfidf_' + names[i] + r'_1.txt', 'w', encoding='utf-8') as idftxt:  # 另外的文本，有中文，清晰一点
        #     for doc in tfidf_model[corpus]:
        #         a = []
        #         for j in range(len(doc)):
        #             l = (dict(dictionary.items())[doc[j][0]], doc[j][1])
        #             a.append(l)
        #         idftxt.write(a.__str__() + '\n')
"""
