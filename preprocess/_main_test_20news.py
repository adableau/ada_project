# -*- coding: UTF-8-*-
# 61188 word
# 20 different newsgroups
# http://qwone.com/~jason/20Newsgroups/

def read_problem(data_file_name, word_num):
    """
    svm_read_problem(data_file_name) -> [y, x]

    Read LIBSVM-format data from data_file_name and return labels y
    and data instances x.
    """
    prob_y = []
    prob_x = []
    line_num = 0
    file_write = open("news20_all_data", 'w')
    for line in open(data_file_name):
        print line_num
        line = line.split(None, 1)
        # In case an instance with all zero features
        #if len(line) == 1: line += ['']
        xi = {}
        label, features = line
        for e in features.split():
            ind, val = e.split(":")
            #xi[int(ind)] = float(val)
            strs = "  (" + str(line_num) + ", " + str(ind) + ") " + str(float(val))
            print strs
            file_write.write(strs+"\n")
        line_num += 1
        prob_y += [float(label)]
        #prob_x += [xi]
    file_write.close()

    #return (prob_y, prob_x)


def save_tfidf_data(dataname, file):
    f = open(dataname, 'w')
    f.write(str(file))
    f.close()


read_problem("test20new.txt", 61188)

