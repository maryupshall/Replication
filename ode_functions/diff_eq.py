import numpy as np
from ode_functions.gating import *


def ode_2d(state, t, parameters):
    I, gNa, gK, gl, ENa, Ek, El = parameters
    v, h = state
    n = f(h)

    dv = I - gl * (v - El) - gNa * (m_inf(v) ** 3) * h * (v - ENa) - gK * ((n ** 3) * (v - Ek))  # 2D model
    dh = - (h - (h_inf(v))) / (Th(v))

    return [dv, dh]


def ode_3d(state, t, parameters):
    I, gNa, gK, gl, ENa, Ek, El = parameters
    v, h, hs = state
    n = f(h)

    dv = I - (gl * (v - El)) - (gNa * (m_inf(v) ** 3) * h * hs * (v - ENa)) - (gK * (n ** 3) * (v - Ek))  # 3D model
    dh = - (h - (h_inf(v))) / (Th(v))
    dhs = - (hs - (hs_inf(v))) / (Ths(v))

    return [dv, dh, dhs]


def ode_5d(state, t, parameters):
    I, gNa, gK, gl, ENa, Ek, El = parameters
    v, h, hs, m, n = state

    dv = I - gl * (v - El) - gNa * (m ** 3) * h * hs * (v - ENa) - gK * ((n) ** 3) * (v - Ek)  # 3D model
    dh = - (h - (h_inf(v))) / (Th(v))
    dhs = - (hs - (hs_inf(v))) / (Ths(v))
    dm = - (m - (m_inf(v))) / (Tm(v))
    dn = - (n - (n_inf(v))) / (Tn(v))

    return [dv, dh, dhs, dm, dn]


def voltage_clamp(state, t, parameters):
    *p, func = parameters

    ddt = func(state, t, p)
    ddt[0] = 0

    return ddt
