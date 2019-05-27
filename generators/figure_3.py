import PyDSTool
from scipy.integrate import odeint
from sympy import *

from helpers.nullclines import nullcline_v, nullcline_h
from helpers.plotting import *
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import hs_clamp
from ode_functions.diff_eq import ode_3d
from ode_functions.gating import *


def run():
    init_figure(size=(10, 15))
    plt.subplot2grid((5, 4), (0, 0), colspan=4, rowspan=1)
    __figure3a__(fig_num=0)

    plt.subplot2grid((5, 4), (1, 0), colspan=4, rowspan=1)
    __figure3a__(fig_num=1)

    for ix in np.arange(4):
        plt.subplot2grid((5, 4), (2, ix), colspan=1, rowspan=1)
        __figure3b__(ix)

    plt.subplot2grid((5, 4), (3, 0), colspan=4, rowspan=1)
    __figure3c__()

    plt.subplot2grid((5, 4), (4, 0), colspan=4, rowspan=1)
    __figure3d__()

    save_fig("3")


def __figure3a__(fig_num=0):
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
    stimulus[t_solved > times[0]] = 1

    if fig_num == 0:
        plt.plot(t_solved, solution[:, 0], 'k')
        plt.plot(t_solved, 10 * stimulus - 80, 'grey')
        set_properties(y_label='v (mV)', y_tick=[-60, -40, -20, 0, 20])

    else:
        plt.plot(t_solved, (solution[:, 1]) * (solution[:, 2]), 'k')
        plt.plot(t_solved, solution[:, 2], "k--")
        set_properties(y_label='h$_{total}$, h$_s$', y_tick=[0, 0.2, 0.4, 0.6, 0.8])


def __figure3b__(ix=0):
    i_app_list = [0, 0.16, 0.16, 0.16]
    hs_list = [0.6, 0.6, 0.2, 0.05]

    v = np.arange(-90, 50)
    nh = nullcline_h(v)

    I = i_app_list[ix]
    hs = hs_list[ix]
    plt.plot(v, nh, 'k')
    nv = nullcline_v(v, I, hs=hs)

    plt.plot(v, nv, '--', color='grey')
    style = 'k' if ix == 3 else 'none'
    cross_index = np.argmin(np.abs(nv - nh))
    plt.scatter(v[cross_index], nv[cross_index], edgecolors='k', facecolors=style)

    set_properties(x_label="v (mV)", y_label="h", x_tick=[-40, 40], y_tick=[0, 0.2, 0.4, 0.6, 0.8],
                   x_limits=(-80, 50),
                   y_limits=(0, 0.6))


def __figure3c__():
    __figure3c_continuation__()
    parameters = default_parameters(i_app=0.16)
    t = np.arange(0, 10000, 0.1)
    ic = [-60, 0, 1]

    trajectory = odeint(ode_3d, ic, t, args=(parameters,))  # pre-stimulus solution
    plt.plot(trajectory[:, 2], trajectory[:, 0], c='grey')

    set_properties(x_label="h$_{s}$", y_label="v (mV)", x_tick=[0, 0.2, 0.4, 0.6, 0.8, 1], y_tick=[-80, -40, 0, 40])


def __figure3c_continuation__():
    parameters = default_parameters(i_app=0.16)
    v, h, h_s = symbols('v h h_s')
    dydt = hs_clamp([v, h, h_s], 0, parameters)

    DSargs = PyDSTool.args(name='bifn')
    DSargs.pars = {'h_s': 0}
    DSargs.varspecs = {'v': PyDSTool.convertPowers(str(dydt[0])),
                       'h': PyDSTool.convertPowers(str(dydt[1]))}
    DSargs.ics = {'v': 0, 'h': 0}

    ode = PyDSTool.Generator.Vode_ODEsystem(DSargs)
    ode.set(pars={'h_s': 0})
    ode.set(ics={'v': -49, "h": 0.4})
    PyCont = PyDSTool.ContClass(ode)

    PCargs = PyDSTool.args(name='EQ1', type='EP-C')
    PCargs.freepars = ['h_s']
    PCargs.MaxNumPoints = 350
    PCargs.MaxStepSize = 0.1
    PCargs.MinStepSize = 1e-5
    PCargs.StepSize = 1e-2
    PCargs.LocBifPoints = 'all'
    PCargs.SaveEigen = True
    PyCont.newCurve(PCargs)
    PyCont['EQ1'].backward()

    PyCont['EQ1'].display(['h_s', 'v'], stability=True, figure=1)

    PCargs.name = 'LC1'
    PCargs.type = 'LC-C'
    PCargs.initpoint = 'EQ1:H2'
    PCargs.freepars = ['h_s']
    PCargs.MaxNumPoints = 500
    PCargs.MaxStepSize = 0.1
    PCargs.LocBifPoints = 'all'
    PCargs.SaveEigen = True
    PyCont.newCurve(PCargs)
    PyCont['LC1'].backward()
    PyCont['LC1'].display(('h_s', 'v_min'), stability=True, figure=1)
    PyCont['LC1'].display(('h_s', 'v_max'), stability=True, figure=1)

    plt.xlim([0, 1])


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
    stimulus[t_solved > times[0]] = 1

    plt.plot(t_solved, solution[:, 0], 'k')
    plt.plot(t_solved, 10 * stimulus - 80, 'grey')
    set_properties(y_label='$V_m$ (mV)', y_tick=[-40, 0], y_limits=(-80, 20))
