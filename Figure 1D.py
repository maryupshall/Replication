from scipy.integrate import odeint
from ode_functions.gating import *
from ode_functions.diff_eq import ode_5d, ode_3d
from ode_functions.defaults import default_parameters
from plotting import *

# Parameter values
ode_functions = [ode_3d, ode_5d]
parameters = default_parameters()

t = np.arange(0, 4300, 0.01)

for ix, ode_function in enumerate(ode_functions):
    state0 = [-55, 0, 0] + ix*[0, 0]

    state = odeint(ode_function, state0, t, args=(parameters,), atol=1e-3)

    plt.subplot(2,1,ix+1)
    if ix == 0:
        plt.title("D1")
    else:
        plt.title("D2")
    plt.plot(t, state[:, 0], "k")

    set_properties(ylabel="v (mV)", ytick= [-80, -40 , 0])