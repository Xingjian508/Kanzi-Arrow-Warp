from functions import *


# These are the choices. Floats represent scaling parameters. Text are self-explanatory.
choices = ['straight', 0.3, 0.5, 0.7, 0.9,
           'trans', 'start', 'problem',
           'fix1', 'fix2', 'experimental1']


if __name__ == '__main__':
    for item in choices:
        print(item)
        data = get(item)

        plt.figure()
        plot(data, item)
        save_plot(plt, f"{item}_plot.png")
