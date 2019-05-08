from helpers.nullclines import nullcline_v, nullcline_h
from ode_functions.gating import *
from helpers.plotting import *

I_list = [0, 0.16, 0.16, 0.16]
hs_list = [0.6, 0.6, 0.2, 0.05]

v = np.arange(-90, 50)
nh = nullcline_h(v)

init_figure(size=(8, 2))
for ix, (I, hs) in enumerate(zip(I_list, hs_list)):
    plt.subplot(1, 4, ix + 1)
    plt.plot(v, nh, 'k')
    nv = nullcline_v(v, I, hs=hs)

    plt.plot(v, nv, '--', color='grey')
    style = 'k' if ix == 3 else 'none'
    cross_index = np.argmin(np.abs(nv - nh))
    plt.scatter(v[cross_index], nv[cross_index], edgecolors='k', facecolors=style)

    set_properties(xlabel="v (mV)", ylabel="h", xtick=[-40, 40], ytick=[0, 0.2, 0.4, 0.6, 0.8], xlim=(-80, 50),
                   ylim=(0, 0.6))

save_fig('3B')
