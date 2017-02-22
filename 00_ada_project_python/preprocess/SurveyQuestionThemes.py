# -*- coding: UTF-8 -*-
'''
# Programmed by Aneesha Bakharia
'''

import re  # import regular expression module
from xml.dom.minidom import Document

from numpy import *  # import numpy for matrix & array features
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from util import porter


##
# A collection of functions for using Non Negative Matrix Factorization to find themes in open ended survey questions

##
# Utility function to return a list of all words that are have a length greater than a specified number of characters.
# @param text The text that must be split in to words.
# @param minWordReturnSize The minimum no of characters a word must have to be included.
def separatewords(text, minWordReturnSize):
    # splitter=re.compile('\\W*')
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-]')
    return [singleWord.lower() for singleWord in splitter.split(text) if len(singleWord) > minWordReturnSize]


##
# Utility function to sort a dictionary by Value in decending order
# Not the most efficient implementation - may need to refactor if speed becomes an issue
# @param dictionary The dictionary data structure.
# @return list A list of keys sorted by their value.
def sortDictionaryByValues(dictionary):
    """ Returns the keys of dictionary d sorted by their values """
    items = dictionary.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort()
    backitems.reverse()
    return [backitems[i][1] for i in range(0, len(backitems))]


##
# Utility function to load stop words from a file and return as a list of words
# @param stopWordFile Path and file name of a file containing stop words.
# @return list A list of stop words.
def loadStopWords(stopWordFile):
    stopWords = []
    for line in open(stopWordFile):
        for word in line.split():  # in case more than one per line
            stopWords.append(word)
    return stopWords


##
# Utility function to remove stop words that are present in a list of words
# @param wordlist Unfiltered list of words
# @param stopwordlist List of stops words
# @return list Filtered list of words
def removeStopWords(wordlist, stopwordlist):
    return [word for word in wordlist if word not in stopwordlist]


##
# This function returns a list of all words that are have a length greater than a specified number of characters.
# @param text The text that must be split in to words.
# @param minWordReturnSize The minimum no of characters a word must have to be included.
def getItemWords(list_of_words, stop_words):
    stemmer = porter.PorterStemmer()
    allwords = {}
    itemwords = []
    itemtitles = []
    ec = 0
    stemlist = {}
    # Loop over every item in list_of_words
    for item in list_of_words:
        words = separatewords(item, 1)
        words = removeStopWords(words, stop_words)
        itemwords.append({})
        itemtitles.append("Response " + str(ec + 1))
        # Increase the counts for this word in allwords and in articlewords
        for word in words:
            unstemmedword = word
            # word = stemmer.stem(word, 0, len(word) - 1)
            if word in stemlist:
                temp = stemlist[word]
                try:
                    temp.index(unstemmedword)
                except ValueError:
                    temp.append(unstemmedword)
                    stemlist[word] = temp
            else:
                temp = []
                temp.append(unstemmedword)
                stemlist[word] = temp
            allwords.setdefault(word, 0)
            allwords[word] += 1
            itemwords[ec].setdefault(word, 0)
            itemwords[ec][word] += 1
        ec += 1
    # allwords:是所有的单词，itemwords：每一个文档中的单词统计。itemtitles：是多少列；
    return allwords, itemwords


##
# Returns the document (row) and words (columns) matrix and the list of words as a vector
# all_words 是所有的词，words_initems是每一个文档的词的矩阵
def createWordMatrix(all_words, words_inItems, part):
    # print all_words
    # print words_inItems
    wordvector = []
    deletewords = []
    # Only take words that are common but not too common

    # if c<len(words_inItems)*0.6: #*0.2
    # Create the word matrix
    # cols = len(wordvector)
    # rows = len(words_inItems)

    '''
    words_inItems_2test = []
    words_inItemstest = ['1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4']
    deletewordstest = ['1','3']
    for singstr in words_inItemstest:
        for deleteword in deletewordstest:
            singstr=singstr.replace(' '+deleteword+' ',' ')
            words_inItems_2test.append(singstr)
    '''

    wrd = 'action'
    f = 'action'
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    # print vectorizer.fit_transform(words_inItems)
    tfidf = transformer.fit_transform(vectorizer.fit_transform(words_inItems))
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    wordvector = word
    count = 0
    '''
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print (u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            if  not weight[i][j] == 0.0:
                count = count +1
                print word[j], weight[i][j],count
    '''
    # 输出到文件
    acpath = 'E:\\LTN\\PreprocessingDataInLTN\\nmftoxml_matrix\\data\\all_WandWX'
    # listOfWordsIncludedpath = 'listOfWordsIncluded.txt'
    # if (os.path.exists(acpath + '\\' + listOfWordsIncludedpath)):
    #    os.remove(acpath + '\\' + listOfWordsIncludedpath)

    # listOfWordsIncludedfile = open(acpath + '\\' + listOfWordsIncludedpath, 'w')
    # for singleword in wordvector:
    #   listOfWordsIncludedfile.write(singleword)
    #    listOfWordsIncludedfile.write('\n')




    wordMatrix = array(weight.T)

    rows = len(word)
    cols = len(words_inItems)
    sum = 0
    wordCount = []
    wordMatrix1 = wordMatrix[:, 0:cols / 2]
    print str(shape(wordMatrix1)) + '---' + str(shape(wordMatrix))
    wordMatrix2 = wordMatrix[:, cols / 2:cols]
    return wordMatrix1, wordMatrix2, wordvector, wordCount, cols / 2, rows


