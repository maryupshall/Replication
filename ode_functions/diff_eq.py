from ode_functions.gating import *


def ode_2d(state, t, parameters):
    i_app, g_na, g_k, g_l, e_na, e_k, e_l = parameters
    v, h = state
    n = f(h)

    dv = i_app - g_l * (v - e_l) - g_na * (m_inf(v) ** 3) * h * (v - e_na) - g_k * ((n ** 3) * (v - e_k))
    dh = - (h - (h_inf(v))) / (tau_h(v))

    return [dv, dh]


def ode_3d(state, t, parameters, synapse=None, scale=1):
    i_app, g_na, g_k, g_l, e_na, e_k, e_l, *p_synapse = parameters
    v, h, hs = state
    n = f(h)

    i_syn = 0 if synapse is None else synapse(v, p_synapse)

    dv = i_app - (g_l * (v - e_l)) - (g_na * (m_inf(v) ** 3) * h * hs * (v - e_na)) - (
            g_k * (n ** 3) * (v - e_k)) - i_syn
    dh = - (h - (h_inf(v))) / (tau_h(v))
    dhs = - (hs - (hs_inf(v))) / (tah_hs(v)) * scale

    return [dv, dh, dhs]


def synaptic_3d(state, t, parameters):
    *p, func = parameters

    return ode_3d(state, t, p, synapse=func)


def ode_5d(state, t, parameters):
    i_app, g_na, g_k, g_l, e_na, e_k, e_l = parameters
    v, h, hs, m, n = state

    dv = i_app - g_l * (v - e_l) - g_na * (m ** 3) * h * hs * (v - e_na) - g_k * (n ** 3) * (v - e_k)  # 3D model
    dh = - (h - (h_inf(v))) / (tau_h(v))
    dhs = - (hs - (hs_inf(v))) / (tah_hs(v))
    dm = - (m - (m_inf(v))) / (tau_m(v))
    dn = - (n - (n_inf(v))) / (tau_n(v))

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
