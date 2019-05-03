from scipy.optimize import newton
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.defaults import default_parameters
from ode_functions.current import nc

I_list_set=[[0,3.5],[0.16,0.16,0.16]]
hs_list_set=[[1,1],[0.6,0.2,0.05]]
v = np.arange(-90, 50)

dh_null = (h_inf(v))
null_solve = np.zeros((len(v), 2))

for figure_ix, (I_list, hs_list) in enumerate(zip(I_list_set, hs_list_set)):
    plt.figure()
    for ix, (I, hs) in enumerate(zip(I_list, hs_list)):
        print(hs)
        parameters = default_parameters(I_app=I)
        plt.plot(v, dh_null)

        for i in range(len(v)):
            h_solve = newton(lambda h: nc(h, v[i], parameters, hs=hs), 0)  # calculate h value where dv=0

            null_solve[i, 0] = v[i]
            null_solve[i, 1] = h_solve

        plt.plot(null_solve[:, 0], null_solve[:, 1], c="red")

    if figure_ix == 0:
        plt.xlim(-40, 5)
        plt.ylim([0, 0.15])
    else:
        plt.xlim(-80,20)
        plt.ylim([0, 0.4])
    plt.xlabel("v_list (mV)")
    plt.ylabel("h")
    plt.legend(["h nullcline", "v_list nullcline (I_list=0, 3.5)"])