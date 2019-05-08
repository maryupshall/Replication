from helpers.nullclines import nullcline_h, nullcline_v
from ode_functions.gating import *
from helpers.plotting import *

I_apps = [0, 3.5]
v = np.arange(-90, 50)
nh = nullcline_h(v)
init_figure(size=(5, 3))
for ix, I_app in enumerate(I_apps):
    plt.subplot(121 + ix)
    plt.plot(v, nh, 'k')
    nv = nullcline_v(v, I_app)

    plt.plot(v, nv, '--', color='grey')
    style = 'k' if ix == 1 else 'none'
    cross_index = np.argmin(np.abs(nv - nh))
    plt.scatter(v[cross_index], nv[cross_index], edgecolors='k', facecolors=style)

    set_properties(xlabel="v (mV)", ylabel="h", xtick=[-50, 0, 50], ytick=[0, 0.1, 0.2, 0.3, 0.4], xlim=[-75, 50],
                   ylim=[0, 0.4])

save_fig("2B")
