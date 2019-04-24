from scipy.optimize import newton
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.diff_eq import ode_2d


#Parameter values

I = np.arange(-5, 5, 0.05)  #uA/cm^2
gNa= 8 #mS/cm^2
gK=0.6 #mS/cm^2
gl=0.013 #mS/cm^2
ENa=60 #mV
Ek=-85 #mV
El=-60 #mV

parameters=[I,gNa,gK,gl,ENa,Ek,El]

tmax = 1000  # ms
dt = 0.1
t = np.arange(0, tmax, dt)

vmax_all = np.zeros(len(I))
vmin_all = np.zeros(len(I))

# Bifurcation:
for i in range(len(I)):
    initial_state = [-55, 0]  # v_list,h
    state0 = initial_state

    parameters = [I[i], gNa, gK, gl, ENa, Ek, El]
    state = odeint(ode_2d, state0, t, args=(parameters,))

    I_point = np.ceil(3 * len(t) / 4)
    state4 = state[int(I_point):, :]
    v = state4[:, 0]
    vmax = np.max(v)
    vmin = np.min(v)
    vmax_all[i] = vmax
    vmin_all[i] = vmin

plt.plot(I, vmax_all, c="black")
plt.plot(I, vmin_all, c="black")
plt.ylim(-80, 40)

