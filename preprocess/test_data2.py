# coding:utf-8
import csv

from sklearn.externals import joblib


def read_problem(data_file_name, word_num):
    """
    svm_read_problem(data_file_name) -> [y, x]

    Read LIBSVM-format data from data_file_name and return labels y
    and data instances x.
    """
    prob_y = []
    prob_x = []
    prob_z = []
    line_num = 0
    file_write = open("news20_all_data", 'w')
    for line in open(data_file_name):
        print line_num
        line = line.split(None, 1)
        # In case an instance with all zero features
        # if len(line) == 1: line += ['']
        label, features = line
        for e in features.split():
            ind, val = e.split(":")
            # xi[int(ind)] = float(val)
            strs = str(line_num) + "," + str(ind) + "," + str(float(val))
            file_write.write(strs + "\n")
        line_num += 1
    # a = csr_matrix((prob_z, (prob_x, prob_y))).toarray()

    print(a.shape)
    # prob_x += [xi]
    file_write.close()

    # return (prob_y, prob_x)


def read_data_matrix(data_file_name, word_num):
    """
    svm_read_problem(data_file_name) -> [y, x]

    Read LIBSVM-format data from data_file_name and return labels y
    and data instances x.
    """
    prob_y = []
    prob_x = []
    prob_z = []
    for line in open(data_file_name):
        line = line.split(",")
        # In case an instance with all zero features
        # if len(line) == 1: line += ['']
        line_num, ind, val = line
        prob_x += [int(line_num)]
        prob_y += [int(ind)]
        prob_z += [float(val)]
    a = csr_matrix((prob_z, (prob_x, prob_y))).toarray()

    print "--------------"
    print(a.shape)
    # prob_x += [xi]


def save_tfidf_data(dataname, file):
    f = open(dataname, 'w')
    f.write(str(file))
    f.close()


if __name__ == "__main__":
    # !/usr/bin/python

    import numpy as np
    from scipy.sparse import csr_matrix

    row = np.array([0, 0, 1, 2, 2, 2])
    col = np.array([0, 2, 2, 0, 1, 2])
    data = np.array([1, 2, 3, 4, 5, 6])
    a = csr_matrix((data, (row, col)), shape=(3, 3)).toarray()

    print(a)

    row = np.array([0, 0, 1, 2, 2, 2])
    col = np.array([0, 2, 2, 0, 1, 2])
    data = np.array([1, 2, 3, 4, 5, 6])
    a = csr_matrix((data, (row, col)), shape=(3, 3)).toarray()

    print(a)

    # read_problem("news20_all", 61188)
    read_data_matrix("news20_all_data", 61188)
