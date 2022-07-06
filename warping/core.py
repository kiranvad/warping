import optimum_reparamN2 as orN2
import numpy as np
from scipy.interpolate import UnivariateSpline

def warp_f_gamma(time, f, gam):
    f_temp = np.interp((time[-1] - time[0]) * gam + time[0], time, f)

    return f_temp

def to_srsf(time, f):
    """
    converts f to a square-root slope function (SRSF)
    :param f: vector of size N samples
    :param time: vector of size N describing the sample points
    :rtype: vector
    :return q: srsf of f
    """
    spl = UnivariateSpline(time, f, s=0)
    grad = spl.derivative(n=1)(time)
    q = grad / np.sqrt(np.fabs(grad) + 1e-3)

    return q

def compute_warping(time, f1, f2, lam=0.0, grid_dim=7):
    """
    calculates the warping to align srsf q2 to q1
    :param q1: vector of size N or array of NxM samples of first SRSF
    :param time: vector of size N describing the sample points
    :param q2: vector of size N or array of NxM samples samples of second SRSF
    :param method: method to apply optimization (default="DP2") options are "DP","DP2","RBFGS"
    :param lam: controls the amount of elasticity (default = 0.0)
    :param grid_dim: size of the grid, for the DP2 method only (default = 7)
    :rtype: vector
    :return gam: describing the warping function used to align q2 with q1
    """
    
    q1 = to_srsf(time, f1)
    q2 = to_srsf(time, f2)
    
    gamma = orN2.coptimum_reparam(np.ascontiguousarray(q1), time,
        np.ascontiguousarray(q2), 
        lam, grid_dim
        )
    f2_gamma = warp_f_gamma(time, f2, gamma)
    
    return gamma, f2_gamma