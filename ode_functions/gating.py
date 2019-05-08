import numpy as np


def m_inf(v):
    m_half = -30.0907
    m_slope = 9.7264
    return 1 / (1 + np.exp(-(v - m_half) / m_slope))


def h_inf(v):
    h_half = -54.0289
    h_slope = -10.7665
    return 1 / (1 + np.exp(-(v - h_half) / h_slope))


def hs_inf(v):
    hs_half = -54.8
    hs_slope = -1.57
    return 1 / (1 + np.exp(-(v - hs_half) / hs_slope))


def n_inf(v):
    n_half = -25
    n_slope = 12
    return 1 / (1 + np.exp(-(v - n_half) / n_slope))


def tau_h(v):
    a = 0.00050754 * np.exp(-0.063213 * v)
    b = 9.7529 * np.exp(0.13442 * v)

    return 0.4 + 1 / (a + b)


def tah_hs(v):
    return 20 + 160 / (1 + np.exp((v + 47.2) / 1))


def tau_m(v):
    a = -(15.6504 + (0.4043 * v)) / (np.exp(-19.565 - (0.50542 * v)) - 1)
    b = 3.0212 * np.exp(-0.0074630 * v)

    return 0.01 + 1 / (a + b)


def tau_n(v):
    return 1 + 19 * np.exp((-(np.log(1 + 0.05 * (v + 60)) / 0.05) ** 2) / 300)


def f(h):
    a0 = 0.8158
    a1 = -3.8768
    a2 = 6.8838
    a3 = -4.2079

    fh = np.asarray(a0 + a1 * h + a2 * (h ** 2) + a3 * (h ** 3))

    fh[fh < 0] = 0
    fh[fh > 1] = 1

    return fh
