from scipy.integrate import odeint
import matplotlib.pyplot as plt
from ode_functions.gating import *
from ode_functions.diff_eq import ode_3d, voltage_clamp
from ode_functions.defaults import default_parameters
from ode_functions.current import INa
from plotting import *

## Doesn't work with INa model including h and hs_list but works without.


# Parameter values
parameters = default_parameters(gNa=0.00000912)  # need to divide given value by 2 to get correct graph
parameters.append(ode_3d)


tmax = 600  # ms
dt = 1
t = np.arange(0, tmax, dt)

## set two time windows, pre and post stimulus
stim_time = 100  # ms; pulse y at this time
tpre = np.arange(0, stim_time, dt)  # array of time values over which to compute the ODE solution
tduring = np.arange(stim_time, (stim_time + 3), dt)
tpost = np.arange(stim_time, tmax, dt)

##PRE STIMULUS

v = -70  # mV

Na_current_pre = np.zeros((len(tpre),2))


initial_state = [-70, 0, 0]  # v_list, h, hs_list
state0 = initial_state

state = odeint(voltage_clamp, state0, tpre, args=(parameters,))
h = state[:, 1]
hs = state[:, 2]
I_Na_pre = INa(v, m_inf(v), parameters, h=h, hs=hs)
#(parameters[1] * (m_inf(v_list) ** 3) * h * hs_list * (v_list - parameters[4]))  # without h & hs_list matches https://www.physiology.org/doi/full/10.1152/jn.00513.2009?url_ver=Z39.88-2003&rfr_id=ori:rid:crossref.org&rfr_dat=cr_pub%3dpubmed
#I_Na_pre = (parameters[1] * (m_inf(v_list) ** 3) * (v_list - parameters[4])) #without h and hs_list

v_clamp = v
Na_current_pre[:,0] = tpre
Na_current_pre[:,1] = I_Na_pre

##DURING STIMULUS

v = 0  # mV

Na_current_during = np.zeros((len(tduring),2))


initial_state = [0, 0, 0]  # v_list, h, hs_list
state0 = initial_state

state = odeint(voltage_clamp, state0, tduring, args=(parameters,))
h = state[:, 1]
hs = state[:, 2]
I_Na_during = INa(v, m_inf(v), parameters, h=h, hs=hs)
#(parameters[1] * (m_inf(v_list) ** 3) * h * hs_list * (v_list - parameters[4]))  # without h & hs_list matches https://www.physiology.org/doi/full/10.1152/jn.00513.2009?url_ver=Z39.88-2003&rfr_id=ori:rid:crossref.org&rfr_dat=cr_pub%3dpubmed
#I_Na_during = (gNa * (m_inf(v_list) ** 3) * (v_list - ENa))

v_clamp = v
Na_current_during[:,0] = tduring
Na_current_during[:,1] = I_Na_during

##POST STIMULUS

v = -70  # mV

Na_current_post = np.zeros((len(tpost),2))

initial_state = [-70, 0, 0]  # v_list, h, hs_list
state0 = initial_state

state = odeint(voltage_clamp, state0, tpost, args=(parameters,))
h = state[:, 1]
hs = state[:, 2]
I_Na_post = INa(v, m_inf(v), parameters, h=h, hs=hs)
#(parameters[1] * (m_inf(v_list) ** 3) * h * hs_list * (v_list - parameters[4]))  # without h & hs_list matches https://www.physiology.org/doi/full/10.1152/jn.00513.2009?url_ver=Z39.88-2003&rfr_id=ori:rid:crossref.org&rfr_dat=cr_pub%3dpubmed
#I_Na_post = (parameters[1] * (m_inf(v_list) ** 3) * (v_list - parameters[4]))

v_clamp = v
# I_Na_max = np.max(I_Na)
Na_current_post[:,0] = tpost
Na_current_post[:,1] = I_Na_post

Na_current = np.concatenate([Na_current_pre[:,1], Na_current_during[:,1], Na_current_post[:,1]], axis=0)
t = np.concatenate([tpre, tduring, tpost], axis=0)

plt.plot(t, Na_current)
plt.xlabel("time (ms)")
plt.ylabel("I_list(Na) (uA/cm^2)")
plt.xlim(0, tmax)
