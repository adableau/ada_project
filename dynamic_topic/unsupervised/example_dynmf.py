#!/usr/bin/env python
#
# [[22 28]
# [49 64]]
# nit gradient norm 80.399005

# Iter = 3 Final proj-grad norm 0.053615
# [[  1.42571928e-04   3.51241590e+00   2.31184835e+00]
# [  0.00000000e+00   1.16978638e+01   2.83327064e+00]]
# [[ 0.99999981  1.00000017]
# [ 2.97900234  4.01686945]
# [ 4.99300074  6.00578361]]
#
from dynamic_topic.evaluate.evaluate import get_RMSE, compute_rmse
from dynmf import *
from numpy import *
from collections import defaultdict
w1 = array([[1, 2, 3], [4, 5, 6], [1, 2, 3], [4, 5, 6], [1, 2, 3], [4, 5, 6]])
h1 = array([[1, 2], [3, 4], [5, 6]])
#X = array([[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

X = dot(w1,h1)
print X
rank = X.shape[1]
pred = np.ones(rank)
pred[:] =2
print rank


(wo, ho) = nmf(X, 2, 0.001, 1000, 1000)
U = dot(wo, ho)
print U
#print get_RMSE(X.tolist(), U.tolist())
print wo
print ho
#
# mu, sigma = 0, 0.1 # mean and standard deviation
# s = random.normal(mu, sigma, 1000)
# rarray=random.uniform(0,1,size=10)
# k=4
# ic=5
# W = array([[random.uniform(0,1,size=4)] for i in range(5)])
# print W
