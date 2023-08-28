import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


HALF = 3 # Defining how big the graph is.


def get(parameter: float):
    with open(f'logs/log_{parameter}.txt') as f:
        data_string = f.read()

    # Split the data into lines and convert them to float tuples.
    lines = data_string.strip().split('\n')
    data_points = [tuple(map(float, line.strip('()').split(','))) for line in lines]

    return data_points


def plot(data_points: list, log_item):
    x_coords, y_coords = zip(*data_points)  # Unzip the data into separate x and y coordinates.

    # Set up the graph.
    plt.scatter(x_coords, y_coords, color='blue', label='Data Points')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.xlim(-HALF, HALF)
    plt.ylim(0, 2*HALF)
    plt.title(f'Scatter Plot of Data Points of "{log_item}"')
    plt.legend()
    plt.grid(True)

    # plt.show()


def plot_dense(data_points: list, log_item):
    x_coords, y_coords = zip(*data_points)  # Unzip the data into separate x and y coordinates.

    # Set up the graph.
    plt.scatter(x_coords, y_coords, color='blue', label='Data Points')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.xlim(-HALF, HALF)
    plt.ylim(0, 2*HALF)
    plt.title(f'Scatter Plot of Data Points of "{log_item}"')
    plt.legend()

    # Set the major locator for the x-axis and y-axis to display grid lines every 0.2.
    x_major_locator = MultipleLocator(1)  # Major ticks every 1 unit
    x_minor_locator = MultipleLocator(0.2)  # Minor ticks every 0.2 units
    y_major_locator = MultipleLocator(1)  # Major ticks every 1 unit
    y_minor_locator = MultipleLocator(0.2)  # Minor ticks every 0.2 units

    plt.gca().xaxis.set_major_locator(x_major_locator)
    plt.gca().xaxis.set_minor_locator(x_minor_locator)
    plt.gca().yaxis.set_major_locator(y_major_locator)
    plt.gca().yaxis.set_minor_locator(y_minor_locator)

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # plt.show()


def save_plot(plt_input, filename):
    plot_folder = 'plots'
    os.makedirs(plot_folder, exist_ok=True)
    save_path = os.path.join(plot_folder, filename)
    plt_input.savefig(save_path)
    plt_input.close()
