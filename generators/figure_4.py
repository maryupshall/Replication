import warnings

from scipy.integrate import odeint

from helpers.nullclines import nullcline_h, nullcline_v
from helpers.plotting import *
from ode_functions.current import sodium_current_hack
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_2d, ode_3d, voltage_clamp
from ode_functions.gating import *


def run():
    __figure4a__()
    __figure4b__()
    __figure4c__()


def __figure4a__():
    i_app_list_set = [[0, 3.5], [0.16, 0.16, 0.16]]
    hs_list_set = [[1, 1], [0.6, 0.2, 0.05]]
    v = np.arange(-90, 50)

    nh = nullcline_h(v)

    init_figure(size=(5, 3))
    for ix, (i_app_list, hs_list) in enumerate(zip(i_app_list_set, hs_list_set)):
        plt.subplot(1, 2, ix + 1)
        plt.plot(v, nh, 'g')
        for iy, (I, hs) in enumerate(zip(i_app_list, hs_list)):
            nv = nullcline_v(v, I, hs=hs)
            plt.plot(v, nv, 'r')

        if ix == 0:
            set_properties(x_label="v (mV)", y_label="h", x_tick=[-40, 0], y_tick=[0, 0.05, 0.1, 0.15],
                           x_limits=(-40, 5),
                           y_limits=(0, 0.15))
        else:
            set_properties(x_label="v (mV)", y_label="h", x_tick=[-60, 20], y_tick=[0, 0.2, 0.4], x_limits=(-80, 20),
                           y_limits=(0, 0.4))

    save_fig('4A')


def __figure4b__():
    warnings.warn('Figure 4b not implemented')


def __figure4c__():
    ode_functions = [ode_2d, ode_3d]
    v_list = np.arange(-100, 20, 0.5)
    t = np.arange(0, 1000, 0.1)

    membrane_current = np.zeros(len(v_list))
    parameters = default_parameters()
    parameters.append(None)

    init_figure(size=(5, 3))
    for ix, ode_function in enumerate(ode_functions):
        parameters[-1] = ode_function

        for i in range(len(v_list)):
            initial_state = [v_list[i], 0] + ix * [0]

            state = odeint(voltage_clamp, initial_state, t, args=(parameters,))
            h = state[:, 1]
            v = state[:, 0]
            hs = 1 if np.shape(state)[1] == 2 else state[:, 2]

            membrane_current[i] = -sodium_current_hack(v, h, parameters, hs=hs)[-1]
        plt.subplot(1, 2, 1 + ix)
        plt.plot(v_list, membrane_current, 'k')
        plt.plot(v_list, v_list * [0], '--', color='grey')

        if ix == 0:
            set_properties(x_label="Voltage (mV)", y_label="I$_{stim} ( \mu A/cm^{2}$)", x_tick=[-80, -40],
                           y_tick=[-5, 0, 5],
                           x_limits=(-100, -20), y_limits=(-5, 5))
        else:
            set_properties(x_label="Voltage (mV)", y_label="I$_{stim} ( \mu A/cm^{2}$)", x_tick=[-70, -60, -50],
                           y_tick=[-0.1, 0, 0.1, 0.2], x_limits=(-70, -50), y_limits=(-0.1, 0.2))

    save_fig("4C")
