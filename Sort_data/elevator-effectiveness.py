"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

file1 = os.path.join(current_dir, 'bal_sorted1.csv')
file2 = os.path.join(current_dir, 'bal_sorted2.csv')
file3 = os.path.join(current_dir, 'bal_sorted3.csv')


bal_sorted_min15 = pd.read_csv(file1)
bal_sorted_0 = pd.read_csv(file2)
bal_sorted_15 = pd.read_csv(file3)

colors = ['b', 'g', 'c', 'r', 'k', 'm', 'tab:orange', 'grey']


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


def plot_from_dataframe(dataframe, order, x_var_name, y_var_name, inp_lst, x_axis_range, xlabel, ylabel):
    """
    Plots data from a dataframe.
    :param dataframe: A dataframe of the tunnel data
    :param order: Order of the polyfit
    :param x_var_name: name of the dataset to be used for x values
    :param y_var_name: name of the dataset to be used for y values
    :param inp_lst: list of combinations of tunnel and propeller speed
    :param x_axis_range: linspace range for the x-axis
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :return: a plot of the submitted data
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(len(inp_lst)):
        dat = get_function_set(dataframe, inp_lst[i][0], inp_lst[i][1])

        # Use a polynomial data fit ## order 2
        curve_fit = np.poly1d(np.polyfit(dat[x_var_name], dat[y_var_name], order))
        lab = 'V = '+str(round(np.mean(dat['V']))) + ' m/s, J = ' + str(round(np.mean(dat['rounded_J']), 1))

        ax.plot(x_axis_range, curve_fit(x_axis_range), '-.', color=colors[i], label=lab)
        ax.scatter(dat[x_var_name], dat[y_var_name], color=colors[i])
        ax.legend()

    ax.grid()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks([i for i in np.arange(x_axis_range[0] - 2, x_axis_range[-1] + 2, 2)])
    ax.set_xlim([x_axis_range[0], x_axis_range[-1]])


# Slice the zero deflection array such that the new dataframe contains the same data points
rows = [0, 12, 17, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 42, 47, 49]
bal_sorted_0_sliced1 = bal_sorted_0.iloc[rows]
bal_sorted_0_sliced = pd.concat([bal_sorted_0_sliced1, bal_sorted_0[50:]])

# Make an array with all Cm coefficients and polyfit to line to return the slopes aka Cm delta
CM_array = np.array([bal_sorted_min15['CMpitch'], bal_sorted_0_sliced['CMpitch'], bal_sorted_15['CMpitch']])
delta_e_array_deg = [-15, 0, 15]    # deg
coeff_CM = np.polyfit(np.transpose(delta_e_array_deg), CM_array, 1)

# Make a dataframe consisting the slopes, AoA, V and K
cm_slope = pd.DataFrame(data=({'CM_de': coeff_CM[0]}))
cm_datapoints = bal_sorted_15.loc[:, ['AoA', 'rounded_AoA', 'V', 'rounded_v', 'J_M1', 'rounded_J']]
cm_dataframe = pd.concat([cm_datapoints, cm_slope], axis=1)

# Plot the dCM/d deltae and CL for the set of tunnel and propeller speeds combinations
tunnel_prop_combi = [[{'rounded_v': 40}, {'rounded_J': 1.6}],
                     [{'rounded_v': 40}, {'rounded_J': 1.8}],
                     [{'rounded_v': 40}, {'rounded_J': 3.5}],
                     [{'rounded_v': 20}, {'rounded_J': 1.6}],
                     [{'rounded_v': 10}, {'rounded_J': 1.6}],
                     [{'rounded_v': 40}, {'rounded_J': 17}],
                     [{'rounded_v': 20}, {'rounded_J': 17}],
                     [{'rounded_v': 10}, {'rounded_J': 17}]]

plot_from_dataframe(cm_dataframe, 2, 'AoA', 'CM_de', tunnel_prop_combi, np.linspace(-6, 20, 26),
                    f'$\\alpha$ [deg]', r'$\frac{\partial C_M}{\partial \delta_e}$')

plot_from_dataframe(bal_sorted_15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26),
                    f'$\\alpha$ [deg]', f'$C_L$')


plt.show()
