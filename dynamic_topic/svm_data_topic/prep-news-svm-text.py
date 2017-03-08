#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Tool to pre-process documents contained one or more directories, and export a document-term matrix for each directory.

1.将数据合成一个大文本,构建矩阵X，类别Y
    类别：word
    X 类别：TF-IDF
2.使用NMF得到 doc-topic 文件
3.合并类别和doc-topic文件
4.分类，计算准确率
5.换其它NMF
6.换数据集

"""

import numpy


# --------------------------------------------------------------
def svm_read_problem(data_file_name):
    """
    svm_read_problem(data_file_name) -> [y, x]

    Read LIBSVM-format data from data_file_name and return labels y
    and data instances x.
    """
    prob_y = []
    prob_x = []
    for line in open(data_file_name):
        line = line.split(None, 1)
        # In case an instance with all zero features
        if len(line) == 1: line += ['']
        label, features = line
        xi = {}
        for e in features.split():
            ind, val = e.split(":")
            xi[int(ind)] = float(val)
        prob_y += [float(label)]
        prob_x += [xi]
    return (prob_y, prob_x)


############################################################################
def main():
    """
        处理为libsvm格式的数据
        按年将数据分开
    """
    news_txt = 'news.txt'
    # 将TXT转为矩阵,X为20组新闻tf-idf矩阵,保存，进行NMF分析；y为分类结果
    y, x = svm_read_problem(news_txt)
    print "----save----model---------------"
    numpy.savetxt(news_txt + "_tfidf.txt", x)
    print "----finished-------"


# --------------------------------------------------------------

if __name__ == "__main__":
    main()
