# -*- coding: utf-8 -*-
# 存到excel排序
import openpyxl
names = ['总统府', '中山陵', '纪念馆', '钟山-明孝陵', '夫子庙-秦淮河', '博物院', '玄武湖', '鸡鸣寺']
# 全部评论
workbook = openpyxl.Workbook()  # 创建一个Workbook对象
for i in range(len(names)):  # (2, 3)
    j = 1
    sheet = workbook.create_sheet(index=i, title=names[i])
    dict_path = r'..\datadict\tfidf_'+names[i]+r'_dict.txt'
    # 首先生成一个字典dict_view,如果碰到重复的关键词，放TFIDF值大的那个进去
    dict_f = open(dict_path, 'r', encoding='utf-8')
    dict_view = {}
    for line in dict_f:
        v = line.replace("'", '').strip().split(', ')  # ['一家', '0.07577536430126272'] len:2
        v[1] = float(v[1])
        if v[0] not in dict_view:
            dict_view[v[0]] = v[1]
        else:
            dict_view[v[0]] = max(dict_view[v[0]], v[1])
    for dic in dict_view:
        sheet['A' + str(j)] = dic
        sheet['B' + str(j)] = dict_view[dic]
        j += 1
    dict_f.close()
workbook.save("南京TFIDF.xlsx")



# dict = {'B':'A','321':'2'}
# for d in dict:
#     print(d,dict[d])
