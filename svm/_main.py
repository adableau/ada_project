# -*- coding: UTF-8-*-

from svmutil import *
#
#[label]   [Index1]:[value1]  [index2]:[value2]  [index3]:[value3]
# [label]:类别（通常是整数）[index n]: 有顺序的索引 [value n]
#

y,x=svm_read_problem("data/news20")
m=svm_train(y,x,'-c 8.0 -g 8.0')


u,v=svm_read_problem("data/news20test")
p_lable,p_acc,p_val=svm_predict(y,x,m)
#ACC, MSE, SCC  4.5, 103.165, 0.00440058054252315
print p_acc
#print p_val
