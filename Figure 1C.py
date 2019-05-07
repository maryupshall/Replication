from scipy.integrate import odeint
from ode_functions.gating import *
from ode_functions.diff_eq import ode_5d
from ode_functions.defaults import default_parameters
from plotting import *

#Parameter values
parameters = default_parameters()

tmax=4200
dt = 0.01 #time step
t=np.arange(0,tmax,dt)

state0=[-55,0,0,0,0] #v_list, h, hs_list, m, n

state=odeint(ode_5d,state0,t,args=(parameters,), rtol=1e-6, atol=1e-6)
v = state[:, 0]
h = state[:, 1]
n = state[:, 4]

plt.plot(h,n, c="grey")
plt.plot(h,list(map(f,h)), "k")
set_properties(xlabel="h", ylabel="n", xtick=[0, 0.2, 0.4, 0.6], ytick= np.arange(0, 1, 0.2))
plt.legend(["n", "n=f(h)"])