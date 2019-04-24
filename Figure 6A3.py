from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ode_functions.gating import *

#Parameter values

I=0 #uA/cm^2
gNa= 8 #mS/cm^2
gK=0.6 #mS/cm^2
gl=0.013 #mS/cm^2
ENa=60 #mV
Ek=-85 #mV
El=-60 #mV
gNmda=0 #nS/cm^2 conductance pulse
gAmpa=0
Eampa= 0 #mV
Enmda = 0 #mV

parameters=[I,gNa,gK,gl,ENa,Ek,El,gNmda,gAmpa,Eampa,Enmda]


def INaLK_ode(state, t, parameters):
    I = parameters[0]
    gNa = parameters[1]
    gK = parameters[2]
    gl = parameters[3]
    ENa = parameters[4]
    Ek = parameters[5]
    El = parameters[6]
    gNmda = parameters[7]
    gAmpa = parameters[8]
    Eampa = parameters[9]
    Enmda = parameters[10]

    v = state[0]
    h = state[1]
    hs = state[2]

    n = f(h)

    dv = I - (gl * (v - El)) - (gNa * (m_inf(v) ** 3) * h * hs * (v - ENa)) - (gK * (n ** 3) * (v - Ek))  # 3D model
    dh = - (h - (h_inf(v))) / (Th(v))
    dhs = - (hs - (hs_inf(v))) / (Ths(v))

    return [dv, dh, dhs]


tmax = 10000  # ms
dt = 0.1
initial_state = [-65, 1, 1]  # v_list, h, & hs_list

Mg = 1.4  # concentration (mM)

## set two time windows, pre and post stimulus
stim_time = 2000  # ms; pulse y at this time
tpre = np.arange(0, stim_time, dt)  # array of time values over which to compute the ODE solution
tduring = np.arange(stim_time, 8000, dt)
tpost = np.arange(8000, tmax, dt)

# PRE-STIMULUS
state0 = initial_state
state = odeint(INaLK_ode, state0, tpre, args=(parameters,))  # pre-stimulus solution
state_pre = state

# POST-STIMULUS
# set initial condition to last prestimulus point + stimulus
I = 0.16
parameters = [I, gNa, gK, gl, ENa, Ek, El, gNmda, gAmpa, Eampa, Enmda]
I_app = I
state0 = state[-1, :]
state0[0] = state0[0] + I_app  # a voltage "pulse"
state = odeint(INaLK_ode, state0, tduring, args=(parameters,))  # post-stimulus solution
state_during = state

I = 0
parameters = [I, gNa, gK, gl, ENa, Ek, El, gNmda, gAmpa, Eampa, Enmda]
I_app = I
state0 = state[-1, :]
state0[0] = state0[0] + I_app  # a voltage "pulse"
state = odeint(INaLK_ode, state0, tpost, args=(parameters,))  # post-stimulus solution

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