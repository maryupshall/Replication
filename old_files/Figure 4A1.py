from scipy.optimize import newton
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.defaults import default_parameters
from ode_functions.current import nc



#Parameter values

parameters = default_parameters(I_app= 0)

vmin = -90
vmax = 50
vstep = 1
v = np.arange(vmin, vmax, vstep)

# dh nullcline:
dh_null = (h_inf(v))
plt.plot(v, dh_null)


# dv nullcline:

null_solve = np.zeros((len(v), 2))

for i in range(len(v)):
    opt_fcn = lambda h: nc(h, v[i], parameters)
    h_solve = newton(opt_fcn, 0)  # calculate h value where dv=0

    # print(h_solve)

    null_solve[i, 0] = v[i]
    null_solve[i, 1] = h_solve

plt.plot(null_solve[:, 0], null_solve[:, 1], c="red")

parameters=default_parameters(I_app=3.5)

null_solve = np.zeros((len(v), 2))

for i in range(len(v)):
    opt_fcn = lambda h: nc(h, v[i], parameters)
    h_solve = newton(opt_fcn, 0)  # calculate h value where dv=0

    # print(h_solve)

    null_solve[i, 0] = v[i]
    null_solve[i, 1] = h_solve

plt.plot(null_solve[:, 0], null_solve[:, 1], c="red")

plt.ylim(0, 0.15)
plt.xlim(-40, 5)
plt.xlabel("v_list (mV)")
plt.ylabel("h")
plt.legend(["h nullcline", "v_list nullcline (I_list=0, 3.5)"])