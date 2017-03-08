#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

from numpy import *
import numpy as np


def get_RMSE(X, U):
    rank = U[0].shape[1]
    pred = np.ones(rank)
    err = 0.0
    nnz = 0
    for (key, val) in X.items():
        if np.isnan(val):
            continue
        pred[:] = 1  # initialization
        for l in xrange(self.mapper.order):
            pred *= U[l][key[l], :]
        err += (np.double(val) - np.sum(pred)) ** 2
        nnz += 1
    try:
        return np.sqrt(err / nnz)
    except ZeroDivisionError:
        return 0


def get_RMSES(prefer1, prefer2):
    rmse = 0
    for key1, value in prefer1.items():
        val = 0
        # 迭代测试集，并与结果集进行比较
        for key, value in prefer1[key1].items():
            temp = pow(value - prefer2[key1][key], 2)  # 算两点的平方
            val += temp
        rmse += math.sqrt(val) / len(prefer1[key1])
    return rmse / len(prefer1)


def compute_rmse(arr):
    """computes rmse (root mean square error)"""

    # compute mean
    mean = sum(arr) / len(arr)
    sse = 0

    # loop through the list
    for i in arr:
        # compute sse as (val - mean)^2
        sse += (i - mean) ** 2

    # compute rmse and return
    rmse = math.sqrt(sse) / len(arr)
    return rmse
