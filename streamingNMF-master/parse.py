#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Parser for UCI bag-of-words dataset

Usage: zcat docword.$(data).txt.gz | tail -n +4 | python parse.py vocab.$(data).txt $(min_freq)
- $(data): the name of data (e.g. nips)
- $(min_freq): minimum word frequency to put into a co-occurrence matrix
"""

import sys
from collections import defaultdict


file_voc = 'vocab.nips.txt'
file_doc = 'docword.nips.txt'
file_doc_word = 'docword.txt'

def _main_func():
    min_freq = 3
    mp = dict()#存放词频
    for i, line in enumerate(open(file_voc, 'r')):
        mp[i + 1] = line.strip()

    write_file = open(file_doc_word,'w')
    old_i = 1
    word_queue = dict()#文章中词/词频对
    for line in open(file_doc, 'r'):
        i, j, k = [int(num) for num in line.split()]#doc,word, frequency
        # 迭代输出,作为下一次的输入
        if i != old_i:
            for w1, f1 in word_queue.iteritems():
                for w2, f2 in word_queue.iteritems():
                    str_w = str(w1)+','+ str(w2)+','+ str(f1 * f2)
                    write_file.write(str_w)
                    write_file.write("\n")
            write_file.write("\n")
            word_queue = dict()

        if k >= min_freq:
            word_queue[mp[j]] = k
        old_i = i
    write_file.close()
    print '--finished---'

_main_func()
