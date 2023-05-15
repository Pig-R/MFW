# coding=utf-8
from gensim import corpora, models, similarities
# 这里生成两个词频文件
names = ['总统府', '中山陵', '纪念馆', '钟山-明孝陵', '夫子庙-秦淮河', '博物院', '玄武湖', '鸡鸣寺']
# 打印模型参数：文档数量与语料库单词数
# print(tfidf_model)
# with open('dict_ZTF.txt', 'a', encoding='utf-8')as f1:
#     f1.write(str(dictionary.token2id))               # 保存dictionary
# 存储通过tfidf转化过的文档，痛过TFIDF转化后每个文档都被表征成在词与权重的大小，

for i in range(len(names)):
    train = []
    # 将分完词的文档加载成符合gensim文格式的输入
    with open(names[i] + r'.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            # print(line)
            line = [word.strip() for word in line.split()]
            train.append(line)
    # 构造词典
    dictionary = corpora.Dictionary(train)
    dictionary.save(r'..\datadict\tfidf_' + names[i] + '.txt')  # 保存词典
    # print(dictionary.token2id)  # 给每个分词一个编号
    """基于词典，将【分词列表集】转换成【向量集】，形成【语料库】
    BoW使用一组无序的单词(words)来表达一段文字或一个文档。近年来，BoW模型被广泛应用于计算机视觉中。
    该向量与原来文本中单词出现的顺序没有关系，而是词典中每个单词在文本中出现的频率。
    corpus是一个元组嵌套列表，表示了每个文本中词语对应的id及词频。"""
    corpus = [dictionary.doc2bow(text) for text in train]
    tfidf_model = models.TfidfModel(corpus)
    with open(r'..\TFIDF\tfidf_'+names[i]+r'.txt', 'w', encoding='utf-8') as fr1:  # 版本1只有ID号#
        for doc in tfidf_model[corpus]:
            fr1.write(doc.__str__() + '\n')
    # 版本2
    with open(r'..\TFIDF\tfidf_'+names[i]+r'_1.txt', 'w', encoding='utf-8') as fr2:  # 另外的文本，有中文，清晰一点
        for doc in tfidf_model[corpus]:
            a = []
            for i in range(len(doc)):
                # print(dict(dictionary.items())[doc[i][0]], doc[i][1])
                l = (dict(dictionary.items())[doc[i][0]], doc[i][1])
                a.append(l)
            fr2.write(a.__str__() + '\n')















# ('dic.dict')  # 乱码。？保存起来以后用到
# print(corpus[0])  # 结果：一句话(词汇编号，出现次数)
# print(dictionary)
# 使用【TF-IDF模型】处理语料库





#  一行一行读，
# # print(len(train))  # 100
# # print(len(train[0]))  # 第一条数据，145个词汇
# nums = 0
# for i in range(100):
#     print(len(train[i]))
#     nums += len(train[i])
# print(nums)  # 4181个



# print(dictionary)
# feature_cnt = len(dictionary.token2id)  # 词典中词的数量
# print(feature_cnt)
# # dictionary.save('ZTFdict.txt')  # 保存生成的词典,用于以后加载 里面是乱码，未解决