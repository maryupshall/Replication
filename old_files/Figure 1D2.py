from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.diff_eq import ode_3d
from ode_functions.defaults import default_parameters


# Parameter values
parameters = default_parameters()


tmax = 2200
dt = 0.001  # time step
t = np.arange(0, tmax, dt)

state0 = [-55, 1, 1]  # v_list, h, hs_list

state = odeint(ode_3d, state0, t, args=(parameters,))

plt.plot(t, state[:, 0])

plt.ylim(-80, 20)
plt.xlim(-20, 2300)
plt.ylabel("v_list(mv)")