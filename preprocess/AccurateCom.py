# -*-coding:utf-8-*-
# encoding: utf-8
__author__ = 'carson'
from numpy import *
import numpy as np
import os
from numpy.linalg import norm
from time import time
from sys import stdout

all_words_path = '../data/output_list/listOfWordsIncluded.txt'



def SIM1(x, y):
    if (len(x) != len(y)):
        print('error input,x and y is not in the same space')
        return;
    result1 = 0.0;
    result2 = 0.0;
    result3 = 0.0;
    for i in range(len(x)):
        result1 += x[i] * y[i]  # sum(X*Y)
        result2 += x[i] ** 2  # sum(X*X)
        result3 += y[i] ** 2  # sum(Y*Y)
    # print(result1)
    # print(result2)
    # print(result3)0
    result = (result1 / ((result2 * result3) ** 0.5))
    print result
    return result  # 结果显示


# x为行，y为列
def SIM(x, y):
    num = float(x * y)  # 若为行向量则 A * B.T
    denom = linalg.norm(x) * linalg.norm(y)
    cos = num / denom  # 余弦值
    sim = 0.5 + 0.5 * cos  # 归一化
    return sim


def readfiletoMatrix(path):
    data = []
    for l in open(path):
        row = [float(x) for x in l.split()]
        data.append(row)
    return data


# 计算q在全部的词中的投影。
def calculateQMatrix(wordpath, qfilepath):
    contentList = []
    qwordsList = []
    allwordsfile = open(wordpath)
    # contents = str(file.readlines()).strip().split('  ')
    # contents = str(allwordsfile.readlines()).strip()
    for wordline in open(wordpath):
        if wordline.split():
            contentList.append(wordline.strip().replace('\n', ''))

    # for qwordline in open(qfilepath):
    #    qwordsList.append(qwordline.strip().replace('\n', ''))

    qwordsList = ''.join(open(qfilepath).readlines()).strip().split(' ')
    wordmatrix = []
    count1 = 0
    for word in contentList:
        if (word in qwordsList):
            wordcount = qwordsList.count(word)
            wordmatrix.append(wordcount)
            count1 = count1 + 1
        else:
            wordmatrix.append(0)
    # print 'the matrix q contain:--' + str(count1) + '--number of one'
    return np.mat(wordmatrix)


# 求出结果的余弦函数平均值，然后找到最大的，返回时属于哪一类。k类中属于第几类。
def caulateAvgMax(catefolderNum, result):
    # 所有的平均数
    avgList = []
    # 一个类别里面有多少列。
    tag = len(result) / catefolderNum
    # 处在第几个类别下面
    cate = 0
    i = 0
    allresult = 0
    catetag = 0
    while (True):
        if catetag == catefolderNum:
            break
        if i < tag:
            if math.isnan(result[i + cate]):
                result[i + cate] = 0
            allresult += result[i + cate]
            i = i + 1
            #print "循环了"+str(i) +" 次，allresult结果是："+ str(allresult)
        else:
            avgList.append(allresult / tag)
            allresult = 0
            i = 0
            cate += tag
            catetag = catetag + 1


    maxnum = max(avgList)
    postion = avgList.index(maxnum)

    return max, postion


