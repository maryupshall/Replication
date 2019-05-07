from scipy.integrate import odeint
from ode_functions.gating import *
from ode_functions.diff_eq import ode_3d
from ode_functions.defaults import default_parameters
from plotting import *

tmax = 6000  # ms
dt = 0.1
stim_time = 2000  # ms; pulse y at this time
state0 = [-55, 0, 0]  # v_list, h
t_solved = np.array([])
solution = np.array([0, 0, 0])
currents = [0, 0.16]

for ix, I_app in enumerate(currents):
    if ix == 0:
        t = np.arange(0, stim_time)
    else:
        t = np.arange(stim_time, tmax)

    t_solved = np.concatenate((t_solved, t))

    parameters = default_parameters(I_app=I_app)
    state = odeint(ode_3d, state0, t, args=(parameters,))
    state0 = state[-1, :]

    solution = np.vstack((solution, state))

solution = solution[1:, :]  # TODO: hack for starting shape

stimulus = np.zeros(t_solved.shape)
stimulus[t_solved > stim_time] = currents[1]

init_figure(size=(4, 3))

# plotting
plt.subplot(3, 1, 1)
plt.plot(t_solved, solution[:, 0], 'k')
set_properties(ylabel='v (mV)', ytick=[-60, -40, -20, 0, 20])


plt.subplot(3, 1, 2)
plt.plot(t_solved, (solution[:, 1]) * (solution[:, 2]), 'k')
plt.plot(t_solved, solution[:, 2], "k--")
set_properties(ylabel='h$_{total}$, h$_s$', ytick=[0, 0.2, 0.4, 0.6, 0.8])

plt.subplot(3, 1, 3)
plt.plot(t_solved, stimulus, 'k')
set_properties(xlabel='Time (ms)', ylabel='I$_{app}$', ytick=[0, 0.16], xtick=np.arange(0, 8000, 2000))

save_fig('Figure 3A')