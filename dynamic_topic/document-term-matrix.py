#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Tool to pre-process documents contained one or more directories, and export a document-term matrix for each directory.
"""
import os, os.path, sys, codecs
import logging as log
from optparse import OptionParser

import text.util
from scipy.sparse import csr_matrix

# --------------------------------------------------------------

def read_problem(data_file_name):
    """
    svm_read_problem(data_file_name) -> [y, x]

    Read LIBSVM-format data from data_file_name and return labels y
    and data instances x.
    """
    prob_y = []
    prob_x = []
    prob_z = []
    line_num = 0
    #file_write = open("news20_all_data", 'w')
    for line in open(data_file_name):
        print line_num
        line = line.split(None, 1)
        # In case an instance with all zero features
        # if len(line) == 1: line += ['']
        label, features = line
        for e in features.split():
            ind, val = e.split(":")
            # xi[int(ind)] = float(val)
            #strs = "  (" + str(line_num) + ", " + str(ind) + ") " + str(float(val))
            prob_x += [int(line_num)]
            prob_y += [int(ind)]
            prob_z += [float(val)]
            #file_write.write(strs + "\n")
        line_num += 1
    a = csr_matrix((prob_z, (prob_x, prob_y))).toarray()
    return prob_x,prob_y,a

def main():
    parser = OptionParser(usage="usage: %prog [options] directory1 directory2 ...")
    parser.add_option("--df", action="store", type="int", dest="min_df",
                      help="minimum number of documents for a term to appear", default=1)
    parser.add_option("--tfidf", action="store_true", dest="apply_tfidf",
                      help="apply TF-IDF term weight to the document-term matrix")
    parser.add_option("--norm", action="store_true", dest="apply_norm",
                      help="apply unit length normalization to the document-term matrix")
    parser.add_option("--minlen", action="store", type="int", dest="min_doc_length",
                      help="minimum document length (in characters)", default=10)
    parser.add_option("-s", action="store", type="string", dest="stoplist_file", help="custom stopword file path",
                      default=None)
    parser.add_option("-o", "--outdir", action="store", type="string", dest="dir_out",
                      help="output directory (default is current directory)", default=None)
    parser.add_option("--ngram", action="store", type="int", dest="max_ngram",
                      help="maximum ngram range (default is 1, i.e. unigrams only)", default=1)
    # Parse command line arguments
    (options, args) = parser.parse_args()
    if (len(args) < 1):
        parser.error("Must specify at least one directory")
    log.basicConfig(level=20, format='%(message)s')

    if options.dir_out is None:
        dir_out = os.getcwd()  # os.getcwd() 方法用于返回当前工作目录
    else:
        dir_out = options.dir_out

    # Process each directory
    for in_path in args:
        print "--in_path--"
        print in_path

        dir_name = os.path.basename(in_path)
        # Read content of all documents in the directory
        # 按行读取数据，转X

        doc_ids,terms,X = read_problem(in_path)

        #terms=[1]
        # Pre-process the documents
        #(X, terms) = x_preprocess(x)
        log.info("Created %dx%d document-term matrix" % X.shape)

        # Save the pre-processed documents
        out_prefix = os.path.join(dir_out, dir_name)
        print "--out_prefix--"
        print out_prefix
        text.util.save_corpus(out_prefix, X, terms, doc_ids)


# --------------------------------------------------------------

if __name__ == "__main__":
    main()
