from scipy.integrate import odeint

from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_3d
from ode_functions.gating import *
from helpers.plotting import *

ic = [-65, 1, 1]  # v_list, h, hs
t_solved = np.array([])
solution = np.array([0, 0, 0])
currents = [0, 0.16]
times = [2000, 10000]
t0 = 0
for ix, I_app in enumerate(currents):
    t = np.arange(t0, times[ix], 0.1)
    t_solved = np.concatenate((t_solved, t))
    t0 = times[ix]

    parameters = default_parameters(I_app=I_app)
    state = odeint(lambda s, _, p: ode_3d(s, _, p, scale=2), ic, t, args=(parameters,))
    ic = state[-1, :]

    solution = np.vstack((solution, state))

solution = solution[1:, :]  # TODO: hack for starting shape

stimulus = np.zeros(t_solved.shape)
stimulus[t_solved > times[0]] = currents[1]

init_figure(size=(5, 3))

plt.subplot(2, 1, 1)
plt.plot(t_solved, solution[:, 0], 'k')
set_properties(ylabel='$V_m$ (mV)', ytick=[-40, 0], ylim=(-80, 20))

plt.subplot(2, 1, 2)
plt.plot(t_solved, stimulus, 'k')
set_properties()

save_fig('3D')
