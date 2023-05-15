# coding:utf-8
# 根据好评率画图
import pandas as pd
import matplotlib.pyplot as plt
import xlrd
xlsx = '..\mafengwo\\spiders\\NanjingHao.xlsx'
workbook = xlrd.open_workbook(xlsx)
sheet1 = workbook.sheet_by_index(0)  # 第一个工作簿
print(sheet1.nrows)
NJList = {}      # 字典不可用下标索引,而是通过Key检索Value
for i in range(1, sheet1.nrows):              # 第一行不要
    if sheet1.cell(i, 0).value != "":         # 不为空值，我的excel文件只对风景名字记录一次，文件内容均为str
        place_name = sheet1.cell(i, 0).value  # 风景名字
        recommend = int(str(sheet1.cell(i, 1).value).strip("%"))   # 推荐指数
        NJList[place_name] = recommend
print(NJList)
print(len(NJList))
# 正确显示中文
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 画图，plt.bar()可以画柱状图
plt.ylim(30, 100)     # 设置y轴刻度范围
plt.title("南京热门景点推荐指数")  # 设置图片名称
# plt.xlabel("景点名称")  # 设置x轴标签名 设置之后有点难看
plt.ylabel("网友推荐度(%)")  # 设置y轴标签名
for k, v in NJList.items():
    print(k, v)
    plt.bar(k, v, color="steelblue")
    plt.text(k, v+0.1, str(v)+"%", ha='center', fontsize=10)
plt.xticks(rotation=-35, fontsize=8, ha='left')  # 调整x轴坐标
plt.gcf().subplots_adjust(bottom=0.3)
plt.savefig('好评率', dpi=1500)  # 得放在下面一句之前
# 显示
plt.show()