# 暂时不用
def createNewMatrix(all_words, words_inItems):
    # print all_words
    # print words_inItems
    wordvector = []
    # Only take words that are common but not too common
    for w, c in all_words.items():
        wordvector.append(w)
        # if c<len(words_inItems)*0.6: #*0.2
    # Create the word matrix
    rows = len(wordvector)
    cols = len(words_inItems)
    wrd = 'action'
    f = 'action'
    # 就是根据原来的f中的每一行的值来判断，根据是不是出现，没有tfidf。
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(words_inItems))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    wordvector = word
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print (u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            print word[j], weight[i][j]
    l1 = [[(wrd in f and weight or 0) for wrd in wordvector] for f in words_inItems]

    wordMatrix = array(l1)
    wordMatrix = wordMatrix.T
    print shape(wordMatrix)
    wordCount = []
    sum = 0
    for c in range(0, cols):
        for r in range(0, rows):
            sum += wordMatrix[r][c]
        wordCount.append(sum)
        sum = 0
    return wordMatrix, wordvector, wordCount, cols, rows


# 用word2vec创建矩阵
def createWordMatrix_w2v(all_words, words_inItems, questionresponses):
    # print all_words
    # print words_inItems
    wordvector = []
    # Only take words that are common but not too common
    for w, c in all_words.items():
        wordvector.append(w)
        # if c<len(words_inItems)*0.6: #*0.2
    # Create the word matrix
    cols = len(wordvector)
    rows = len(words_inItems)
    wrd = 'action'
    f = 'action'
    # 就是根据原来的f中的每一行的值来判断，根据是不是出现，没有tfidf。
    l1 = [[(wrd in f and f[wrd] or 0) for wrd in wordvector] for f in words_inItems]

    # model_vec = word2vec.Word2Vec.load_word2vec_format(
    #    'E:\\_Research Direction\\GoogleNews-vectors-negative300.bin\\vectors.bin', binary=True)
    # model_vec.
    # 在这地方，用word2vec来做矩阵处理。得到最后的矩阵。
    wordMatrix = array(l1)
    wordCount = []
    sum = 0
    for c in range(0, cols):
        for r in range(0, rows):
            sum += wordMatrix[r][c]
        wordCount.append(sum)
        sum = 0
    return wordMatrix, wordvector, wordCount, cols, rows


##
# Display themes, top six words in a theme and associated documents in theme.
# weights, themes = w,h
def display_themes(weights_matrix, themes_matrix, list_Of_Included_Words, item_Titles,
                   inc_articles, surveyQuestionResponseNID):
    # Data structures for Graph Representation
    ThemeDictionary = {}
    DocDictionary = {}
    TermDictionary = {}
    # Data structures to represent relationships
    DocInTheme = {}
    TermInTheme = {}
    # Start of NMF interpretation ,the shape of the h is (2,34)
    norows, nocols = shape(themes_matrix)
    # w is the (9,2)
    noarticles, nofeatures = shape(weights_matrix)
    d1 = {}
    count = 1
    theme_html = ""
    themes_html = ""
    # setup XML structure
    # Create the minidom document
    doc = Document()
    # Create the <themes> base element
    themes_xml = doc.createElement("themes")
    doc.appendChild(themes_xml)

    for row in range(norows):
        theme_html = ""
        # Create the main <theme> element
        theme_xml = doc.createElement("theme")
        theme_xml.setAttribute("id", str(count))
        theme_xml.setAttribute("title", "Theme " + str(count))
        themes_xml.appendChild(theme_xml)

        ThemeDictionary["T" + str(count)] = "Theme " + str(count)

        # Create a <words> element
        words_xml = doc.createElement("words")
        theme_xml.appendChild(words_xml)

        for col in range(nocols):
            # h
            d1[list_Of_Included_Words[col]] = themes_matrix[row, col]
        themes_list_in_order = sortDictionaryByValues(d1)
        for it in themes_list_in_order[0:50]:
            word_index = list_Of_Included_Words.index(it)
            # TermDictionary[it] = stemdictionary[it]
            TermInTheme["T" + str(count) + "_" + it] = str("%.2f" % d1[it])

            word_xml = doc.createElement("word")
            word_xml.setAttribute("weight", str(d1[it]))
            wordtext_xml = doc.createTextNode(it)
            word_xml.appendChild(wordtext_xml)
            words_xml.appendChild(word_xml)

        theme_html = theme_html + "</p>"
        if (inc_articles == 1):
            # Print articles/items/survey responses that map to Theme/Feature
            articlesInTheme = {}
            articleweights = []
            article_row = 0
            for article in surveyQuestionResponseNID:
                # if (weights_matrix[article, row] > 0.008):
                articlesInTheme[article] = weights_matrix[article_row, row]
                articleweights.append(weights_matrix[article_row, row])
                DocDictionary["D" + str(article)] = "Doc" + str(article)
                DocInTheme["T" + str(count) + "_D" + str(article)] = str("%.2f" % weights_matrix[article_row, row])
                article_row = article_row + 1
                # else:
                # Capture all non attached documents
                # DocDictionary["D" + str(article)] = "Doc" + str(article)
            # max_weight_val = max(articleweights)
            # min_weight_val = min(articleweights)

            articles_In_Theme_Order = sortDictionaryByValues(articlesInTheme)

            # Create a <responses> element
            reponses_xml = doc.createElement("responses")
            theme_xml.appendChild(reponses_xml)

            for article_no in articles_In_Theme_Order:
                response_xml = doc.createElement("response")
                print 'article_no:' + str(article_no)
                print 'surveyQuestionResponseNIDLength:+' + str(len(surveyQuestionResponseNID))
                # response_xml.setAttribute("id", str(surveyQuestionResponseNID[article_no]))

                response_xml.setAttribute("id", article_no)
                response_xml.setAttribute("weight", str(("%.2f" % weights_matrix[surveyQuestionResponseNID.index(article_no), row])))

                responsetext_xml = doc.createTextNode(item_Titles[surveyQuestionResponseNID.index(article_no)])
                response_xml.appendChild(responsetext_xml)

                #zzreponses_xml.appendChild(response_xml)

            # Create Rendered element
            rendered_xml = doc.createElement("rendered")
            theme_xml.appendChild(rendered_xml)

        count = count + 1
    return doc.toprettyxml(indent="  ")


# weights 是w，themes_matrix是h
def display_SameDis_themes(weights_matrix, themes_matrix, start, k, list_Of_Included_Words, item_Titles,
                           inc_articles, surveyQuestionResponseNID):
    # Data structures for Graph Representation
    ThemeDictionary = {}
    DocDictionary = {}
    TermDictionary = {}
    # Data structures to represent relationships
    DocInTheme = {}
    TermInTheme = {}
    # Start of NMF interpretation ,the shape of the h is (2,34)
    norows, nocols = shape(themes_matrix)
    # w is the (9,2)
    noarticles, nofeatures = shape(weights_matrix)
    d1 = {}
    count = 1
    theme_html = ""
    themes_html = ""
    # setup XML structure
    # Create the minidom document
    doc = Document()
    # Create the <themes> base element
    themes_xml = doc.createElement("themes")
    doc.appendChild(themes_xml)

    for row in range(norows):
        theme_html = ""
        # Create the main <theme> element
        theme_xml = doc.createElement("theme")
        theme_xml.setAttribute("id", str(count))
        theme_xml.setAttribute("title", "Theme " + str(count))
        themes_xml.appendChild(theme_xml)

        ThemeDictionary["T" + str(count)] = "Theme " + str(count)

        # Create a <words> element
        words_xml = doc.createElement("words")
        theme_xml.appendChild(words_xml)

        # 应该就从这个地方开始修改，col是H矩阵的，row是行，所以应该修改col，不要修改row，col从1到k。
        # 最后应该得到一个row*k的矩阵。
        # for col in range(nocols):
        for col in range(start, k, 1):
            d1[list_Of_Included_Words[col]] = themes_matrix[row, col]
        themes_list_in_order = sortDictionaryByValues(d1)
        for it in themes_list_in_order[0:40]:
            word_index = list_Of_Included_Words.index(it)
            # TermDictionary[it] = stemdictionary[it]
            TermInTheme["T" + str(count) + "_" + it] = str("%.2f" % d1[it])

            word_xml = doc.createElement("word")
            word_xml.setAttribute("weight", str(d1[it]))
            wordtext_xml = doc.createTextNode(it)
            word_xml.appendChild(wordtext_xml)
            words_xml.appendChild(word_xml)

        theme_html = theme_html + "</p>"
        if (inc_articles == 1):
            # Print articles/items/survey responses that map to Theme/Feature
            articlesInTheme = {}
            articleweights = []
            for article in range(noarticles):
                if (weights_matrix[article, row] > 0.008):
                    articlesInTheme[article] = weights_matrix[article, row]
                    articleweights.append(weights_matrix[article, row])
                    DocDictionary["D" + str(article)] = "Doc" + str(article)
                    DocInTheme["T" + str(count) + "_D" + str(article)] = str("%.2f" % weights_matrix[article, row])
                else:
                    # Capture all non attached documents
                    DocDictionary["D" + str(article)] = "Doc" + str(article)
            # max_weight_val = max(articleweights)
            # min_weight_val = min(articleweights)

            articles_In_Theme_Order = sortDictionaryByValues(articlesInTheme)

            # Create a <responses> element
            reponses_xml = doc.createElement("responses")
            theme_xml.appendChild(reponses_xml)

            for article_no in articles_In_Theme_Order:
                response_xml = doc.createElement("response")
                response_xml.setAttribute("id", str(surveyQuestionResponseNID[article_no]))
                response_xml.setAttribute("weight", str(("%.2f" % weights_matrix[article_no, row])))

                responsetext_xml = doc.createTextNode(item_Titles[article_no])
                response_xml.appendChild(responsetext_xml)

                reponses_xml.appendChild(response_xml)

            # Create Rendered element
            rendered_xml = doc.createElement("rendered")
            theme_xml.appendChild(rendered_xml)

        count = count + 1
    return doc.toprettyxml(indent="  ")


# weights 是w，themes_matrix是h
def display_Dis_themes(weights_matrix, themes_matrix, k, list_Of_Included_Words, item_Titles,
                       inc_articles, surveyQuestionResponseNID):
    # Data structures for Graph Representation
    ThemeDictionary = {}
    DocDictionary = {}
    TermDictionary = {}
    # Data structures to represent relationships
    DocInTheme = {}
    TermInTheme = {}
    # Start of NMF interpretation ,the shape of the h is (2,34)
    norows, nocols = shape(themes_matrix)
    # w is the (9,2)
    noarticles, nofeatures = shape(weights_matrix)
    d1 = {}
    count = 1
    theme_html = ""
    themes_html = ""
    # setup XML structure
    # Create the minidom document
    doc = Document()
    # Create the <themes> base element
    themes_xml = doc.createElement("themes")
    doc.appendChild(themes_xml)

    for row in range(norows):
        theme_html = ""
        # Create the main <theme> element
        theme_xml = doc.createElement("theme")
        theme_xml.setAttribute("id", str(count))
        theme_xml.setAttribute("title", "Theme " + str(count))
        themes_xml.appendChild(theme_xml)

        ThemeDictionary["T" + str(count)] = "Theme " + str(count)

        # Create a <words> element
        words_xml = doc.createElement("words")
        theme_xml.appendChild(words_xml)

        # 应该就从这个地方开始修改，col是H矩阵的，row是行，所以应该修改col，不要修改row，col从1到k。
        # 最后应该得到一个row*k的矩阵。
        # for col in range(nocols):
        for col in range(k + 1, col):
            d1[list_Of_Included_Words[col]] = themes_matrix[row, col]
        themes_list_in_order = sortDictionaryByValues(d1)
        for it in themes_list_in_order[0:30]:
            word_index = list_Of_Included_Words.index(it)
            # TermDictionary[it] = stemdictionary[it]
            TermInTheme["T" + str(count) + "_" + it] = str("%.2f" % d1[it])

            word_xml = doc.createElement("word")
            word_xml.setAttribute("weight", str(d1[it]))
            wordtext_xml = doc.createTextNode(it)
            word_xml.appendChild(wordtext_xml)
            words_xml.appendChild(word_xml)

        theme_html = theme_html + "</p>"
        if (inc_articles == 1):
            # Print articles/items/survey responses that map to Theme/Feature
            articlesInTheme = {}
            articleweights = []
            for article in range(noarticles):
                if (weights_matrix[article, row] > 0.08):
                    articlesInTheme[article] = weights_matrix[article, row]
                    articleweights.append(weights_matrix[article, row])
                    DocDictionary["D" + str(article)] = "Doc" + str(article)
                    DocInTheme["T" + str(count) + "_D" + str(article)] = str("%.2f" % weights_matrix[article, row])
                else:
                    # Capture all non attached documents
                    DocDictionary["D" + str(article)] = "Doc" + str(article)
            # max_weight_val = max(articleweights)
            # min_weight_val = min(articleweights)

            articles_In_Theme_Order = sortDictionaryByValues(articlesInTheme)

            # Create a <responses> element
            reponses_xml = doc.createElement("responses")
            theme_xml.appendChild(reponses_xml)

            for article_no in articles_In_Theme_Order:
                response_xml = doc.createElement("response")
                response_xml.setAttribute("id", str(surveyQuestionResponseNID[article_no]))
                response_xml.setAttribute("weight", str(("%.2f" % weights_matrix[article_no, row])))

                responsetext_xml = doc.createTextNode(item_Titles[article_no])
                response_xml.appendChild(responsetext_xml)

                reponses_xml.appendChild(response_xml)

            # Create Rendered element
            rendered_xml = doc.createElement("rendered")
            theme_xml.appendChild(rendered_xml)

        count = count + 1
    return doc.toprettyxml(indent="  ")


def showtopterms(weights_matrix1, weights_matrix2, m, k, list_Of_Included_Words, outputsamefiledir, outputdisfiledir1,
                 outputdisfiledir2):
    '''displays the top NUMTERMS terms for each cluster, k'''
    fsame = open(outputsamefiledir, 'a')
    fdis1 = open(outputdisfiledir1, 'a')
    fdis2 = open(outputdisfiledir2, 'a')
    # 输出相同的主题1
    print str(shape(weights_matrix1)) + '--' + str(shape(list_Of_Included_Words))
    for c in range(k):
        # populate a dict with term:membership
        # as a key:value pair for each term in this cluster
        toptermsd = {}
        for t in range(len(weights_matrix1)):
            toptermsd[list_Of_Included_Words[t]] = weights_matrix1[t][c]

        # sort the terms into a list of tuples, ordered by value
        # (cluster membership)对x这个数组，用第二个元素排序。
        topterms = sorted(toptermsd.items(), key=lambda x: x[1])

        # print the last NUMTERMS terms
        fsame.write("\nW矩阵中，第 %d:" % (c + 1) + '列\n')
        for j in range(1, m):
            fsame.write("\t" + str(topterms[-j][0]).strip() + " (%.7f)" % (topterms[-j][1]))
            if topterms[-j][1] == 0:
                break
        toptermsd.clear()

    # 输出不相同的主题1
    for c in range(k, shape(weights_matrix1)[1]):
        # populate a dict with term:membership
        # as a key:value pair for each term in this cluster
        toptermsd = {}
        for t in range(len(weights_matrix1)):
            toptermsd[list_Of_Included_Words[t]] = weights_matrix1[t][c]

        # sort the terms into a list of tuples, ordered by value
        # (cluster membership)对x这个数组，用第二个元素排序。
        topterms = sorted(toptermsd.items(), key=lambda x: x[1])

        # print the last NUMTERMS terms
        fdis1.write("\nW1矩阵中，第 %d:" % (c + 1) + '列\n')
        for j in range(1, m):
            fdis1.write("\t" + str(topterms[-j][0]).strip() + " (%.7f)" % (topterms[-j][1]))
            if topterms[-j][1] == 0:
                break
        toptermsd.clear()

        # 输出不相同的主题2
    for c in range(k, shape(weights_matrix2)[1]):
        # populate a dict with term:membership
        # as a key:value pair for each term in this cluster
        toptermsd = {}
        for t in range(len(weights_matrix2)):
            toptermsd[list_Of_Included_Words[t]] = weights_matrix2[t][c]

        # sort the terms into a list of tuples, ordered by value
        # (cluster membership)对x这个数组，用第二个元素排序。
        topterms = sorted(toptermsd.items(), key=lambda x: x[1])

        # print the last NUMTERMS terms
        fdis2.write("\nW2矩阵中，第 %d:" % (c + 1) + '列\n')
        for j in range(1, m):
            fdis2.write("\t" + str(topterms[-j][0]).strip() + " (%.7f)" % (topterms[-j][1]))
            if topterms[-j][1] == 0:
                break
        toptermsd.clear()

    fsame.close()
    fdis1.close()
    fdis2.close()


# Strange way to determine if NaN in Python?
def isNaN(x):
    return (x == x) == False


if __name__ == '__main__':
    s2 = [[ 5,'aom'], [2,'bone'], [4,'cusan'], [1,'dom'], [0,'eom']]
    s2.sort()
    s2.reverse()
    for item in s2:
        print item

