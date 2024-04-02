import matplotlib.pyplot as plt
import numpy as np


class PlotData:
    def __init__(self, x_name: str, y_name: str, x_range: np.array, data: [list, np.array], data_type: str, labels_lst: [list, np.array]):
        """
        A class that generates a plot with a general plotting style.
        :param x_name: Name of the x variable. If inputting a dataframe, make sure that the column name is filled in.
        :param y_name:Name of the y variable. If inputting a dataframe, make sure that the column name is filled in.
        :param x_range: list or array of x-values. Note that this is one range for all different lists/arrays of y-values
        :param data: list/array of y-values or list/array of list/arrays of y-values OR list of FunctionClasses
        :param data_type: Fill in the type of input data: Classes, lists, arrays or curvefit
        :param labels_lst: a list of the labels to be used in the plot. Note that for a dataframe the labels are generated automatically. Fill in None in that case.
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
        self.list_labels = labels_lst

        fig, ax, savename = self.initiate_plot()
        if 'class' in self.data_type:
            self.data_to_plot = self.data
            self.plot_data_class_lst(fig, ax, savename)
        elif 'list' in self.data_type or 'array' in self.data_type:
            self.data_to_plot = self.data
            self.plot_lists(fig, ax, self.data_to_plot, ['line'], self.list_labels, savename)
        elif 'curvefit' in self.data_type:
            self.curve_fit(fig, ax, savename)

    def get_axislabel(self, name):
        if 'AoA' in name:
            axislabel = f'$\\alpha$ [deg]'
        elif 'CL' in name:
            axislabel = f'$C_L$ [-]'
        elif 'CM' in name:
            axislabel = f'$C_M$ [-]'
        elif 'CD' in name:
            axislabel = f'$C_D$ [-]'
        elif 'delta_e' in name:
            axislabel = f'$\\delta_e$ [deg]'
        elif 'CT' in name:
            axislabel = f'$C_T$ [-]'
        elif 'J' in name:
            axislabel = f'J [-]'
        elif 'LD' in name:
            axislabel = f'$C_L$/$C_D$ [-]'
        else:
            axislabel = ''
            print(f'{name} is not in the database. The following options exist: AoA, CL, CD, CM, CT, delta_e. If you want additional ones, ask Dorothé.')

        if 'trim' in name:
            axislabel = f'{axislabel} (trim)'

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
        plt.rcParams.update({'font.size': 15})
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlabel(self.get_axislabel(self.x_name))
        ax.set_ylabel(self.get_axislabel(self.y_name))

        savename = f'{self.x_name}_vs_{self.y_name}-{self.data_type}'

        if all(item is None for item in self.xlim):
            self.xlim[0] = self.x_range[0]
            self.xlim[1] = self.x_range[-1]

        ax.set_xticks(self.generate_xticks(self.xlim[0], self.xlim[1]))
        ax.set_xlim(self.xlim)

        if self.grid:
            ax.grid()

        return fig, ax, savename

    def plot_data_class_lst(self, fig, ax, savename):

        for i, function in enumerate(self.data_to_plot):
            function_label = f'V = {function.tunnel_speed} m/s, J = {function.propeller_speed}'

            ax.plot(self.x_range, function.poly_coeff(self.x_range), '-.', color=self.colors[i], label=function_label)
            ax.scatter(function.data_points[function.x_variable], function.data_points[function.y_variable], color=self.colors[i])

        if self.legend:
            ax.legend()

        fig.tight_layout()
        plt.savefig(f"../Figures/{savename}.svg")

        return

    def plot_lists(self, fig, ax, plotting_data, type_lst, labels_lst, savename):
        if len(plotting_data) == 1:
            ax.plot(self.x_range, plotting_data, color=self.colors[0])

        elif len(plotting_data) > 2:
            i = 0
            counter = 0
            if 'line' in type_lst and 'scatter' in type_lst:
                # for j, i in enumerate(range(0, len(plotting_data), 4)):
                for j, one_type in enumerate(type_lst):
                    if 'line' in one_type:
                        if self.list_labels is not None:
                            ax.plot(plotting_data[i], plotting_data[i + 1], '-.', color=self.colors[counter], label=labels_lst[j])
                            i += 4
                            counter += 1
                        else:
                            ax.plot(plotting_data[i], plotting_data[i + 1], '-.', color=self.colors[j])
                    elif 'scatter' in one_type:
                        ax.scatter(plotting_data[i - 2], plotting_data[i - 1], color=self.colors[counter - 1])

            elif 'scatter' not in type_lst:
                for j, i in enumerate(range(0, len(plotting_data), 2)):
                    for one_type in type_lst:
                        if 'line' in one_type:
                            if self.list_labels is not None:
                                ax.plot(plotting_data[i], plotting_data[i + 1], color=self.colors[j], label=labels_lst[j])
                            else:
                                ax.plot(plotting_data[i], plotting_data[i + 1], color=self.colors[j])

        else:
            print('Please provide x and y list of values.')

        if self.legend:
            ax.legend()

        fig.tight_layout()
        plt.savefig(f"../Figures/{savename}.svg")
        return

    def curve_fit(self, fig, ax, savename):
        order = int(input('Please provide order of fit: '))
        type_lst = []
        label_lst = []

        if len(self.data) == 2:
            polyfit = np.poly1d(np.polyfit(self.data[0], self.data[1], order))

            # Append the polyfit line
            self.data_to_plot.append(self.x_range)
            self.data_to_plot.append(polyfit(self.x_range))
            type_lst.append(['line'])
            label_lst.append(self.list_labels[0])

            # Append the points
            self.data_to_plot.append(self.data[0])
            self.data_to_plot.append(self.data[1])
            type_lst.append('scatter')
            label_lst.append(self.list_labels[0])

        elif len(self.data) > 2:
            for j, i in enumerate(range(0, len(self.data), 2)):
                polyfit = np.poly1d(np.polyfit(self.data[i], self.data[i + 1], order))

                # Append the line
                self.data_to_plot.append(self.x_range)
                self.data_to_plot.append(polyfit(self.x_range))
                type_lst.append('line')
                label_lst.append(self.list_labels[j])

                # Append the points
                self.data_to_plot.append(self.data[i])
                self.data_to_plot.append(self.data[i + 1])
                type_lst.append('scatter')
                label_lst.append(self.list_labels[j])

        self.plot_lists(fig, ax, self.data_to_plot, type_lst, label_lst, savename)

        if self.legend:
            ax.legend()

        # fig.tight_layout()
        # plt.savefig(f"../Figures/{savename}.svg")


if __name__ == "__main__":
    n = 40
    x_axis_range = np.linspace(-10, 20, 100)
    function1 = np.poly1d([0.5, 5])
    ylst1 = function1(x_axis_range)
    function2 = np.poly1d([-0.5, 5])
    ylst2 = function2(x_axis_range)

    plot = PlotData('AoA', 'CL', x_axis_range, [x_axis_range, ylst1, x_axis_range, ylst2], 'lists', ['labeltest', 'test2'])

    plt.show()
