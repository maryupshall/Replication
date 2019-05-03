import numpy as np
from ode_functions.gating import *


def ode_2d(state, t, parameters):
    I, gNa, gK, gl, ENa, Ek, El = parameters
    v, h = state
    n = f(h)

    dv = I - gl * (v - El) - gNa * (m_inf(v) ** 3) * h * (v - ENa) - gK * ((n ** 3) * (v - Ek))  # 2D model
    dh = - (h - (h_inf(v))) / (Th(v))

    return [dv, dh]


def ode_3d(state, t, parameters, synapse=None, scale=1):
    I, gNa, gK, gl, ENa, Ek, El, *p_synapse = parameters
    v, h, hs = state
    n = f(h)

    i_syn = 0 if synapse is None else synapse(v, p_synapse)

    dv = I - (gl * (v - El)) - (gNa * (m_inf(v) ** 3) * h * hs * (v - ENa)) - (
                gK * (n ** 3) * (v - Ek)) - i_syn  # 3D model
    dh = - (h - (h_inf(v))) / (Th(v))
    dhs = - (hs - (hs_inf(v))) / (Ths(v)) * scale

    return [dv, dh, dhs]


def synaptic_3d(state, t, parameters):
    *p, func = parameters

    return ode_3d(state, t, p, synapse=func)


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
    return __clamp__(state, t, p, func, 0)


def hs_clamp(state, t, parameters):
    return __clamp__(state, t, parameters, ode_3d, 2)


def __clamp__(state, t, p, func, ix):
    ddt = func(state, t, p)
    ddt[ix] = 0
    return ddt


def I_NMDA(v, p, Mg=1.4):
    gNmda, Enmda = p
    return (gNmda * (v - Enmda)) / (1 + (Mg / 3.57) * np.exp(0.062 * v))


def I_AMPA(v, p):
    gAmpa, EAmpa = p
    return gAmpa * (v - EAmpa)
