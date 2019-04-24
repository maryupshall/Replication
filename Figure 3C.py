from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.diff_eq import ode_3d



#Parameter values

parameters=[I,gNa,gK,gl,ENa,Ek,El]

tmax = 10000  # ms
dt = 0.1
t = np.arange(0, tmax, dt)

initial_state = [-60, 0, 1]  # v_list, h, & hs_list

state0 = initial_state
state = odeint(ode_3d, state0, t, args=(parameters,))  # pre-stimulus solution

# TRAJECTORY:
state5 = state


def ode_3d(state, t, parameters):
    I = parameters[0]
    gNa = parameters[1]
    gK = parameters[2]
    gl = parameters[3]
    ENa = parameters[4]
    Ek = parameters[5]
    El = parameters[6]
    hs = parameters[7]

    v = state[0]
    h = state[1]

    n = f(h)

    dv = I - (gl * (v - El)) - (gNa * (m_inf(v) ** 3) * h * hs * (v - ENa)) - (gK * (n ** 3) * (v - Ek))  # 3D model
    dh = - (h - (h_inf(v))) / (Th(v))

    return [dv, dh]


I = 0.16  # uA/cm^2
gNa = 8  # mS/cm^2
gK = 0.6  # mS/cm^2
gl = 0.013  # mS/cm^2
ENa = 60  # mV
Ek = -85  # mV
El = -60  # mV

hs_min = 0
hs_max = 1
hs_step = 0.05
hs = np.arange(hs_min, hs_max, hs_step)

tmax = 1000  # ms
dt = 0.1
t = np.arange(0, tmax, dt)

vmax_all = np.zeros(len(hs))
vmin_all = np.zeros(len(hs))

# Bifurcation:
for i in range(len(hs)):
    initial_state = [-55, 0]
    state0 = initial_state

    parameters = [I, gNa, gK, gl, ENa, Ek, El, hs[i]]
    state = odeint(ode_3d, state0, t, args=(parameters,))

    h_point = np.ceil(3 * len(t) / 4)
    state4 = state[int(h_point):, :]
    # hs4=np.full(len(state4),hs_list[i])
    v = state4[:, 0]
    vmax = np.max(v)
    vmin = np.min(v)
    vmax_all[i] = vmax
    vmin_all[i] = vmin

plt.plot(hs, vmax_all, "--", c="black")
plt.plot(hs, vmin_all, "--", c="black")
plt.plot(state5[:, 2], state5[:, 0])

