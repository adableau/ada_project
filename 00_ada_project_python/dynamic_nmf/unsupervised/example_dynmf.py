#!/usr/bin/env python
#
#[[22 28]
#[49 64]]
#nit gradient norm 80.399005

#Iter = 3 Final proj-grad norm 0.053615
#[[  1.42571928e-04   3.51241590e+00   2.31184835e+00]
# [  0.00000000e+00   1.16978638e+01   2.83327064e+00]]
#[[ 0.99999981  1.00000017]
# [ 2.97900234  4.01686945]
# [ 4.99300074  6.00578361]]
#

from dynmf import *
from numpy import *



w1 = array([[1,2,3],[4,5,6],[1,2,3],[4,5,6],[1,2,3],[4,5,6]])
h1 = array([[1,2],[3,4],[5,6]])



#X = dot(h1,w1)
#print X.shape


(wo,ho) =  nmf(w1, 2, 0.001, 1000, 1000)

print wo
print ho
#
#mu, sigma = 0, 0.1 # mean and standard deviation
#s = random.normal(mu, sigma, 1000)
#rarray=random.uniform(0,1,size=10)
#k=4
#ic=5
#W = array([[random.uniform(0,1,size=4)] for i in range(5)])
#print W