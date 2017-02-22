# -*- coding:utf-8 -*-
import os
import nltk
import string   
import re 
from nltk.corpus import wordnet as wn  
from string import maketrans
from string import punctuation
from string import digits 
# ���ַ������д���
def PreprocessingSentence(original_line):
    line1 = nltk.sent_tokenize(original_line)
    str = ''.join(line1)
    line2 = nltk.word_tokenize(str)
    return line2

# �ָ�ɾ���
def SenToken(raw):
    sent_tokenizer = nltk.data._open('../util/english.pickle')
    sents = sent_tokenizer.tokenize(raw)
    return sents

# ȥ�����ֱ��ͷ���ĸ�ַ�
def CleanLines(line):  
    identify = maketrans('', '')  
    delEStr = punctuation + digits  # ASCII �����ţ�����    
    #cleanLine = line.translate(identify, delEStr)  # ȥ��ASCII �����źͿո�  
    cleanLine = line.translate(identify, delEStr)  # ȥ��ASCII ������  
    return cleanLine  

#���Ա�ע
def PosTagger(sents):
    taggedLine=[nltk.pos_tag(sent) for sent in sents]  
    return taggedLine

#nltk.word_tokenize�ִ�
def WordTokener(self,sent):#�������ַ����ָ�ɴ�  
    result=''  
    wordsInStr = nltk.word_tokenize(sent)  
    return wordsInStr

#ȥͣ�ôʺ�Сдȥ�̴�
#ȥ�������ţ�����С��3�Ĵ��Լ�non-alpha�ʣ�Сд�� 
def CleanWords(self,wordsInStr): 
    cleanWords=[]  
    stopwords = {}.fromkeys([ line.rstrip()for line in open('EnglishStopWords.txt')])
    for words in wordsInStr:
        cleanWords+= [[w.lower() for w in words if w.lower() not in stopwords and 3<=len(w)]]  
    return cleanWords  