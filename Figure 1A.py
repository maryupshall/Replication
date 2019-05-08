from scipy.integrate import odeint

from ode_functions.current import INa
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_3d, voltage_clamp
from ode_functions.gating import *
from helpers.plotting import *

parameters = default_parameters(gNa=0.00000592 / 2)  # need to divide given value by 2 to get correct graph
parameters.append(ode_3d)

v = np.arange(-100, 60, 0.5)
t = np.arange(0, 1000, 0.1)

Na_current = np.zeros(len(v))

for i in range(len(v)):
    ic = [v[i], 0, 0]

    state = odeint(voltage_clamp, ic, t, args=(parameters,))
    I_Na = INa(v[i], m_inf(v[i]), parameters)

    Na_current[i] = np.max(I_Na) * 1e6

init_figure(size=(5, 3))
plt.plot(v, Na_current, 'k')
set_properties(xlabel="V (mV)", ylabel="peak I$_{Na}$", xtick=[-80, -40, 0, 40], ytick=[-160, 0])
save_fig('1A')
