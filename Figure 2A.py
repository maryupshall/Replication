from scipy.integrate import odeint

from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_2d
from ode_functions.gating import *
from helpers.plotting import *

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

    parameters = default_parameters(I_app=I_app)
    state = odeint(ode_2d, ic, t, args=(parameters,))
    ic = state[-1, :]

    solution = np.vstack((solution, state))

solution = solution[1:, :]  # TODO: hack for starting shape

stimulus = np.zeros(t_solved.shape)
stimulus[t_solved > times[0]] = currents[1]

init_figure(size=(5, 3))
plt.subplot(2, 1, 1)
plt.plot(t_solved, solution[:, 0], "k")
set_properties(ylabel="V (mV)", ytick=[-40, -20, 0, 20])

plt.subplot(2, 1, 2)
plt.plot(t_solved, stimulus, "k")
set_properties(None)

save_fig('2A')