def AccurateCom():
    # 读取矩阵B'X矩阵
    # 这个是k*n的


    T_B_X1path = ('../data/output_list/bx1.txt')
    T_B_X2path = ('../data/output_list/bx2.txt')
    # print 'shape is:' + str(shape(T_B_HMatrix)[0]) + '----' + str(shape(T_B_HMatrix)[1])
    # 读取B'矩阵
    # 这是k*m的
    B1path = ('../data/output_list/b1.txt')
    B2path = ('../data/output_list/b2.txt')

    # T_BMatrix = BMatrix.T
    # print 'shape is:' + str(shape(BMatrix)[0]) + '----' + str(shape(BMatrix)[1])
    # 读取q矩阵，也就是测试集下面判断分类是否正确的。
    # 这个是1*m的
    testPath = '../data/output_list/20newsgroups_sampleComtest_4'

    # k*n
    T_B_X1Matrix = np.mat(readfiletoMatrix(T_B_X1path))
    T_B_X2Matrix = np.mat(readfiletoMatrix(T_B_X2path))
    B1Matrix = np.mat(readfiletoMatrix(B1path))
    B2Matrix = np.mat(readfiletoMatrix(B2path))

    # test下面的所有的类别文件夹目录
    catedirs = os.listdir(testPath)
    cateNum = len(os.listdir(testPath))
    # 循环读取每个文件夹
    errorcount = 0
    allcount = 0
    for catesingle in catedirs:
        # 拿到每个文件夹下的文件
        eachfiles = os.listdir(testPath + '\\' + catesingle)
        for singlefile in eachfiles:
            allcount = allcount + 1
            q_path = (testPath + '\\' + catesingle + '\\' + singlefile)
            # 得到q在所有文档中的投影。
            q_Matrix = calculateQMatrix(all_words_path, q_path)

            # 获取这个文本q的类别。
            cateinfo = q_path.split('\\')[-2]
            txtinfo = q_path.split('\\')[-1]

            # print 'q_Matrix shape is:' + str(shape(q_Matrix)[0]) + '----' + str(shape(q_Matrix)[1])
            # print 'T_BMatrix shape is:' + str(shape(BMatrix)[0]) + '----' + str(shape(BMatrix)[1])

            # 得到规范后的q_B
            q_BMatrix = dot(q_Matrix, B1Matrix)
            # print 'shape is:' + str(shape(q_BMatrix)[0]) + '----' + str(shape(q_BMatrix)[1])
            # 计算相似度了，q_B和T_BMatrix的余弦距离,计算每一列的距离，然后根据类别，比如5类，那就统计这个5类中的评价值
            result = []
            for i in range(shape(T_B_X1Matrix)[1]):
                # 这样统计的就是所有的列的相似度的值。
                result.append(SIM(q_BMatrix, T_B_X1Matrix[:, i]))

            # 统计一个平均值,返回的有兩個，第一个是距离最近的值，第二个是类别，也就是所属的位置
            max, position = caulateAvgMax(cateNum, result)
            cateposition = getPosition(position)

            if (cateposition == cateinfo):
                print (cateinfo + '\\' + txtinfo + '在W1中被划分正确')
            else:
                print (cateinfo + '\\' + txtinfo + '在W1中被划分错误,应该属于' + cateinfo + '但是划成了' + cateposition)
                # errorcount = errorcount + 1
                # 得到规范后的q_B
                q_BMatrix = dot(q_Matrix, B2Matrix)
                # print 'shape is:' + str(shape(q_BMatrix)[0]) + '----' + str(shape(q_BMatrix)[1])
                # 计算相似度了，q_B和T_BMatrix的余弦距离,计算每一列的距离，然后根据类别，比如5类，那就统计这个5类中的评价值
                result2 = []
                for i in range(shape(T_B_X2Matrix)[1]):
                    # 这样统计的就是所有的列的相似度的值。
                    result2.append(SIM(q_BMatrix, T_B_X2Matrix[:, i]))

                # 统计一个平均值,返回的有兩個，第一个是距离最近的值，第二个是类别，也就是所属的位置
                max, position = caulateAvgMax(cateNum, result2)
                cateposition, errorcount = countdata(cateinfo, cateposition, errorcount, position, txtinfo)
    acrate = (allcount - errorcount) / float(allcount)
    acrate = round(acrate * 100, 3)
    print 'allcount:' + str(allcount) + '--errorcount is:' + str(errorcount)
    print '正确率是：' + str(acrate)


def getPosition(position):
    if position == 0:
        cateposition = '1_comp'
    if position == 1:
        cateposition = '2_rec'
    if position == 2:
        cateposition = '3_sci'
    if position == 3:
        cateposition = '4_talk'
    if position == 4:
        cateposition = 'comp.sys.mac.hardware'
    if position == 5:
        cateposition = 'comp.windows.x'
    if position == 6:
        cateposition = 'misc.forsale'
    if position == 7:
        cateposition = 'rec.autos'
    if position == 8:
        cateposition = 'rec.motorcycles'
    if position == 9:
        cateposition = 'rec.sport.baseball'
    if position == 10:
        cateposition = 'rec.sport.hockey'
    if position == 11:
        cateposition = 'sci.crypt'
    if position == 12:
        cateposition = 'sci.electronics'
    if position == 13:
        cateposition = 'sci.med'
    if position == 14:
        cateposition = 'sci.space'
    if position == 15:
        cateposition = 'soc.religion.christian'
    if position == 16:
        cateposition = 'talk.politics.guns'
    if position == 17:
        cateposition = 'talk.politics.guns'
    if position == 18:
        cateposition = 'talk.politics.misc'
    if position == 19:
        cateposition = 'talk.religion.misc'
    return cateposition


def countdata(cateinfo, cateposition, errorcount, position, txtinfo):
    cateposition =getPosition(position)
    if (cateposition == cateinfo):
        print (cateinfo + '\\' + txtinfo + '在W2中被划分正确')
    else:
        print (cateinfo + '\\' + txtinfo + '在W2中被划分错误,应该属于' + cateinfo + '但是划成了' + cateposition)
        errorcount = errorcount + 1
    return cateposition, errorcount


if __name__ == '__main__':
    # calculateQMatrix(allwordspath,
    #                 'F:\\_Paper_Expri\\20newsgroups_sampleTest\\1comp.graphics\\chuli37915.txt')
    AccurateCom()
