import numpy as np


# Boltzmann functions
def m_inf(v):
    mhalf = -30.0907  # mV
    mslope = 9.7264  # mV
    return 1 / (1 + np.exp(-(v - mhalf) / mslope))


def h_inf(v):
    hhalf = -54.0289  # mV
    hslope = -10.7665  # mV
    return 1 / (1 + np.exp(-(v - hhalf) / hslope))


def hs_inf(v):
    hshalf = -54.8  # mV
    hsslope = -1.57  # mV
    return 1 / (1 + np.exp(-(v - hshalf) / hsslope))


def n_inf(v):
    nhalf = -25  # mV
    nslope = 12  # mV
    return 1 / (1 + np.exp(-(v - nhalf) / nslope))


# Time constants (ms)

def Th(v):
    a = 0.00050754 * np.exp(-0.063213 * v)
    b = 9.7529 * np.exp(0.13442 * v)

    return 0.4 + 1 / (a + b)  # ms


def Ths(v):
    return 20 + 160 / (1 + np.exp((v + 47.2) / 1))  # ms


def Tm(v):
    a = -(15.6504 + (0.4043 * v)) / (np.exp(-19.565 - (0.50542 * v)) - 1)
    b = 3.0212 * np.exp(-0.0074630 * v)

    return 0.01 + 1 / (a + b)


def Tn(v):
    # return 1 + 19 * np.exp((-(np.log(1 + 0.05 * (v_list + 40)) / 0.05) ** 2) / 300)
    return 1 + 19 * np.exp((-(np.log(1 + 0.05 * (v + 60)) / 0.05) ** 2) / 300)


# variable n as a function of h
def f(h): # TODO:confirm
    a0 = 0.8158
    a1 = -3.8768
    a2 = 6.8838
    a3 = -4.2079

    fh = np.asarray(a0 + a1 * h + a2 * (h ** 2) + a3 * (h ** 3))

    fh[fh<0] = 0
    fh[fh>1]=1

    return fh
