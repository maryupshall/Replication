from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.diff_eq import ode_5d, ode_3d
from ode_functions.defaults import default_parameters

# Parameter values
ode_functions = [ode_3d, ode_5d]
parameters = default_parameters()

t = np.arange(0, 4300, 0.01)

for ix, ode_function in enumerate(ode_functions):
    state0 = [-55, 0, 0] + ix*[0, 0]

    state = odeint(ode_function, state0, t, args=(parameters,), atol=1e-3)

    plt.figure()
    plt.plot(t, state[:, 0])

    plt.ylim(-80, 20)
    plt.xlim(-20, 4300)