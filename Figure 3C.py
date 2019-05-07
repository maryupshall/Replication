from scipy.integrate import odeint
from ode_functions.gating import *
from ode_functions.diff_eq import hs_clamp, ode_3d
from ode_functions.defaults import default_parameters
from plotting import *

parameters=default_parameters(I_app=0.16)
t = np.arange(0, 10000, 0.1)

state0 = [-60, 0, 1]  # v_list, h, & hs_list

state = odeint(ode_3d, state0, t, args=(parameters,))  # pre-stimulus solution

# TRAJECTORY:
trajectory = state

hs = np.arange(0, 1, 0.05)

vmax_all = np.zeros(len(hs))
vmin_all = np.zeros(len(hs))

# Bifurcation:
for i in range(len(hs)):
    state0 = [-55, 0, hs[i]]
    parameters = default_parameters(I_app=0.16)

    state = odeint(hs_clamp, state0, t, args=(parameters,))

    h_point = np.ceil(3 * len(t) / 4)
    state4 = state[int(h_point):, :]
    v = state4[:, 0]
    vmax = np.max(v)
    vmin = np.min(v)
    vmax_all[i] = vmax
    vmin_all[i] = vmin

plt.plot(hs, vmax_all, "--", c="black")
plt.plot(hs, vmin_all, "--", c="black")
plt.plot(trajectory[:, 2], trajectory[:, 0])
set_properties(xlabel="h$_{s}$", ylabel= "v (mV)", xtick= [0, 0.2, 0.4, 0.6, 0.8, 1], ytick= [-80, -40, 0, 40])


