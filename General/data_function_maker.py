"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

colors = ['b', 'g', 'c', 'r', 'k', 'm', 'tab:orange', 'grey']

class FunctionData:
    def __init__(self, tunnel_speed: float, propeller_speed: float, x_variable: str, poly_coeff: np.poly1d):
        self.tunnel_speed: float = tunnel_speed
        self.propeller_speed: float = propeller_speed
        self.x_variable: str = x_variable
        self.poly_coeff: np.poly1d = poly_coeff


def get_function_set(data, var1, var2):
    """
    returns the data filtered by var1 and var2, sorted by 'AoA'
    :param data: dataframe
    :param var1: {"name": value}
    :param var2: {"name": value}
    """

    name1 = list(var1.keys())[0]
    group1 = data.groupby(name1)      # eg: 'rounded_v'
    layer1 = group1.get_group(var1[name1])

    name2 = list(var2.keys())[0]
    group2 = layer1.groupby(name2)    # eg: 'rounded_J'
    layer2 = group2.get_group(var2[name2])

    return layer2.sort_values(by='AoA')


def plot_from_dataframe(dataframe: pd.DataFrame, order: int, x_var_name: str, y_var_name: str, inp_lst: list,
                        x_axis_range: np.array, xlabel: str, ylabel: str):
    """
    Plots data from a dataframe based on variables names of x and y. Note that these should be the same names as the
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
    fig, ax = plt.subplots(figsize=(10, 6))
    dict_f = {}
    f_lst = []

    for i in range(len(inp_lst)):
        dat = get_function_set(dataframe, inp_lst[i][0], inp_lst[i][1])

        # Use a polynomial data fit with prescribed order
        curve_fit = np.poly1d(np.polyfit(dat[x_var_name], dat[y_var_name], order))

        # Create label with V and J
        var1 = round(np.mean(dat['rounded_v']))
        var2 = round(np.mean(dat['rounded_J']))

        lab = f'V = {var1} m/s, J = {var2}'

        # Plot
        ax.plot(x_axis_range, curve_fit(x_axis_range), '-.', color=colors[i], label=lab)
        ax.scatter(dat[x_var_name], dat[y_var_name], color=colors[i])
        ax.legend()

        # Save the poly coefficients to a class with corresponding var1 and var2
        correspondingClass = FunctionData(var1, var2, x_var_name, curve_fit)
        dict_f[f"V_{var1}_J_{var2}"] = correspondingClass
        f_lst.append(correspondingClass)


    # Set up the plot
    ax.grid()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks([i for i in np.arange(x_axis_range[0] - 2, x_axis_range[-1] + 2, (x_axis_range[-1] - x_axis_range[0]) / 10)])
    ax.set_xlim([x_axis_range[0], x_axis_range[-1]])

    return f_lst


def extract(function_datas: list, tunnel_speed: int, propeller_speed: int):
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