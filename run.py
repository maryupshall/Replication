import sys
from generators import figure_1, figure_2, figure_3, figure_4, figure_6


def run_all():
    figure_1.run()
    figure_2.run()
    figure_3.run()
    figure_4.run()
    figure_6.run()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        switcher = {"f1": figure_1.run,
                    "f2": figure_2.run,
                    "f3": figure_3.run,
                    "f4": figure_4.run,
                    "f6": figure_6.run}
        if sys.argv[1] in switcher.keys():
            switcher[sys.argv[1]]()
        else:
            run_all()
    else:
        run_all()
