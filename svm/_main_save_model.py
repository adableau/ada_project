# -*- coding: UTF-8-*-

from svmutil import *

#
# [label]   [Index1]:[value1]  [index2]:[value2]  [index3]:[value3]
# [label]:类别（通常是整数）[index n]: 有顺序的索引 [value n]
# http://www.cnblogs.com/Finley/p/5329417.html
# 18:52
# #

y, x = svm_read_problem("data/news20")
model_name = '20news_model'
model = svm_load_model(model_name)
if model is None:
    m = svm_train(y, x, '-t 1 -s 1 -b 1')
    svm_save_model(model_name, model)

u, v = svm_read_problem("data/news20test")
p_lable, p_acc, p_val = svm_predict(u, v, model)
# ACC, MSE, regression  4.5, 103.165, 0.00440058054252315
# (5.141049301344582, 101.73345636699183, 0.0012423517636237576)
print p_acc
# print p_val
