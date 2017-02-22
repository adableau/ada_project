# -*- coding: UTF-8 -*-

'''
# Programmed by Aneesha Bakharia
'''

import csv
import os
import re

from numpy import *

import SurveyQuestionThemes as surveythemer
import nmf as nmf  # import non negative matrix factorization algorithm


def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def findthemes_backup(nothemes, wordlist, questionresponses, inc_articles, outputfile):
    #synonym_wordlists = wordlist.splitlines()

    stop_path = "englishstop.txt"
    stop_words = surveythemer.loadStopWords(stop_path)

    surveyQuestionResponse = []
    surveyQuestionResponseNID = []

    for response in questionresponses:
        newresp = remove_html_tags(response["text"])
        surveyQuestionResponse.append(newresp)
        surveyQuestionResponseNID.append(response["id"])
    #allwords:是所有的单词，itemwords：每一个文档中的单词统计
    listOfAllWords, listOfSurveyQuestionWords, listOfAllSurveyQuestionTitles, stemdictionary = surveythemer.getItemWords(
        surveyQuestionResponse, stop_words)
    wordMatrix, listOfWordsIncluded, fc, ic = surveythemer.createWordMatrix(listOfAllWords,
                                                                            listOfSurveyQuestionWords)
    pc = nothemes
    # size of input matrix
    ic = shape(wordMatrix)[0]
    fc = shape(wordMatrix)[1]
    # Random initialization
    w = array([[random.random() for j in range(pc)] for i in range(ic)])
    h = array([[random.random() for i in range(fc)] for i in range(pc)])
    weights, themes = nmf.nmf(wordMatrix, w, h, 0.001, 10, 500)
    themexml = surveythemer.display_themes(weights, themes, listOfWordsIncluded, surveyQuestionResponse, inc_articles,
                                           surveyQuestionResponseNID)

    f = open(outputfile, 'w')
    f.write(themexml)
    f.close()
    return


# 创建矩阵的方法
def createMatrix(questionresponses, part):
    # print questionresponses

    stop_path = "englishstop.txt"
    stop_words = surveythemer.loadStopWords(stop_path)

    surveyQuestionResponse = []
    surveyQuestionResponseNID = []

    for response in questionresponses:
        newresp = remove_html_tags(response["text"])
        # surveyQuestionResponse.append(newresp)
        surveyQuestionResponse.append(str(newresp))
        surveyQuestionResponseNID.append(response["id"])

    listOfAllWords, listOfSurveyQuestionWords = surveythemer.getItemWords(
        surveyQuestionResponse, stop_words)
    # 输出字典文件到本地目录。E:\LTN\PreprocessingDataInLTN\nmftoxml_matrix\data\all_WandWX

    # 得到词频小于10的list
    deletelist = []
    newlistofallwords = []
    for key in listOfAllWords:
        if (listOfAllWords[key] < 5):
            deletelist.append(key)
        else:
            newlistofallwords.append(key)
    listOfAllWords = newlistofallwords

    # 重新获得所有去除低词频的文本
    alldoclist = []
    for singlestr in surveyQuestionResponse:
        singlelist = singlestr.split(' ')
        linelist = []
        for word in singlelist:
            if (not word in deletelist):
                linelist.append(word)

        line = ' '.join(linelist).strip()
        alldoclist.append(line)
    surveyQuestionResponse = alldoclist

    # wordMatrix, listOfWordsIncluded, wordCount, fc, ic = surveythemer.createWordMatrix(listOfAllWords,
    #                                                                                  listOfSurveyQuestionWords, part)
    # 返回两个矩阵，是一个大矩阵的前一半，以及后一半。
    # listOfWordsIncluded 是所有词的向量
    # fc 是 cols的一半，也就是每个小矩阵的列数
    # ic是行数

    '''
    words_inItems_2 = []
    for singstr in words_inItems:
        for deleteword in deletewords:
            singstr=singstr.replace(' '+deleteword+' ',' ')
            words_inItems_2.append(singstr)

    words_inItems = words_inItems_2


     #输出到文件
    acpath = 'E:\\LTN\\PreprocessingDataInLTN\\nmftoxml_matrix\\data\\all_WandWX'
    listOfWordsIncludedpath = 'listOfWordsIncluded.txt'
    if (os.path.exists(acpath + '\\' + listOfWordsIncludedpath)):
        os.remove(acpath + '\\' + listOfWordsIncludedpath)

    listOfWordsIncludedfile = open(acpath + '\\' + listOfWordsIncludedpath, 'w')
    for singleword in listOfAllWords:
        listOfWordsIncludedfile.write(singleword)
        listOfWordsIncludedfile.write('\n')
    '''


    # wordMatrix1, wordMatrix2, listOfWordsIncluded, wordCount, fc, ic = surveythemer.createWordMatrix(listOfAllWords,
    #                                                                                                  surveyQuestionResponse, part)
    wordMatrix1, wordMatrix2, listOfWordsIncluded, wordCount, fc, ic = surveythemer.createWordMatrix(listOfAllWords,
                                                                                                     surveyQuestionResponse,
                                                                                                     part)

    return wordMatrix1, wordMatrix2, listOfWordsIncluded, surveyQuestionResponse, surveyQuestionResponseNID, wordCount, fc, ic


