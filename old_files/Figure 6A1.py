from scipy.integrate import odeint
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.defaults import default_parameters
from ode_functions.diff_eq import synaptic_3d, I_NMDA

parameters = default_parameters()
gSyn=0 #nS/cm^2 conductance pulse
ESyn=0
parameters.append(gSyn)
parameters.append(ESyn)
parameters.append(I_NMDA)


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
state = odeint(synaptic_3d, state0, tpre, args=(parameters,))  # pre-stimulus solution
state_pre = state

# POST-STIMULUS
gNmda = 0.06
parameters[-3] = gNmda
state0 = state[-1, :]
state = odeint(synaptic_3d, state0, tduring, args=(parameters,))  # post-stimulus solution
state_during = state

gNmda = 0
parameters[-3] = gNmda
state0 = state[-1, :]
state = odeint(synaptic_3d, state0, tpost, args=(parameters,))  # post-stimulus solution

state_all = np.concatenate([state_pre, state_during, state], axis=0)
t = np.concatenate([tpre, tduring, tpost], axis=0)

# plotting
plt.plot(t, state_all[:, 0])
plt.xlabel('time', size=14)
plt.ylabel('v_list (mV)', size=14)
plt.ylim(-80, 40)
plt.xlim(0, 10000)


