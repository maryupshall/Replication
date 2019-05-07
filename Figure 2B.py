from scipy.optimize import newton
from ode_functions.gating import *
from ode_functions.defaults import default_parameters
from ode_functions.current import nc
from plotting import *

I_apps = [0, 3.5]

v = np.arange(-90, 50)
dh_null = (h_inf(v))
null_solve = np.zeros((len(v), 2))

for ix, I_app in enumerate(I_apps):
    parameters = default_parameters(I_app=I_app)

    plt.figure()
    plt.plot(v, dh_null)

    for i in range(len(v)):
        h_solve = newton(lambda h: nc(h, v[i], parameters), 0)  # calculate h value where dv=0

        null_solve[i, 0] = v[i]
        null_solve[i, 1] = h_solve

    plt.plot(null_solve[:, 0], null_solve[:, 1])
    set_properties(xlabel="v (mV)", ylabel="h", xtick=[-50, 0, 50], ytick=[0, 0.1, 0.2, 0.3, 0.4], xlim=[-75, 50], ylim=[0, 0.4])