# def createMatrix_wordbag(questionresponses):



def findthemes(nothemes, questionresponses, inc_articles, outputfile1, outputfile2,
               outputsamefiledir1, outputsamefiledir2, outputdisfiledir1, outputdisfiledir2):
    # 得到矩阵1
    # 返回两个矩阵，是一个大矩阵的前一半，以及后一半。
    # 3.listOfWordsIncluded 是所有词的向量
    # fc 是 cols的一半，也就是每个小矩阵的列数
    # ic是行数
    # surveyQuestionResponse1是原始的文本以及nid1是原始的文本对应的序号。
    wordMatrix1, wordMatrix2, listOfWordsIncluded, surveyQuestionResponse, surveyQuestionResponseNID, wordCount, fc, ic = createMatrix(
        questionresponses, 1)

    nothemes = 10
    for maxiter in range(2000, 2100, 500):
        print "现在打印话题是：" + str(nothemes) + "迭代次数是：" + str(maxiter)

        # 得到矩阵2
        # wordMatrix2, listOfWordsIncluded2, surveyQuestionResponse2, surveyQuestionResponseNID2, wordCount2, fc2, ic2 = createMatrix(
        #    questionresponses, 2)

        # wordMatrix, listOfWordsIncluded, wordCount, fc, ic = surveythemer.createWordMatrix(listOfAllWords,
        #                                                                                   listOfSurveyQuestionWords)
        pc = nothemes
        # size of input matrix
        ic1 = shape(wordMatrix1)[0]
        fc1 = shape(wordMatrix1)[1]

        ic2 = shape(wordMatrix2)[0]
        fc2 = shape(wordMatrix2)[1]

        print(shape(wordMatrix1)[0], shape(wordMatrix1)[1])

        # Random initialization
        w1 = array([[random.random() for j in range(pc)] for i in range(ic1)])
        h1 = array([[random.random() for i in range(fc1)] for i in range(pc)])
        w2 = array([[random.random() for j in range(pc)] for i in range(ic2)])
        h2 = array([[random.random() for i in range(fc2)] for i in range(pc)])

        nmfresult = ""
        themes = ""
        # weights, themes = w,h
        # weights, themes = nmf.nmf(wordMatrix, w, h, 0.001, 10, 500) pc 是w的列的数目   tol, timelimit, maxiter,
        weights1, themes1, weights2, themes2, k = nmf.NMF_multiMatrix(wordMatrix1, wordMatrix2, w1, w2, h1, h2,
                                                                      0.000001, 2000, maxiter, pc)



if __name__ == '__main__':

    fileName = 'NewMatirx_combine4.csv'
    # fileName2 = 'file05_11.csv'
    directoryName = 'E:\\LTN\\PreprocessingDataInLTN\\nmftoxml_matrix'
    filepath = os.path.abspath(directoryName + '/' + fileName)
    nothemes = int(3)
    showdocs = int(1)
    outputfile1 = 'sample1.xml'
    outputfile2 = 'sample2.xml'
    outputsamefile1 = 'samesample1.xml'
    outputsamefile2 = 'samesample2.xml'

    outputdisfile1 = 'dissample1.xml'
    outputdisfile2 = 'dissample2.xml'

    outputfiledir1 = os.path.abspath(directoryName + '/data/' + outputfile1)
    outputfiledir2 = os.path.abspath(directoryName + '/data/' + outputfile2)

    outputsamefiledir1 = os.path.abspath(directoryName + '/data/' + outputsamefile1)
    outputsamefiledir2 = os.path.abspath(directoryName + '/data/' + outputsamefile2)

    outputdisfiledir1 = os.path.abspath(directoryName + '/data/' + outputdisfile1)
    outputdisfiledir2 = os.path.abspath(directoryName + '/data/' + outputdisfile2)

    data = csv.reader(open(filepath))

    questionresponses = []

    # Read the column names from the first line of the file
    fields = data.next()
    items = ""
    count = 1
    i = 0

    for row in data:
        # print count
        count = count + 1
        # Zip together the field names and values
        items = zip(fields, row)
        item = {}
        # Add the value to our dictionary
        for (name, value) in items:
            item[name] = value.strip()
        questionresponses.append(item)

    findthemes(nothemes, questionresponses, showdocs, outputfiledir1, outputfiledir2,
               outputsamefiledir1, outputsamefiledir2, outputdisfiledir1, outputdisfiledir2)
