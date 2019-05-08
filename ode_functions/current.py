from ode_functions.gating import f, m_inf


def INa(v, m, parameters, h=1, hs=1):
    gNa = parameters[1]
    ENa = parameters[4]
    return gNa * (v - ENa) * (m ** 3) * h * hs


def I_na_hack(v, h, parameters, hs=1):
    I, gNa, gK, gl, ENa, Ek, El, *_ = parameters
    return - (gl * (v - El)) - (gNa * (m_inf(v) ** 3) * h * hs * (v - ENa)) - (
            gK * (f(h[-1]) ** 3) * (v - Ek))
