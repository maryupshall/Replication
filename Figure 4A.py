from ode_functions.gating import *
from helpers.plotting import *
from helpers.nullclines import nullcline_h, nullcline_v

I_list_set = [[0, 3.5], [0.16, 0.16, 0.16]]
hs_list_set = [[1, 1], [0.6, 0.2, 0.05]]
v = np.arange(-90, 50)

nh = nullcline_h(v)

init_figure(size=(5,3))
for ix, (I_list, hs_list) in enumerate(zip(I_list_set, hs_list_set)):
    plt.subplot(1, 2, ix + 1)
    plt.plot(v, nh, 'g')
    for iy, (I, hs) in enumerate(zip(I_list, hs_list)):
        nv = nullcline_v(v, I, hs=hs)
        plt.plot(v, nv, 'r')

    if ix == 0:
        set_properties(xlabel="v (mV)", ylabel="h", xtick=[-40, 0], ytick=[0, 0.05, 0.1, 0.15], xlim=(-40, 5),
                       ylim=(0, 0.15))
    else:
        set_properties(xlabel="v (mV)", ylabel="h", xtick=[-60, 20], ytick=[0, 0.2, 0.4], xlim=(-80, 20), ylim=(0, 0.4))

save_fig('4A')
