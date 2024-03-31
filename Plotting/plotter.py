import matplotlib.pyplot as plt
import numpy as np


class PlotData:
    def __init__(self, x_name: str, y_name: str, x_range: np.array, data: [list, np.array], data_type: str):
        """

        :param x_name:
        :param y_name:
        :param x_range: list or array of x-values. Note that that this is one range for all different lists/arrays of y-values
        :param data: list/array of y-values or list/array of list/arrays of y-values OR list of FunctionClasses
        :param data_type: Fill in the type of input data: Classes, lists, arrays or curvefit
        """
        self.colors = ["#00A6B6", "#A50034", "#EF60A3", "#6CC24A", "#FFB81C", "#6F1D77", "#EC6842", "#000000"]
        #               cyan,   raspberry,    pink,   light green, yellow,     purple,     orange,   black
        self.grid = True
        self.legend = True
        self.xlim = [None, None]
        self.ylim = [None, None]
        self.x_name: str = x_name
        self.y_name: str = y_name
        self.x_range = x_range
        self.data = data
        self.data_type = data_type
        self.data_to_plot = []
        self.list_labels = None

        ax = self.initiate_plot()
        if 'class' in self.data_type:
            self.data_to_plot = self.data
            self.plot_data_class_lst(ax)
        elif 'list' or 'array' in self.data_type:
            self.data_to_plot = self.data
            self.plot_lists(ax)
        elif 'curvefit' in self.data_type:
            self.curve_fit(ax)

    def get_axislabel(self, name):
        if 'AoA' in name:
            axislabel = f'$\\alpha$ [deg]'
        elif 'CL' in name:
            axislabel = f'$C_L$ [-]'
        elif 'CM' in name:
            axislabel = f'$C_M$ [-]'
        elif 'CD' in name:
            axislabel = f'$C_M$ [-]'
        elif 'delta_e' in name:
            axislabel = f'$\\delta_e$ [deg]'
        elif 'CT' in name:
            axislabel = f'$C_T$ [-]'
        elif 'J' in name:
            axislabel = f'J [-]'
        else:
            axislabel = ''
            print('This label is not in the database. The following options exist: AoA, CL, CD, CM, CT, delta_e. If you want additional ones, ask Dorothé')
        return axislabel

    def generate_xticks(self, min_val, max_val):
        range_val = max_val - min_val
        num_ticks = 11

        # Define the candidate spacings
        spacings = [5, 2.5, 1, 0.5, 0.25]

        for spacing in spacings:
            # Calculate the number of ticks based on the spacing
            num_ticks_candidate = range_val / spacing + 1

            # Check if the number of ticks is close to the desired number
            if np.isclose(num_ticks_candidate, num_ticks):
                # Generate the ticks
                ticks = np.arange(min_val, max_val + spacing, spacing)
                return ticks

        # If none of the spacings worked, default to 1
        ticks = np.linspace(min_val, max_val, num_ticks)
        return ticks

    def initiate_plot(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlabel(self.get_axislabel(self.x_name))
        ax.set_ylabel(self.get_axislabel(self.y_name))

        if all(item is None for item in self.xlim):
            self.xlim[0] = self.x_range[0]
            self.xlim[1] = self.x_range[-1]

        ax.set_xticks(self.generate_xticks(self.xlim[0], self.xlim[1]))
        ax.set_xlim(self.xlim)

        if self.grid:
            ax.grid()

        return ax

    def plot_data_class_lst(self, ax):

        for i, function in enumerate(self.data_to_plot):
            function_label = f'V = {function.tunnel_speed} m/s, J = {function.propeller_speed}'
            ax.plot(self.x_range, function.poly_coeff(self.x_range), '-.', color=self.colors[i], label=function_label)
            ax.scatter(function.data_points[function.x_variable], function.data_points[function.y_variable], color=self.colors[i])

        if self.legend:
            ax.legend()
        return

    def plot_lists(self, ax):

        if len(self.data_to_plot) == 1:
            ax.plot(self.x_range, self.data_to_plot, color=self.colors[0])

        elif len(self.data_to_plot) > 1:
            for i in range(0, len(self.data_to_plot), 1):
                if self.list_labels is not None:
                    ax.plot(self.x_range, self.data_to_plot[i], color=self.colors[i], label=self.list_labels[i])
                else:
                    ax.plot(self.x_range, self.data_to_plot[i], color=self.colors[i])
        else:
            print('Please provide x and y list of values.')
        return

    def curve_fit(self, ax):
        order = int(input('Please provide order of fit'))

        if len(self.data) == 1:
            polyfit = np.poly1d(np.polyfit(self.x_range, self.data, order))
            self.data_to_plot = polyfit(self.x_range)

        elif len(self.data) > 1:
            for i in range(0, len(self.data_to_plot), 1):
                polyfit = np.poly1d(np.polyfit(self.x_range, self.data[i], order))
                self.data_to_plot.append(polyfit(self.x_range))

        self.plot_lists(ax)


if __name__ == "__main__":
    n = 40
    x_range = np.linspace(-10, 20, 100)
    function1 = np.poly1d([0.5, 5])
    ylst1 = function1(x_range)
    function2 = np.poly1d([-0.5, 5])
    ylst2 = function2(x_range)

    PlotData('AoA', 'CL', x_range, [x_range, ylst1, x_range, ylst2], 'lists')

    plt.show()
