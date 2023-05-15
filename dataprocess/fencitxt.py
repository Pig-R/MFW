# coding=utf-8
# 将八个景点分词结果以txt文件形式保存
import jieba, re
from gensim import corpora, models, similarities
import emoji
import xlrd
from snownlp import SnowNLP
xlsx_path = "..\mafengwo\\spiders\\Nanjing.xlsx"
workbook = xlrd.open_workbook(xlsx_path, 'utf-8')
sheet1 = workbook.sheet_by_index(0)  # 第一个工作簿
nextone = 100 #  每个景点一百条评论
# 去除原始字符串中的url
def remove_urls(raw_sentence):
    # 正则表达式
    url_reg = r'[a-z,A-Z]+'
    result = re.sub(url_reg, '', raw_sentence)  # 去url,字母
    result = re.sub(r'[\',、：…“（）...\\xa0]', '', result)  # 去符号
    result = re.sub('(:.+?:)', '', emoji.demojize(result))   # 去表情
    result = re.sub(r'\d+', '', result)   # 去数字
    snow = SnowNLP(result)
    result = snow.han  # 繁转简，review_text是文本处理后的最终结果
    return result


# 创建停用词表
def stopwordslist():
    stopwords = [line.strip() for line in open('SCUstopwprd.txt', encoding='UTF-8').readlines()]
    return stopwords


# 利用jieba分词对文档进行中文分词
def seg_depart(raw_sentence):
    sentence_depart = jieba.cut(raw_sentence.strip())
    stopwords = stopwordslist()
    outstr = ''
    for word in sentence_depart:
        if word not in stopwords:
            outstr += word
            outstr += " "
    return outstr

def writetxt():
    # 下面的函数其实可以简化，递归调用自己，该方法在对差评做分词的时候（badreviews.py）有改进
    for i in range(1, sheet1.nrows):    # txt分别保存每个景点评论的分词
        sentence = remove_urls(sheet1.cell(i, 2).value)
        words = seg_depart(sentence)
        if 1 <= i <= nextone:   # 简化链式
            ZTFtxt = open('总统府.txt', mode='a+', encoding='utf-8')
            ZTFtxt.write(words + '\n')  # \n 换行符
        elif nextone < i <= 2 * nextone:
            ZSLtxt = open('中山陵.txt', mode='a+', encoding='utf-8')
            ZSLtxt.write(words + '\n')
        elif 2 * nextone < i <= 3 * nextone:
            JNGtxt = open('纪念馆.txt', mode='a+', encoding='utf-8')
            JNGtxt.write(words + '\n')
        elif 3 * nextone < i <= 4 * nextone:
            ZSMXLtxt = open('钟山-明孝陵.txt', mode='a+', encoding='utf-8')
            ZSMXLtxt.write(words + '\n')
        elif 4 * nextone < i <= 5 * nextone:
            FZMtxt = open('夫子庙-秦淮河.txt', mode='a+', encoding='utf-8')
            FZMtxt.write(words + '\n')
        elif 5 * nextone < i <= 6 * nextone:
            BWYtxt = open('博物院.txt', mode='a+', encoding='utf-8')
            BWYtxt.write(words + '\n')
        elif 6 * nextone < i <= 7 * nextone:
            XWHtxt = open('玄武湖.txt', mode='a+', encoding='utf-8')
            XWHtxt.write(words + '\n')
        else:
            JMStxt = open('鸡鸣寺.txt', mode='a+', encoding='utf-8')
            JMStxt.write(words + '\n')


# writetxt()  # 运行这个文件的时候在打开，不然启动其他文件会连着一起运行




# sentence = remove_urls(sheet1.cell(542, 2).value)
# words = seg_depart(sentence)
# print(words)