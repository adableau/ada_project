# -*- coding:utf-8 -*-
# 词干化、去停用词处理

import os
import nltk
import string
import re
from nltk.corpus import wordnet as wn
from string import maketrans
from string import punctuation
from string import digits
import jieba
from __builtin__ import file
# 结巴分词的词性标注模块
import jieba.posseg
from nltk.stem import WordNetLemmatizer
import codecs

# 修改了第一行与第二行的保存的地方
localpath_EditionDate = '/home/baiqingchun/00_data/20newsGroup'
# 分词后的localpath_EditionDate
wordseg_localpath_EditionDate = '/home/baiqingchun/00_data/20_output_data/'

deleteList = ['SECTION:', 'LENGTH:', 'Final Edition:', 'To the Editor:', 'BYLINE:', 'Late Edition', 'SOURCE:']


# 处理每个txt文件
# 对文本按照句子进行分割
# 对句子进行分词
def ReadTextFile(path):
    file = open(path)
    list = []
    # 判断是否找到文档的开始的第一个文章长度的tag，找到则加1
    tag = 0
    # contents = file.read();
    # print(contents)
    while (True):
        original_line = file.readline()
        for keywords_str in deleteList:
            if keywords_str in original_line:
                continue
        if ('LOAD-DATE:' in original_line):
            break
        original_line = original_line.lower()
        # elif '?' in original_line:
        #    continue
        if original_line:
            # 结巴分词对读入的数据进行处理
            # 先分词，然后查找是否在停用词库中
            process_line = DeleteStopWords(original_line)
            proresult = DeletePunctuation(process_line)
            # nltk词性标注
            wordsList = JiebaPosseg(proresult)
            # wordsList = JiebaPosseg("effectively")
            # 拿出每一个词，进行词性还原
            wordnet_lemmatizer = WordNetLemmatizer()
            for item in wordsList:
                # result =  nltk.stem.WordNetLemmatizer(word[0],word[1])
                # result =  nltk.stem.WordNetLemmatizer(word[0])
                word = item[0]
                wordpos = penn_to_wn(item[1])
                if wordpos != None:
                    result = wordnet_lemmatizer.lemmatize(word, wordpos)
                    # if word!=result:
                    #    print(word+'-->'+result)
                    list.append(result)
                else:
                    list.append(word)
            # sample_list = [line + ' ' for line in process_line]
            # result = ''.join(sample_list)
            list.append('\n')
            # print(file.name)
        else:
            break
    return list


# 对读取的出的文本处理
def DealTheContent(list):
    for item in list:
        original_line = item
        '''
        if (original_line == '\n'):
            continue
        if ('LENGTH:' not in original_line and tag == 0):
            continue
        elif ('LENGTH:' in original_line):
            tag = tag + 1
            continue
        '''
        for deleteItem in deleteList:
            if (deleteItem in original_line):
                continue
        original_line = original_line.lower()
        # elif '?' in original_line:
        #    continue
        if original_line != '\n':
            # 结巴分词对读入的数据进行处理
            # 先分词，然后查找是否在停用词库中
            process_line = DeleteStopWords(original_line)
            proresult = DeletePunctuation(process_line)
            # nltk词性标注
            wordsList = JiebaPosseg(proresult)
            # wordsList = JiebaPosseg("effectively")
            # 拿出每一个词，进行词性还原
            wordnet_lemmatizer = WordNetLemmatizer()
            for item in wordsList:
                # result =  nltk.stem.WordNetLemmatizer(word[0],word[1])
                # result =  nltk.stem.WordNetLemmatizer(word[0])
                word = item[0]
                wordpos = penn_to_wn(item[1])
                if wordpos != None:
                    result = wordnet_lemmatizer.lemmatize(word, wordpos)
                    # if word!=result:
                    #    print(word+'-->'+result)
                    list.append(result)
                else:
                    list.append(word)
            # sample_list = [line + ' ' for line in process_line]
            # result = ''.join(sample_list)
            list.append('\n')
            # print(file.name)
    return list


# 删除停用词
def DeleteStopWords(str):
    stopwords = {}.fromkeys([line.rstrip() for line in
                             open('words.py')])
    segs = jieba.cut(str, cut_all=False)
    final = ''
    for seg in segs:
        seg = seg.encode('utf-8')
        if seg not in stopwords:
            final += seg

    return final


# 正则表达式去除字符串中的标点符号
def DeletePunctuation(str):
    r = '[’!"#$%&\'()*+,-./:;<=>??@[\\]^_`{|}~]+'
    line = re.sub(r, ' ', str)
    return line


# nltk分词、词性标注
def JiebaPosseg(str):
    seg = jieba.posseg.cut(str)
    list = []
    for item in seg:
        # print(item)
        if (item.word != ' ' and item.word != '\n'):
            list.append((item.word, item.flag))
    return list


# 判断是不是名词
def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


# 判断是不是动词
def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


# 副词
def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


# 形容词
def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


# 对词性的判断
def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return None


# dirpath
def WriteToLocal(dirpath):
    files = os.listdir(dirpath)
    for folderName in files:  ##第一层文件夹
        rootpath = os.path.join(dirpath, folderName)
        secondFolders = os.listdir(rootpath)
        for secondFolder in secondFolders:
            fullpath = os.path.join(rootpath, secondFolder)
            txtFiles = os.listdir(fullpath)
            for txtName in txtFiles:  # 第二个文件夹
                fullpaths = os.path.join(fullpath, txtName)
                print fullpaths
                list = ReadTextFile(fullpaths)  # 对文本分句、分词
                save_path = wordseg_localpath_EditionDate + '/' + folderName + '/' + secondFolder
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                save_path = save_path + '/' + txtName
                file_write = open(save_path, 'w')
                sample_list = [line + ' ' for line in list]
                for line in sample_list:
                    try:
                        file_write.write(line)
                    except Exception, e:
                        print Exception, ":", e
                print(wordseg_localpath_EditionDate + folderName + '\\' + 'chuli' + txtName + '--->done')
                file_write.close()


'''
判断文中是不是有
LOAD-DATE:和LENGTH:
'''


def JudgeTheTxtFile(path):
    file = open(path)
    content = file.readlines()
    contentStr = ''.join(content)
    if ('LOAD-DATE:' not in contentStr):
        os.system('notepad ' + path)
        print(path)
    # if('LENGTH:' not in contentStr):
    file.close()


# 判断文章中的第一行出版社和第二行的时间是不是这个顺序
def JudgeEditionTime(path):
    # path = 'E:\\LTN\\test\\DataDelete-N\\1997\\delete5.txt'
    monthList = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                 'november', 'december']
    flag1 = 0
    flag2 = 0
    file = open(path)
    content = file.readlines()
    line1Date = content[1].lower()
    line2Date = content[2].lower()
    for item in monthList:
        if (item not in line1Date):
            flag1 = flag1 + 1
        else:
            flag1 = 13
    for item in monthList:
        if (item not in line2Date):
            flag2 = flag2 + 1
        else:
            flag2 = 13
    # 如果第二行不是日期，第三行是日期，则互换2,3，行
    if flag1 == 12 and flag2 != 12:
        content[1] = line2Date
        content[2] = line1Date
        print(path + '-->' + 'success')
    file.close()
    return content


def DeleteBlackEnter(path):
    file = open(path)
    contensList = []
    while (True):
        content = file.readline()
        if (content):
            if (content != '\n'):
                contensList.append(content)
        else:
            break
    file.close()
    contentStr = ''.join(contensList)
    return contentStr


if __name__ == '__main__':
    WriteToLocal(localpath_EditionDate)
