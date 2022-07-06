# cython: language_level=2
cimport cDPQ
import numpy as np
from numpy.linalg import norm

cimport numpy as np
from cpython cimport array


def coptimum_reparam(np.ndarray[double, ndim=1, mode="c"] q1, np.ndarray[double, ndim=1, mode="c"] time,
                     np.ndarray[double, ndim=1, mode="c"] q2, lam1=0.0, size_t nbhd_dim=7):
    """
    cython interface for calculates the warping to align srsf q2 to q1

    :param q1: vector of size N samples of first SRSF
    :param time: vector of size N describing the sample points
    :param q2: vector of size N samples of second SRSF
    :param lam1: controls the amount of elasticity (default = 0.0)
    :param nbhd_dim: size of the grid (default = 7)

    :rtype vector
    :return gam: describing the warping function used to align q2 with q1
    """
    cdef int M, n1
    cdef double lam
    M = q1.shape[0]
    n1 = 1
    lam = lam1
    q1 = q1 / norm(q1)
    q2 = q2 / norm(q2)
    cdef np.ndarray[double, ndim=1, mode="c"] G = np.zeros(M)
    cdef np.ndarray[double, ndim=1, mode="c"] T = np.zeros(M)
    cdef np.ndarray[double, ndim=1, mode="c"] size = np.zeros(1)

    sizes = np.zeros(1, dtype=np.int32)
    Go = np.zeros((M, 1))
    To = np.zeros((M, 1))
    cDPQ.DynamicProgrammingQ2(&q1[0], &time[0], &q2[0], &time[0], n1, M, M, &time[0], &time[0], M, M, &G[0],
                              &T[0], &size[0], lam, nbhd_dim)
    sizes = np.int32(size)
    Go[:, 0] = G
    To[:, 0] = T
    gam0 = np.interp(time, To[0:sizes[0], 0], Go[0:sizes[0], 0])
    gam = (gam0 - gam0[0]) / (gam0[-1] - gam0[0])

    return gam

