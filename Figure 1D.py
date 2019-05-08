from scipy.integrate import odeint

from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_5d, ode_3d
from ode_functions.gating import *
from helpers.plotting import *

ode_functions = [ode_3d, ode_5d]
parameters = default_parameters()
t = np.arange(0, 4300, 0.01)

init_figure(size=(5, 3))
for ix, ode_function in enumerate(ode_functions):
    ic = [-55, 0, 0] + ix * [0, 0]
    state = odeint(ode_function, ic, t, args=(parameters,), atol=1e-3)

    plt.subplot(2, 1, ix + 1)
    plt.plot(t, state[:, 0], "k")

    set_properties(ylabel="v (mV)", ytick=[-80, -40, 0])

save_fig('1D')
