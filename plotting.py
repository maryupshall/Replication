import matplotlib.pyplot as plt
from os.path import join


def init_figure(size=(2, 2), dpi=96):
    plt.figure(figsize=size, dpi=dpi)


def save_fig(name, extension='pdf'):
    figure_path = 'figures'
    plt.tight_layout()

    plt.savefig(join(figure_path, name+'.'+extension), format=extension)
    plt.close('all')


def set_properties(xlabel="", ylabel="", xtick=[], ytick=[]):
    plot_label_size = 10
    tick_label_size = 8

    plt.xlabel(xlabel, size=plot_label_size)
    plt.ylabel(ylabel, size=plot_label_size)
    plt.xticks(xtick, size=tick_label_size)
    plt.yticks(ytick, size=tick_label_size)

    plt.tight_layout()
