# -*- coding: UTF-8-*-

from svmutil import *

#
# [label]   [Index1]:[value1]  [index2]:[value2]  [index3]:[value3]
# [label]:类别（通常是整数）[index n]: 有顺序的索引 [value n]
# http://www.cnblogs.com/Finley/p/5329417.html
# 73.9441%


y, x = svm_read_problem("data/news20")
m = svm_train(y, x, '-t 2 -s 1')

u, v = svm_read_problem("data/news20test")
p_lable, p_acc, p_val = svm_predict(u, v, m)
# ACC, MSE, regression
# 4.5, 103.165, 0.00440058054252315
print p_acc
