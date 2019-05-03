from scipy.integrate import odeint
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.diff_eq import ode_3d
from ode_functions.defaults import default_parameters

tmax = 10000  # ms
dt = 0.01
stim_time = 2000  # ms; pulse y at this time
state0 = [-65, 1, 1]  # v_list, h, hs
t_solved = np.array([])
solution = np.array([0, 0, 0])
currents = [0, 0.16]

for ix, I_app in enumerate(currents):
    if ix == 0:
        t = np.arange(0, stim_time, dt)
    else:
        t = np.arange(stim_time, tmax, dt)

    t_solved = np.concatenate((t_solved, t))

    parameters = default_parameters(I_app=I_app)

    state = odeint(lambda s, _, p: ode_3d(s, _, p, scale=2), state0, t, args=(parameters,))
    state0 = state[-1, :]

    solution = np.vstack((solution, state))

solution = solution[1:, :]  # TODO: hack for starting shape

stimulus = np.zeros(t_solved.shape)
stimulus[t_solved > stim_time] = currents[1]

# plotting
plt.subplot(2, 1, 1)
plt.plot(t_solved, solution[:, 0])
plt.xlabel('time', size=10)
plt.ylabel('$V_m$ (mV)', size=10)
plt.ylim(-80, 60)

plt.subplot(2, 1, 2)
plt.plot(t_solved, stimulus)
plt.xlabel('time (ms)', size=10)
plt.ylabel('$I_{app}$', size=10)
