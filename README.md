# MFW
1.爬虫文件在mafengwo文件夹下。Nanjing.xlsx文件是爬取的全部评论，NanjingHao是好评,NanjingHuai是差评。
2.BadRes是保存分析差评的结果。tfidf_景区名字_dict.txt是按行拆分每一个词汇的文件，方便后续读入词汇。
3.ciyunImg是保存分析全部评论的词云图。
4.dataprocess里面有进行评论分析的各个可执行文件。
5.GoodRes保存好评+差评的分词结果及TFIDF词频字典。
6.LDAoutput保存LDA实验时不同主题个数输出的结果
7.TFIDF保存保存分别分析八个景点全部评论的TFIDF词频，tfidf_景区名字.txt是词汇编号+分数，tfidf_景区名字_1.txt是词汇中文对应起来+分数。