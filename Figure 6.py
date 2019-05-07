from scipy.integrate import odeint
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import synaptic_3d, I_NMDA, I_AMPA
from plotting import *

tmax = 10000  # ms
dt = 0.1
ESyn = 0
conditions = [I_NMDA, I_AMPA, None]
parameter_sets1 = [[0, 0.060, 0], [0, 0.0023, 0], [0, 0.16, 0]]
parameter_sets2 = [[0, 0.060, 0], [0, 0.0007, 0], [0, 0.32, 0]]
all_parameters = [parameter_sets1, parameter_sets2]
times = [2000, 8000, 10000]

plt.figure()
for iz, parameter_sets in enumerate(all_parameters):
    for ix, (condition, parameter_set) in enumerate(zip(conditions, parameter_sets)):
        t0 = 0
        state0 = [-65, 1, 1]  # v_list, h, & hs_list
        t_solved = np.array([])
        solution = np.array([0, 0, 0])
        plt.tight_layout()
        plt.subplot(4, 2, 2*ix+iz+1)

        for iy, control_parameter in enumerate(parameter_set):
            t = np.arange(t0, times[iy])
            t_solved = np.concatenate((t_solved, t))
            t0 = times[iy]

            if condition is not None:
                parameters = default_parameters(I_app=0)
                parameters.append(control_parameter)
                parameters.append(ESyn)
                parameters.append(condition)
            else:
                parameters = default_parameters(I_app=control_parameter)
                parameters.append(condition)

            state = odeint(synaptic_3d, state0, t, args=(parameters,))
            state0 = state[-1, :]

            solution = np.vstack((solution, state))

        solution = solution[1:, :]  # TODO: hack for starting shape

        plt.plot(t_solved, solution[:, 0])

    stimulus = np.zeros(t_solved.shape)
    stimulus[(t_solved > times[0]) & (t_solved < times[1])] = 1

    plt.subplot(4, 2, 7+iz)
    plt.plot(t_solved, stimulus)

