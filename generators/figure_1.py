from scipy.integrate import odeint

from helpers.plotting import *
from ode_functions.current import sodium_current
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_3d, voltage_clamp
from ode_functions.diff_eq import ode_5d
from ode_functions.gating import *


def run():
    __figure1a__()
    __figure1b__()
    __figure1c__()
    __figure1d__()


def __figure1a__():
    parameters = default_parameters(g_na=0.00000592 / 2)  # need to divide given value by 2 to get correct graph
    parameters.append(ode_3d)

    v = np.arange(-100, 60, 0.5)
    current = list(map(lambda x: 1e6 * np.max(sodium_current(x, m_inf(x), parameters)), v))

    init_figure(size=(5, 3))
    plt.plot(v, current, 'k')
    set_properties(x_label="V (mV)", y_label="peak I$_{Na}$", x_tick=[-80, -40, 0, 40], y_tick=[-160, 0])
    save_fig('1A')


def __figure1b__():
    clamp_current = np.array([])
    all_time = np.array([])

    packet = [[-100, 0],
              [0, 3],
              [3, 100],
              [100, 103],
              [103, 200],
              [200, 203],
              [203, 300],
              [300, 303],
              [303, 400],
              [400, 403],
              [403, 500],
              [500, 503],
              [503, 600]]  # TODO: programmatically generate +100, +3, +100, +3?

    parameters = default_parameters(g_na=0.00000912)  # need to divide given value by 2 to get correct graph
    parameters.append(ode_3d)
    ic = [-70, 0, 0]
    for (t0, t1) in packet:
        time = np.arange(t0, t1, 0.05)  # off
        all_time = np.concatenate((all_time, time))

        state = odeint(voltage_clamp, ic, time, args=(parameters,))
        v = state[:, 0]
        h = state[:, 1]
        hs = state[:, 2]
        clamp_current = np.concatenate((clamp_current, sodium_current(v, m_inf(v), parameters, h=h, hs=hs)))
        if ic[0] == -70:
            ic = [0, h[-1], hs[-1]]
        else:
            ic = [-70, h[-1], hs[-1]]

    init_figure(size=(5, 3))
    plt.plot(all_time, 1e6 * clamp_current, 'k')
    set_properties(x_label="time (ms)", y_label="I$_{Na}$ (pA)", x_tick=[0, 200, 400], y_tick=[-200, 0],
                   x_limits=[-50, 600])
    save_fig("1B")


def __figure1c__():
    parameters = default_parameters()

    t = np.arange(0, 4200, 0.01)
    ic = [-55, 0, 0, 0, 0]
    state = odeint(ode_5d, ic, t, args=(parameters,), rtol=1e-6, atol=1e-6)

    h = state[200000:, 1]
    n = state[200000:, 4]

    init_figure(size=(5, 3))
    plt.plot(h, n, c="grey")
    plt.plot(h, list(map(f, h)), "k")
    set_properties(x_label="h", y_label="n", x_tick=[0, 0.2, 0.4, 0.6], y_tick=np.arange(0, 1, 0.2))
    plt.legend(["n", "n=f(h)"])
    save_fig("1C")


def __figure1d__():
    ode_functions = [ode_3d, ode_5d]
    parameters = default_parameters()
    t = np.arange(0, 4300, 0.01)

    init_figure(size=(5, 3))
    for ix, ode_function in enumerate(ode_functions):
        ic = [-55, 0, 0] + ix * [0, 0]
        state = odeint(ode_function, ic, t, args=(parameters,), atol=1e-3)

        plt.subplot(2, 1, ix + 1)
        plt.plot(t, state[:, 0], "k")

        set_properties(y_label="v (mV)", y_tick=[-80, -40, 0])

    save_fig('1D')
