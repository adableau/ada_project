# coding:utf-8  
__author__ = "ada"
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

if __name__ == "__main__":
    #hi = raw_input('hello123? ')

    print 'hello? ',  # comma to stay in the same line
    print 'hello12? ',  # comma to stay in the same line

    #hi = sys.stdin.readline()  # -1 to discard the '\n' in input stream
    for line in sys.stdin:
        print line