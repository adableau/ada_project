#!/usr/bin/env python
"""
Tool to generate a NMF topic model on one or more corpora, using a fixed number of topics.
"""
import os, sys, random, operator
import logging as log
from optparse import OptionParser
import numpy as np
import text.util
import unsupervised.nmf, unsupervised.rankings, unsupervised.coherence

from scipy.sparse import csr_matrix


# --------------------------------------------------------------

def save_tfidf_data(dataname, file):
    print type(file)
    np.savetxt(dataname, file, delimiter=',')


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
    for line in open(data_file_name):
        print line_num
        line = line.split(None, 1)
        label, features = line
        for e in features.split():
            ind, val = e.split(":")
            prob_x += [int(line_num)]
            prob_y += [int(ind)]
            prob_z += [float(val)]
        line_num += 1
    a = csr_matrix((prob_z, (prob_x, prob_y))).toarray()
    return prob_x, prob_y, a


def main():
    parser = OptionParser(usage="usage: %prog [options] window_matrix1 window_matrix2...")
    parser.add_option("--seed", action="store", type="int", dest="seed", help="initial random seed", default=1000)
    parser.add_option("-k", action="store", type="string", dest="krange", help="number of topics", default=None)
    parser.add_option("--maxiters", action="store", type="int", dest="maxiter", help="maximum number of iterations",
                      default=200)
    parser.add_option("-o", "--outdir", action="store", type="string", dest="dir_out",
                      help="base output directory (default is current directory)", default=None)
    parser.add_option("-m", "--model", action="store", type="string", dest="model_path",
                      help="path to Word2Vec model, if performing automatic selection of number of topics",
                      default=None)
    parser.add_option("-t", "--top", action="store", type="int", dest="top",
                      help="number of top terms to use, if performing automatic selection of number of topics",
                      default=20)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="display topic descriptors")
    (options, args) = parser.parse_args()
    if (len(args) < 1):
        parser.error("Must specify at least one time window matrix file")
    log.basicConfig(level=20, format='%(message)s')

    # Parse user-specified range for number of topics K
    if options.krange is None:
        parser.error("Must specific number of topics, or a range for the number of topics")
    kparts = options.krange.split(",")
    kmin = int(kparts[0])

    # NMF implementation
    impl = unsupervised.nmf.SklNMF(max_iters=options.maxiter, init_strategy="nndsvd")
    k = 128
    # Process each specified time window document-term matrix
    for matrix_filepath in args:
        # Load the cached corpus
        window_name = os.path.splitext(os.path.split(matrix_filepath)[-1])[0]
        print "window_name--------" + str(window_name)
        log.info("- Processing time window matrix for '%s' from %s ..." % (window_name, matrix_filepath))
        X = text.util.load_corpus(matrix_filepath)
        log.info("Read %dx%d document-term matrix" % (X.shape[0], X.shape[1]))
        print "--------preprocess--X----"
        impl.apply(X, k)
        log.info("Generated %dx%d factor W and %dx%d factor H" % (
            impl.W.shape[0], impl.W.shape[1], impl.H.shape[0], impl.H.shape[1]))
        save_tfidf_data("X_tfidf_W_%s_%s.csv" % window_name % k, impl.W)
        save_tfidf_data("X_tfidf_H_%s_%s.csv" % window_name % k, impl.H)


# --------------------------------------------------------------

if __name__ == "__main__":
    main()
