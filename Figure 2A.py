from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.diff_eq import ode_2d
from ode_functions.defaults import default_parameters


#Parameter values
parameters= default_parameters()

tmax = 3000  # ms
dt = 0.1
initial_state = [-35, 1]  # v_list, h

## set two time windows, pre and post stimulus
stim_time=2000  #ms; pulse y at this time
tpre=np.arange(0,stim_time,dt)  # array of time values over which to compute the ODE solution
tpost=np.arange(stim_time,tmax,dt)

# PRE-STIMULUS
state0=initial_state
state=odeint(ode_2d,state0,tpre,args=(parameters,)) #pre-stimulus solution
state_pre=state

# POST-STIMULUS
# set initial condition to last prestimulus point + stimulus
parameters= default_parameters(I_app=3.5)
state0=state[-1,:]
state=odeint(ode_2d,state0,tpost,args=(parameters,)) #post-stimulus solution

state_all=np.concatenate([state_pre, state], axis=0)
t=np.concatenate([tpre, tpost], axis=0)

#make stimulus array for plotting
stim_pre=np.zeros(len(tpre))
stim_post=np.zeros(len(tpost))
stim_post[:]=parameters[0]
stimulus=np.concatenate([stim_pre, stim_post], axis=0)

# plotting
plt.subplot(2,1,1)
plt.plot(t,state_all[:,0])
plt.xlabel('time',size=10)
plt.ylabel('v_list (mV)',size=10)
plt.ylim(-80,60)
print(t[-1],(state_all[:,0])[-1])


plt.subplot(2,1,2)
plt.plot(t,stimulus)
plt.xlabel('time (ms)',size=14)
plt.ylabel('I_app',size=14)
