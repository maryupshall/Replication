from scipy.integrate import odeint
import PyDSTool
from helpers.nullclines import nullcline_h, nullcline_v
from helpers.plotting import *
from ode_functions.current import sodium_current_hack
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_2d, ode_3d, voltage_clamp
from ode_functions.gating import *
from sympy import *


def run():
    init_figure(size=(10, 10))
    plt.subplot2grid((4, 2), (0, 0), colspan=1, rowspan=1)
    __figure4a__(ix=0)
    plt.subplot2grid((4, 2), (0, 1), colspan=1, rowspan=1)
    __figure4a__(ix=1)

    # plt.subplot2grid((5, 2), (0, 0), colspan=1, rowspan=1)
    # __figure4b__()

    plt.subplot2grid((4, 2), (3, 0), colspan=1, rowspan=1)
    __figure4c__(ix=0)
    plt.subplot2grid((4, 2), (3, 1), colspan=1, rowspan=1)
    __figure4c__(ix=1)


def __figure4a__(ix=0):
    i_app_list_set = [[0, 3.5], [0.16, 0.16, 0.16]]
    hs_list_set = [[1, 1], [0.6, 0.2, 0.05]]
    v = np.arange(-90, 50)

    nh = nullcline_h(v)

    i_app_list = i_app_list_set[ix]
    hs_list = hs_list_set[ix]

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


def __figure4b__(version=0):
    if version == 0:
        __figure4b1_continuation__()
    else:
        __figure4b2_continuation__()


def __figure4b1_continuation__():
    parameters = default_parameters(i_app=0)
    v, h, i_app = symbols('v h i_app')
    parameters[0] = i_app
    dydt = ode_2d([v, h], 0, parameters, exp=exp)

    DSargs = PyDSTool.args(name='bifn')
    DSargs.pars = {'i_app': 0}
    DSargs.varspecs = {'v': PyDSTool.convertPowers(str(dydt[0])),
                       'h': PyDSTool.convertPowers(str(dydt[1]))}
    DSargs.ics = {'v': 0, 'h': 0}

    ode = PyDSTool.Generator.Vode_ODEsystem(DSargs)
    ode.set(pars={'i_app': 0})
    ode.set(ics={'v': -49, "h": 0.4})
    PyCont = PyDSTool.ContClass(ode)

    PCargs = PyDSTool.args(name='EQ1', type='EP-C')
    PCargs.freepars = ['i_app']
    PCargs.MaxNumPoints = 500
    PCargs.MaxStepSize = 0.1
    PCargs.MinStepSize = 1e-5
    PCargs.StepSize = 1e-2
    PCargs.LocBifPoints = 'all'
    PCargs.SaveEigen = True
    PyCont.newCurve(PCargs)
    PyCont['EQ1'].backward()
    PyCont['EQ1'].forward()
    PyCont['EQ1'].backward()

    PyCont['EQ1'].display(['i_app', 'v'], stability=True, figure=1)

    PCargs.name = 'LC1'
    PCargs.type = 'LC-C'
    PCargs.initpoint = 'EQ1:H1'
    PCargs.freepars = ['i_app']
    PCargs.MaxNumPoints = 500
    PCargs.MaxStepSize = 0.1
    PCargs.LocBifPoints = 'all'
    PCargs.SaveEigen = True
    PyCont.newCurve(PCargs)
    PyCont['LC1'].backward()
    PyCont['LC1'].display(('h_s', 'v_min'), stability=True, figure=1)
    PyCont['LC1'].display(('h_s', 'v_max'), stability=True, figure=1)

    plt.xlim([-5, 5])


def __figure4b2_continuation__():
    pass


def __figure4c__(ix=0):
    ode_functions = [ode_2d, ode_3d]
    v_list = np.arange(-100, 20, 0.5)
    t = np.arange(0, 1000, 0.1)

    membrane_current = np.zeros(len(v_list))
    parameters = default_parameters()
    parameters.append(None)

    ode_function = ode_functions[ix]
    parameters[-1] = ode_function

    for i in range(len(v_list)):
        initial_state = [v_list[i], 0] + ix * [0]

        state = odeint(voltage_clamp, initial_state, t, args=(parameters,))
        h = state[:, 1]
        v = state[:, 0]
        hs = 1 if np.shape(state)[1] == 2 else state[:, 2]

        membrane_current[i] = -sodium_current_hack(v, h, parameters, hs=hs)[-1]

    plt.plot(v_list, membrane_current, 'k')
    plt.plot(v_list, v_list * [0], '--', color='grey')

    if ix == 0:
        set_properties(x_label="Voltage (mV)", y_label="I$_{stim} ( \mu A/cm^{2}$)", x_tick=[-80, -40],
                       y_tick=[-5, 0, 5],
                       x_limits=(-100, -20), y_limits=(-5, 5))
    else:
        set_properties(x_label="Voltage (mV)", y_label="I$_{stim} ( \mu A/cm^{2}$)", x_tick=[-70, -60, -50],
                       y_tick=[-0.1, 0, 0.1, 0.2], x_limits=(-70, -50), y_limits=(-0.1, 0.2))
