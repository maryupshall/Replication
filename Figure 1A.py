from scipy.integrate import odeint
from ode_functions.gating import *
from ode_functions.diff_eq import ode_3d, voltage_clamp
from ode_functions.defaults import default_parameters
from ode_functions.current import INa
from plotting import *


parameters = default_parameters(gNa=0.00000592 / 2)  # need to divide given value by 2 to get correct graph
parameters.append(ode_3d)

vmin = -100
vmax = 60
vstep = 0.5
v = np.arange(vmin, vmax, vstep)

tmax = 1000  # ms
dt = 0.1
t = np.arange(0, tmax, dt)

Na_current = np.zeros(len(v))

for i in range(len(v)):
    initial_state = [v[i], 0, 0]  # v_list, h, hs_list
    state0 = initial_state

    state = odeint(voltage_clamp, state0, t, args=(parameters,))
    h = state[:, 1]
    hs = state[:, 2]
    I_Na = INa(v[i], m_inf(v[i]), parameters)
    # (parameters[1] * (m_inf(v_list[i]) ** 3) * (v_list[i] - parameters[4]))  # without h & hs_list
    # I_Na= (parameters[1]*(m_inf(v_list[i])**3)*h[-1]*hs_list[-1]*(v_list[i]-parameters[4])) #with h & hs_list doesn't work

    v_clamp = v
    I_Na_max = np.max(I_Na)
    Na_current[i] = I_Na_max

plt.plot(v_clamp, Na_current*1e6)
set_properties(xlabel="v (mV)", ylabel="peak I$_{Na}$", xtick=[-80,-40,0,40], ytick= [-160, 0])

