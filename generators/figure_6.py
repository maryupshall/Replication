from scipy.integrate import odeint

from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import synaptic_3d
from ode_functions.current import nmda_current, ampa_current
from ode_functions.gating import *
from helpers.plotting import *


def run():
    __figure6__()


def __figure6__():
    e_syn = 0
    conditions = [nmda_current, ampa_current, None]
    parameter_sets1 = [[0, 0.060, 0], [0, 0.0023, 0], [0, 0.16, 0]]
    parameter_sets2 = [[0, 0.060, 0], [0, 0.0007, 0], [0, 0.32, 0]]
    all_parameters = [parameter_sets1, parameter_sets2]
    times = [2000, 8000, 10000]

    init_figure(size=(6, 6))
    for iz, parameter_sets in enumerate(all_parameters):
        for ix, (condition, parameter_set) in enumerate(zip(conditions, parameter_sets)):
            t0 = 0
            ic = [-65, 1, 1]
            t_solved = np.array([])
            solution = np.array([0, 0, 0])

            plt.subplot(4, 2, 2 * ix + iz + 1)
            for iy, control_parameter in enumerate(parameter_set):
                t = np.arange(t0, times[iy])
                t_solved = np.concatenate((t_solved, t))
                t0 = times[iy]

                if condition is not None:
                    parameters = default_parameters(i_app=0)
                    parameters.append(control_parameter)
                    parameters.append(e_syn)
                    parameters.append(condition)
                else:
                    parameters = default_parameters(i_app=control_parameter)
                    parameters.append(condition)

                state = odeint(synaptic_3d, ic, t, args=(parameters,))
                ic = state[-1, :]

                solution = np.vstack((solution, state))

            solution = solution[1:, :]  # TODO: hack for starting shape

            plt.plot(t_solved, solution[:, 0], 'k')
            set_properties(y_label="V (mV)", y_tick=[-80, -40, 0])

            if ix == 0:
                stimulus = np.zeros(t_solved.shape)
                stimulus[(t_solved > times[0]) & (t_solved < times[1])] = 1

                plt.subplot(4, 2, 7 + iz)
                plt.plot(t_solved, stimulus, 'k')
                set_properties()

    save_fig('6')
