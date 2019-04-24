
#nonmonotonic I_list-V curve for 2D model

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_2d, voltage_clamp
from ode_functions.current import I_na_hack


#Parameter values
parameters= default_parameters()
parameters.append(ode_2d)
#parameters=[I,gNa,gK,gl,ENa,Ek,El,ode_2d]


vmin = -100
vmax = 60
vstep = 0.5
v_list = np.arange(vmin, vmax, vstep)

tmax = 1000  # ms
dt = 0.1
t = np.arange(0, tmax, dt)

membrane_current = np.zeros(len(v_list))

# Bifurcation:
for i in range(len(v_list)):
    initial_state = [v_list[i], 0]  # v_list, h
    state0 = initial_state

    state = odeint(voltage_clamp, state0, t, args=(parameters,))
    h = state[:, 1]
    v = state[:,0 ]
    membrane_current[i]= -I_na_hack(v, h, parameters)[-1]

plt.plot(v_list, membrane_current)
plt.xlim(-100, 0)
plt.ylim([-5, 5])
plt.xlabel("Voltage (mv)")
plt.ylabel("I_list (uA/cm^2)")

