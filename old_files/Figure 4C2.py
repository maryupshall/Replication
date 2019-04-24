#monotonic I_list-V curve for 3D model

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.diff_eq import ode_3d, voltage_clamp


#Parameter values

I=0
gNa= 8 #mS/cm^2
gK=0.6 #mS/cm^2
gl=0.013 #mS/cm^2
ENa=60 #mV
Ek=-85 #mV
El=-60 #mV

parameters=[I,gNa,gK,gl,ENa,Ek,El,ode_3d]

vmin = -100
vmax = 60
vstep = 0.5
v = np.arange(vmin, vmax, vstep)

tmax = 1000  # ms
dt = 0.1
t = np.arange(0, tmax, dt)

membrane_current = np.zeros(len(v))

# Bifurcation:
for i in range(len(v)):
    initial_state = [v[i], 0, 0]  # v_list, h, hs_list
    state0 = initial_state

    state = odeint(voltage_clamp, state0, t, args=(parameters,))
    h = state[:, 1]
    hs = state[:, 2]
    membrane_I = - (gl * (v[i] - El)) - (gNa * (m_inf(v[i]) ** 3) * h[-1] * hs[-1] * (v[i] - ENa)) - (
                gK * (f(h[-1]) ** 3) * (v[i] - Ek))

    v_clamp = v
    membrane_current[i] = -membrane_I

plt.plot(v_clamp, membrane_current)
plt.xlim(-70, -50)
plt.ylim(-0.1, 0.2)
plt.xlabel("Voltage (mv)")
plt.ylabel("I_list (uA/cm^2)")