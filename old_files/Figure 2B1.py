##Where I_list=0 uA/cm^2

from scipy.optimize import newton
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.defaults import default_parameters
from ode_functions.current import nc

#Parameter values
parameters = default_parameters()

vmin = -90
vmax = 50
vstep = 1
v = np.arange(vmin, vmax, vstep)

# dh nullcline:
dh_null = (h_inf(v))
plt.plot(v, dh_null)


# dv nullcline:

# def nc(h, v_list):  # function to pass h and v_list to
#     I_list, gNa, gK, gl, ENa, Ek, El = parameters
#     return I_list - gl * (v_list - El) - gK * (f(h) ** 3) * (v_list - Ek) - gNa * h * (m_inf(v_list) ** 3) * (v_list - ENa)
#

null_solve = np.zeros((len(v), 2))

for i in range(len(v)):
    opt_fcn = lambda h: nc(h, v[i], parameters)
    h_solve = newton(opt_fcn, 0)  # calculate h value where dv=0

    null_solve[i, 0] = v[i]
    null_solve[i, 1] = h_solve

plt.plot(null_solve[:, 0], null_solve[:, 1])

plt.ylim(0, 0.4)
plt.xlim(-80, 50)
plt.xlabel("v_list (mV)")
plt.ylabel("h")




