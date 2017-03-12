# -*- coding: UTF-8-*-

from svmutil import *

#
# [label]   [Index1]:[value1]  [index2]:[value2]  [index3]:[value3]
# [label]:类别（通常是整数）[index n]: 有顺序的索引 [value n]
# (42.57450538442274, 22.97044828449787, 0.38045666500901687)
# -t 1 -c 20.0 -g 100.0
# -t 2  -c 8.0  -h 0  (39.644377660906585, 26.12296518908089, 0.27957965774361493)
# -t 0 -v 5 -c 8.0 -g 10 -h 0'  Accuracy = 73.0091%
# -t 0 -v 5 -c 8.0 -g 10 -h 0'  Accuracy = 73.0091%
# -t 0 -v 10 -c 2 -g 150 -h 0 Accuracy = 74.2642%
#-t 0 -c 100 -v 10 -g 150 -h 0 Accuracy = 74.9545%
#-t 0 -c 100.0 -g 150.0 -h 0 (75.4320060105184, 7.293764087152517, 0.791816467246095)
#-t 0 -c 100.0 -g 150.0 -d 4
#-t 0 -c 100.0 -g 10.0 (75.4320060105184, 7.293764087152517, 0.791816467246095)



y, x = svm_read_problem("data/news20")
m = svm_train(y, x, '-t 0 -c 100.0 -g 10.0')
print "----finish training---"

u, v = svm_read_problem("data/news20test")
p_lable, p_acc, p_val = svm_predict(u, v, m)
print p_acc
