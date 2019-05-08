from scipy.integrate import odeint

from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_5d
from ode_functions.gating import *
from helpers.plotting import *

parameters = default_parameters()

t = np.arange(0, 4200, 0.01)
ic = [-55, 0, 0, 0, 0]
state = odeint(ode_5d, ic, t, args=(parameters,), rtol=1e-6, atol=1e-6)

h = state[200000:, 1]
n = state[200000:, 4]

init_figure(size=(5, 3))
plt.plot(h, n, c="grey")
plt.plot(h, list(map(f, h)), "k")
set_properties(xlabel="h", ylabel="n", xtick=[0, 0.2, 0.4, 0.6], ytick=np.arange(0, 1, 0.2))
plt.legend(["n", "n=f(h)"])
save_fig("1C")
