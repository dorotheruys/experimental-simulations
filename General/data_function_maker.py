"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# colors = ['b', 'g', 'c', 'r', 'k', 'm', 'tab:orange', 'grey']
colors = ["#00A6B6", "#A50034", "#EF60A3", "#6CC24A", "#FFB81C", "#6F1D77", "#EC6842", "#000000"]
#           cyan,   raspberry,    pink,   light green, yellow,     purple,     orange,   black


class FunctionData:
    """
    Class to save the polyfit coefficients with the corresponding data
    """
    def __init__(self, name: str, tunnel_speed: float, propeller_speed: float, x_variable: str, y_variable: str, poly_coeff: np.poly1d, data_points: pd.DataFrame):
        self.name: str = name
        self.tunnel_speed: float = tunnel_speed
        self.propeller_speed: float = propeller_speed
        self.x_variable: str = x_variable
        self.y_variable: str = y_variable
        self.poly_coeff: np.poly1d = poly_coeff
        self.data_points: pd.DataFrame = data_points
        self.trim_point = None


def plot_function_data(plot_data: list, xlabel: str, ylabel: str, x_axis_range: np.array):
    """
    Makes a plot of a list of FunctionData classes
    :param plot_data: list of FunctionData classes
    :param xlabel: Label for the x-axis, incl unit
    :param ylabel: Label for y-axis, incl unit
    :param x_axis_range: range for the x-axis
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, function in enumerate(plot_data):
        function_label = f'V = {function.tunnel_speed} m/s, J = {function.propeller_speed}'
        ax.plot(x_axis_range, function.poly_coeff(x_axis_range), '-.', color=colors[i], label=function_label)
        ax.scatter(function.data_points[function.x_variable], function.data_points[function.y_variable], color=colors[i])

    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks([i for i in
                   np.arange(x_axis_range[0] - 2, x_axis_range[-1] + 2.1, (x_axis_range[-1] - x_axis_range[0]) / 10)])
    ax.set_xlim([x_axis_range[0], x_axis_range[-1]])


def get_function_set(data, var1, var2):
    """
    returns the data filtered by var1 and var2, sorted by 'AoA'
    :param data: dataframe
    :param var1: {"name": value}
    :param var2: {"name": value}
    """

    name1 = list(var1.keys())[0]
    layer1 = data[(data[name1] <= var1[name1] + 0.45) & (data[name1] >= var1[name1] - 0.45)]

    if var2 is not None:
        name2 = list(var2.keys())[0]    # eg: 'rounded_J'
        layer2 = layer1[(layer1[name2] <= var2[name2] + 0.1) & (layer1[name2] >= var2[name2] - 0.1)]
        return layer2.sort_values(by='AoA')
    else:
        return layer1.sort_values(by='AoA')


def get_function_from_dataframe(dataframe: pd.DataFrame, order: int, x_var_name: str, y_var_name: str, inp_lst: list, x_axis_range: np.array, xlabel: [str, None], ylabel: [str, None]):
    """
    Plots data from a dataframe based on variables names of x and y for the given combinations of V and J. Note that these should be the same names as the
    column names of the dataframe for the function to work.
    :param dataframe: A dataframe of the tunnel data
    :param order: Order of the polyfit
    :param x_var_name: name of the dataset to be used for x values
    :param y_var_name: name of the dataset to be used for y values
    :param inp_lst: list of dictionaries with the combinations of tunnel and propeller speed
    :param x_axis_range: np.linspace range for the x-axis
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :return: a plot of the submitted data
    """
    dict_f = {}
    f_lst = []

    for i in range(len(inp_lst)):
        dat = get_function_set(dataframe, inp_lst[i][0], inp_lst[i][1])

        # Use a polynomial data fit with prescribed order
        polyfit = np.polyfit(dat[x_var_name], dat[y_var_name], order, full=True)
        curve_fit = np.poly1d(polyfit[0])
        # print(f"Residual values for {order} order fit: {polyfit[1]}")

        # Create label with V and J
        var1 = round(np.mean(dat['rounded_v']))
        var2 = round(np.mean(dat['rounded_J']), 2)

        # Save the poly coefficients to a class with corresponding var1 and var2
        name = f'{y_var_name}vs{x_var_name}_V{var1}_J{var2}'
        correspondingClass = FunctionData(name, var1, var2, x_var_name, y_var_name, curve_fit, dat)
        dict_f[f"V_{var1}_J_{var2}"] = correspondingClass
        f_lst.append(correspondingClass)

    # Plot
    if xlabel is not None and ylabel is not None:
        plot_function_data(f_lst, xlabel, ylabel, x_axis_range)
    else:
        # print("The data has not been plotted. Please fill in the correct fields if wanted.")
        print(" ")

    return f_lst


def extract_from_list_classes(function_datas: list, tunnel_speed: int, propeller_speed: float):
    """
    Extracts the polyline coefficients based on a tunnel and propeller speed combination.
    :param function_datas: a list of FunctionClass classes that contain the data
    :param tunnel_speed: the tunnel speed
    :param propeller_speed: the propeller speed
    """
    for function in function_datas:
        if function.tunnel_speed == tunnel_speed and function.propeller_speed == propeller_speed:
            return function.poly_coeff
        else:
            pass
