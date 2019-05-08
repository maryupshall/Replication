from scipy.integrate import odeint

from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import hs_clamp, ode_3d
from ode_functions.gating import *
from helpers.plotting import *

parameters = default_parameters(I_app=0.16)
t = np.arange(0, 10000, 1)
ic = [-60, 0, 1]

trajectory = odeint(ode_3d, ic, t, args=(parameters,))  # pre-stimulus solution

hs = np.arange(0, 1, 0.05)

vmax_all = np.zeros(len(hs))
vmin_all = np.zeros(len(hs))

for i in range(len(hs)):
    ic = [-55, 0, hs[i]]
    parameters = default_parameters(I_app=0.16)

    state = odeint(hs_clamp, ic, t, args=(parameters,))
    v = state[7500:, 0]

    vmax = np.max(v)
    vmin = np.min(v)
    vmax_all[i] = vmax
    vmin_all[i] = vmin

init_figure(size=(5, 3))
plt.plot(hs, vmax_all, "--", c="k")
plt.plot(hs, vmin_all, "--", c="k")
plt.plot(trajectory[:, 2], trajectory[:, 0], c='grey')

set_properties(xlabel="h$_{s}$", ylabel="v (mV)", xtick=[0, 0.2, 0.4, 0.6, 0.8, 1], ytick=[-80, -40, 0, 40])
save_fig("3C")
