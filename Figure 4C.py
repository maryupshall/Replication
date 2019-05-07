from scipy.integrate import odeint
from ode_functions.gating import *
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_2d, ode_3d, voltage_clamp
from ode_functions.current import I_na_hack
from plotting import *

ode_functions = [ode_2d, ode_3d]

v_list = np.arange(-100, 20, 0.5)

tmax = 1000  # ms
dt = 0.1
t = np.arange(0, tmax, dt)

membrane_current = np.zeros(len(v_list))

for ix, ode_function in enumerate(ode_functions):
    parameters = default_parameters()
    parameters.append(ode_function)

    for i in range(len(v_list)):
        initial_state = [v_list[i], 0] + ix*[0] # tack on extra 0 for 3d model

        state = odeint(voltage_clamp, initial_state, t, args=(parameters,))
        h = state[:, 1]
        v = state[:, 0]
        hs = 1 if state.shape[1] == 2 else state[:, 2]

        membrane_current[i] = -I_na_hack(v, h, parameters, hs=hs)[-1]

    plt.figure()
    plt.plot(v_list, membrane_current)
    if ix == 0:
        set_properties(xlabel= "Voltage (mV)", ylabel= "I$_{stim} ( \mu A/cm^{2}$)", xtick=[-80, -40], ytick=[-5,0,5], xlim=(-100, -20), ylim=(-5, 5))
        plt.title("C1 Nonmonotonic IV curve")
    else:
        set_properties(xlabel= "Voltage (mV)", ylabel= "I$_{stim} ( \mu A/cm^{2}$)", xtick=[-70, -60, -50], ytick=[-0.1,0,0.1,0.2], xlim=(-70, -50), ylim=(-0.1, 0.2))
        plt.title("C2 Monotonic IV curve")

