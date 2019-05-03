from scipy.integrate import odeint
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.diff_eq import ode_2d, ode_3d
from ode_functions.defaults import default_parameters

ode_functions = [ode_2d, ode_3d]
I_list = np.arange(-5, 5, 0.01)  #uA/cm^2
t = np.arange(0, 2000, 0.1)

vmax_all = np.zeros(len(I_list))
vmin_all = np.zeros(len(I_list))

for ix, ode_function in enumerate(ode_functions):
    for i, I in enumerate(I_list):
        parameters=default_parameters(I_app=I)
        state0= [-60, 0] + ix*[0] # v_list,h, hs

        state = odeint(ode_function, state0, t, args=(parameters,))

        I_point = np.ceil(3 * len(t) / 4)
        state4 = state[int(I_point):, :]
        v = state4[:, 0]
        vmax = np.max(v)
        vmin = np.min(v)
        vmax_all[i] = vmax
        vmin_all[i] = vmin

    plt.figure()
    if ix == 0:
        plt.xlim(-5,5)
        plt.ylim(-100,40)
    else:
        plt.xlim(-0.1,0.2)
        plt.ylim(-80, 100)
    plt.plot(I_list,vmax_all, c="black")
    plt.plot(I_list, vmin_all, c="black")
    plt.ylim(-80, 40)
