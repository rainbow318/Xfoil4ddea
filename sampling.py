# -*- coding: utf-8 -*-

import numpy as np
from utils import to2dColVec
import time

def lhs(n, d, lower_bound, upper_bound):
    """Latin hypercude sampling

   Args:
        n: The number of the sample data
        d: The number of the decision variables
        lower_bound: A number or a vector, the lower bound of the decision variables
        upper_bound: A number or a vector, the upper_bound of the decision variables
    """

    if np.any(lower_bound > upper_bound):
        return None
    lower_bound, upper_bound = to2dColVec(lower_bound), to2dColVec(upper_bound)
    intervalSize = 1.0 / n
    # samplePoints[i] is the point that sampled from demension i
    samplePoints = np.empty([d, n])
    for i in range(n):
        samplePoints[:, i] = np.random.uniform(low=i * intervalSize, high=(i + 1) * intervalSize, size=d)
    # offset
    samplePoints = lower_bound + samplePoints * (upper_bound - lower_bound)
    for i in range(d):
        np.random.shuffle(samplePoints[i])
    return samplePoints.T
    

"""
def lhs(N, D, lower_bound, upper_bound):

    d = 1.0 / N
    result = np.empty([N, D])
    temp = np.empty([N])
    for i in range(D):
        for j in range(N):
            temp[j] = np.random.uniform(
                low=j * d, high=(j + 1) * d, size=1)[0]
        np.random.shuffle(temp)
        for j in range(N):
            result[j, i] = temp[j]
    if np.any(lower_bound > upper_bound):
        print('Range error')
        return None
    np.add(np.multiply(result, (upper_bound - lower_bound),
           out=result), lower_bound, out=result)
    return result
"""

def rs(n, d, lower_bound, upper_bound):
    """random sampling

    Args:
        n: The number of the sample data
        d: The number of the decision variables
        lower_bound: A number or a vector, the lower bound of the decision variables
        upper_bound: A number or a vector, the upper_bound of the decision variables
    """
    if np.any(lower_bound > upper_bound):
        return None
    lower_bound, upper_bound = to2dColVec(lower_bound), to2dColVec(upper_bound)
    samplePoints = np.random.random([d, n])
    samplePoints = lower_bound + samplePoints * (upper_bound - lower_bound)
    return samplePoints.T


def latin(N, D, lower_bound, upper_bound):
    """ another implement of lhs

    code reference: https://github.com/HandingWangXDGroup/TT-DDEA
    """
    d = 1.0 / N
    result = np.empty([N, D])
    temp = np.empty([N])
    for i in range(D):
        for j in range(N):
            temp[j] = np.random.uniform(
                low=j * d, high=(j + 1) * d, size=1)[0]
        np.random.shuffle(temp)
        for j in range(N):
            result[j, i] = temp[j]
    if np.any(lower_bound > upper_bound):
        print('Range error')
        return None
    np.add(np.multiply(result, (upper_bound - lower_bound),
           out=result), lower_bound, out=result)
    return result


if __name__ == "__main__":
    def test_lhs_accuracy(samples, lower_bound, upper_bound):
        """testing code: test the right of lhs
        """
        n, d = np.shape(samples)

        gap = (upper_bound - lower_bound) / n
        interval_lower = np.array(
            [i * gap + lower_bound for i in range(n)]).reshape([-1, 1])
        interval_upper = np.array(
            [(i + 1) * gap + lower_bound for i in range(n)]).reshape([-1, 1])

        samples = np.sort(samples, axis=0)
        n_error_points = np.sum(
            ~((interval_lower <= samples) & (samples < upper_bound)))

        return n_error_points

    upper_bound = 5.12
    lower_bound = -5.12
    d = 100
    n = 11 * d

    b = lhs(n, d, lower_bound, upper_bound)
    print(b)
    np.savetxt("./F50_0_training.txt", b, fmt="%.6f")
    print(test_lhs_accuracy(b, lower_bound, upper_bound))

    c = latin(n, d, lower_bound, upper_bound)
    np.savetxt("./F50_0_testing.txt", c, fmt="%.6f")

    print(test_lhs_accuracy(c, lower_bound, upper_bound))
