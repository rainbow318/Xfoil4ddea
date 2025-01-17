# -*- coding: utf-8 -*-

import numpy as np
import math


# to2dNpArray(): 将一维的数组转化为2维的矩阵
def to2dNpArray(x):
    # type conversion  对于输入的x，首先判断其是否为ndarray类型
    if not isinstance(x, np.ndarray):  # isinstance()函数来判断一个对象是否是一个已知的类型
        x = np.array(x)
    # convert to matrix
    if x.ndim == 1:  # ndarray.ndim 秩，即x, y, z轴的数量，或维度的数量。
        x = x[np.newaxis, :]  # 对行增加维度
    return x


# to2dColVec: 转化为列向量
def to2dColVec(x):
    """convert to column vector
    convert a number or 1-d vector to column vector
    """
    # if issubclass(type(x), (int, float, complex)):
    if np.size(x) == 1:  # 如果x只有一个元素，就直接返回x
        return x
    # convert to 2-d column vector of type numpy.array
    return np.reshape(x, (np.size(x), -1))


def mean(x):
    x = to2dNpArray(x)
    return np.mean(x)


def std(x):
    x = to2dNpArray(x)
    return math.sqrt(var(x))


def var(x):
    x = to2dNpArray(x)
    m = np.mean(x)
    s = 0
    for i in x[0]:
        s += (i - m) * (i - m)
    return math.fabs(s / m)


if __name__ == "__main__":
    a = [1, 2, 3, 4]
    b = np.array(a)
    a = to2dNpArray(a)
    b = to2dNpArray(b)
    print(a)
    print(b)
    print(a.shape)
    print(b.shape)
    print(type(to2dNpArray(a)))
    print(type(to2dNpArray(b)))
