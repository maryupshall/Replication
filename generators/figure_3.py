from scipy.integrate import odeint

from helpers.nullclines import nullcline_v, nullcline_h
from helpers.plotting import *
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import hs_clamp
from ode_functions.diff_eq import ode_3d
from ode_functions.gating import *


def run():
    __figure3a__()
    __figure3b__()
    __figure3c__()
    __figure3d__()


def __figure3a__():
    ic = [-55, 0, 0]
    t_solved = np.array([])
    solution = np.array([0, 0, 0])
    currents = [0, 0.16]
    t0 = 0
    times = [2000, 6000]

    for ix, I_app in enumerate(currents):
        t = np.arange(t0, times[ix], 0.1)
        t_solved = np.concatenate((t_solved, t))
        t0 = times[ix]

        parameters = default_parameters(i_app=I_app)
        state = odeint(ode_3d, ic, t, args=(parameters,))
        ic = state[-1, :]

        solution = np.vstack((solution, state))

    solution = solution[1:, :]  # TODO: hack for starting shape

    stimulus = np.zeros(t_solved.shape)
    stimulus[t_solved > times[0]] = currents[1]

    init_figure(size=(5, 3))

    plt.subplot(3, 1, 1)
    plt.plot(t_solved, solution[:, 0], 'k')
    set_properties(y_label='v (mV)', y_tick=[-60, -40, -20, 0, 20])

    plt.subplot(3, 1, 2)
    plt.plot(t_solved, (solution[:, 1]) * (solution[:, 2]), 'k')
    plt.plot(t_solved, solution[:, 2], "k--")
    set_properties(y_label='h$_{total}$, h$_s$', y_tick=[0, 0.2, 0.4, 0.6, 0.8])

    plt.subplot(3, 1, 3)
    plt.plot(t_solved, stimulus, 'k')
    set_properties(x_label='Time (ms)', y_label='I$_{app}$', y_tick=[0, 0.16], x_tick=np.arange(0, 8000, 2000))

    save_fig('3A')


def __figure3b__():
    i_app_list = [0, 0.16, 0.16, 0.16]
    hs_list = [0.6, 0.6, 0.2, 0.05]

    v = np.arange(-90, 50)
    nh = nullcline_h(v)

    init_figure(size=(8, 2))
    for ix, (I, hs) in enumerate(zip(i_app_list, hs_list)):
        plt.subplot(1, 4, ix + 1)
        plt.plot(v, nh, 'k')
        nv = nullcline_v(v, I, hs=hs)

        plt.plot(v, nv, '--', color='grey')
        style = 'k' if ix == 3 else 'none'
        cross_index = np.argmin(np.abs(nv - nh))
        plt.scatter(v[cross_index], nv[cross_index], edgecolors='k', facecolors=style)

        set_properties(x_label="v (mV)", y_label="h", x_tick=[-40, 40], y_tick=[0, 0.2, 0.4, 0.6, 0.8],
                       x_limits=(-80, 50),
                       y_limits=(0, 0.6))

    save_fig('3B')


def __figure3c__():
    parameters = default_parameters(i_app=0.16)
    t = np.arange(0, 10000, 1)
    ic = [-60, 0, 1]

    trajectory = odeint(ode_3d, ic, t, args=(parameters,))  # pre-stimulus solution

    hs = np.arange(0, 1, 0.05)

    v_max = np.zeros(len(hs))
    v_min = np.zeros(len(hs))

    for i in range(len(hs)):
        ic = [-55, 0, hs[i]]
        parameters = default_parameters(i_app=0.16)

        state = odeint(hs_clamp, ic, t, args=(parameters,))
        v = state[7500:, 0]
        v_max[i] = np.max(v)
        v_min[i] = np.min(v)

    init_figure(size=(5, 3))
    plt.plot(hs, v_max, "--", c="k")
    plt.plot(hs, v_min, "--", c="k")
    plt.plot(trajectory[:, 2], trajectory[:, 0], c='grey')

    set_properties(x_label="h$_{s}$", y_label="v (mV)", x_tick=[0, 0.2, 0.4, 0.6, 0.8, 1], y_tick=[-80, -40, 0, 40])
    save_fig("3C")


def __figure3d__():
    ic = [-65, 1, 1]
    t_solved = np.array([])
    solution = np.array([0, 0, 0])
    currents = [0, 0.16]
    times = [2000, 10000]
    t0 = 0
    for ix, I_app in enumerate(currents):
        t = np.arange(t0, times[ix], 0.1)
        t_solved = np.concatenate((t_solved, t))
        t0 = times[ix]

        parameters = default_parameters(i_app=I_app)
        state = odeint(lambda s, _, p: ode_3d(s, _, p, scale=2), ic, t, args=(parameters,))
        ic = state[-1, :]

        solution = np.vstack((solution, state))

    solution = solution[1:, :]  # TODO: hack for starting shape

    stimulus = np.zeros(t_solved.shape)
    stimulus[t_solved > times[0]] = currents[1]

    init_figure(size=(5, 3))

    plt.subplot(2, 1, 1)
    plt.plot(t_solved, solution[:, 0], 'k')
    set_properties(y_label='$V_m$ (mV)', y_tick=[-40, 0], y_limits=(-80, 20))

    plt.subplot(2, 1, 2)
    plt.plot(t_solved, stimulus, 'k')
    set_properties()

    save_fig('3D')
