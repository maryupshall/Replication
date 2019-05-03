from scipy.integrate import odeint
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import ode_3d

parameters= default_parameters()

tmax = 10000  # ms
dt = 0.1
initial_state = [-65, 1, 1]  # v_list, h, & hs_list

## set two time windows, pre and post stimulus
stim_time = 2000  # ms; pulse y at this time
tpre = np.arange(0, stim_time, dt)  # array of time values over which to compute the ODE solution
tduring = np.arange(stim_time, 8000, dt)
tpost = np.arange(8000, tmax, dt)

# PRE-STIMULUS
state0 = initial_state
state = odeint(ode_3d, state0, tpre, args=(parameters,))  # pre-stimulus solution
state_pre = state

# POST-STIMULUS
# set initial condition to last prestimulus point + stimulus
I = 0.16
parameters[0] = I
state0 = state[-1, :]
state = odeint(ode_3d, state0, tduring, args=(parameters,))  # post-stimulus solution
state_during = state

I = 0
parameters[0] = I
state0 = state[-1, :]
state = odeint(ode_3d, state0, tpost, args=(parameters,))  # post-stimulus solution

state_all = np.concatenate([state_pre, state_during, state], axis=0)
t = np.concatenate([tpre, tduring, tpost], axis=0)

# make stimulus array for plotting
stim_pre = np.zeros(len(tpre))
stim_during = np.zeros(len(tduring))
stim_post = np.zeros(len(tpost))
stim_pre[:] = 0
stim_during[:] = 0.16
stim_post[:] = 0
stimulus = np.concatenate([stim_pre, stim_during, stim_post], axis=0)

# plotting
plt.subplot(2, 1, 1)
plt.plot(t, state_all[:, 0])
plt.xlabel('time', size=14)
plt.ylabel('v_list (mV)', size=14)
plt.ylim(-80, 40)
plt.xlim(0, 10000)

plt.subplot(2, 1, 2)
plt.plot(t, stimulus)
plt.xlabel('time (ms)', size=14)
plt.ylabel('I_app', size=14)
plt.xlim(0, 10000)