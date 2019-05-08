import numpy as np
from scipy.optimize import newton

from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import h_inf, f, m_inf


def nullcline_h(v):
    return h_inf(v)


def nullcline_v(v, I_app, hs=1):
    nv = np.zeros((len(v),))
    parameters = default_parameters(I_app=I_app)
    for i in range(len(v)):
        h_solve = newton(lambda h: nc(h, v[i], parameters, hs=hs), 0)  # calculate h value where dv=0
        nv[i] = h_solve

    return nv


def nc(h, v, parameters, hs=1):  # maybe take from diffeq d=5
    I, gNa, gK, gl, ENa, Ek, El, *_ = parameters
    return I - gl * (v - El) - gK * (f(h) ** 3) * (v - Ek) - gNa * h * hs * (m_inf(v) ** 3) * (v - ENa)
