from scipy.integrate import odeint

from helpers.nullclines import nullcline_h, nullcline_v
from helpers.plotting import *
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_2d
from ode_functions.gating import *


def run():
    __figure2a__()
    __figure2b__()


def __figure2a__():
    ic = [-35, 1]
    t_solved = np.array([])
    solution = np.array([0, 0])
    currents = [0, 3.5]
    times = [2000, 3000]
    t0 = 0

    for ix, I_app in enumerate(currents):
        t = np.arange(t0, times[ix], 0.1)
        t0 = times[ix]
        t_solved = np.concatenate((t_solved, t))

        parameters = default_parameters(i_app=I_app)
        state = odeint(ode_2d, ic, t, args=(parameters,))
        ic = state[-1, :]

        solution = np.vstack((solution, state))

    solution = solution[1:, :]  # TODO: hack for starting shape

    stimulus = np.zeros(t_solved.shape)
    stimulus[t_solved > times[0]] = currents[1]

    init_figure(size=(5, 3))
    plt.subplot(2, 1, 1)
    plt.plot(t_solved, solution[:, 0], "k")
    set_properties(y_label="V (mV)", y_tick=[-40, -20, 0, 20])

    plt.subplot(2, 1, 2)
    plt.plot(t_solved, stimulus, "k")
    set_properties(None)

    save_fig('2A')


def __figure2b__():
    i_app_list = [0, 3.5]
    v = np.arange(-90, 50)
    nh = nullcline_h(v)
    init_figure(size=(5, 3))
    for ix, I_app in enumerate(i_app_list):
        plt.subplot(121 + ix)
        plt.plot(v, nh, 'k')
        nv = nullcline_v(v, I_app)

        plt.plot(v, nv, '--', color='grey')
        style = 'k' if ix == 1 else 'none'
        cross_index = np.argmin(np.abs(nv - nh))
        plt.scatter(v[cross_index], nv[cross_index], edgecolors='k', facecolors=style)

        set_properties(x_label="v (mV)", y_label="h", x_tick=[-50, 0, 50], y_tick=[0, 0.1, 0.2, 0.3, 0.4],
                       x_limits=[-75, 50], y_limits=[0, 0.4])

    save_fig("2B")
