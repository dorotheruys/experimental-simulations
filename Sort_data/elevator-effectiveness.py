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
tunnel_prop_combi = [(40, 1.6), (40, 1.8), (40, 3.5), (20, 1.6), (10, 1.6), (40, 17), (20, 17), (10, 17)]


def get_set(data, vel, prop):
    if prop == 'off':
        prop = 17
        group1 = data.groupby('rounded_J')
        layer1 = group1.get_group(prop)

        group2 = layer1.groupby('rounded_v')
        layer2 = group2.get_group(vel)
    else:

        group1 = data.groupby('rounded_v')
        layer1 = group1.get_group(vel)

        group2 = layer1.groupby('rounded_J')
        layer2 = group2.get_group(prop)

    return layer2.sort_values(by='AoA')


def plot_from_dataframe(dataframe, x_name, y_name, inp_lst, xlabel, ylabel):
    """
    Plots data from a dataframe.
    :param dataframe: A dataframe of the tunnel data
    :param x_name: name of the dataset to be used for x values
    :param y_name: name of the dataset to be used for y values
    :param inp_lst: list of combinations of tunnel and propeller speed
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :return: a plot of the submitted data
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    # X axis for curve fitting
    x_axis = np.linspace(-20, 20, 26)

    for i in range(len(inp_lst)):
        dat = get_set(dataframe, inp_lst[i][0], inp_lst[i][1])

        # Use a polynomial data fit ## order 2
        curve_fit = np.poly1d(np.polyfit(dat[x_name], dat[y_name], 2))
        lab = 'V = '+str(round(np.mean(dat['V']))) + ' m/s, J = ' + str(round(np.mean(dat['rounded_J']), 1))

        ax.plot(x_axis, curve_fit(x_axis), '-.', color=colors[i], label=lab)
        ax.scatter(dat[x_name], dat[y_name], color=colors[i])
        ax.legend(loc="upper right")

    ax.grid()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks([i for i in np.arange(x_axis[0] - 2, x_axis[-1] + 2, 2)])
    ax.set_xlim([x_axis[0] - 2, x_axis[-1] + 2])


# Slice the zero deflection array such that the new dataframe contains the same data points
rows = [0, 12, 17, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 42, 47, 49]
bal_sorted_0_sliced1 = bal_sorted_0.iloc[rows]
bal_sorted_0_sliced = pd.concat([bal_sorted_0_sliced1, bal_sorted_0[50:]])

# Make an array with all Cm coefficients and polyfit to line to return the slopes aka Cm delta
CM_array = np.array([bal_sorted_min15['CMpitch'], bal_sorted_0_sliced['CMpitch'], bal_sorted_15['CMpitch']])
delta_e_array_deg = [-15, 0, 15]    # deg
coeff_CM = np.polyfit(np.transpose(delta_e_array_deg), CM_array, 1)
cm_slope = pd.DataFrame(data=({'CM_de': coeff_CM[0]}))
cm_datapoints = bal_sorted_15.loc[:, ['AoA', 'rounded_AoA', 'V', 'rounded_v', 'J_M1', 'rounded_J']]

cm_dataframe = pd.concat([cm_datapoints, cm_slope], axis=1)
plot_from_dataframe(cm_dataframe, 'AoA', 'CM_de', tunnel_prop_combi, f'$\\alpha$ [deg]', r'$\frac{\partial C_M}{\partial \delta_e}$')
plt.yticks([i for i in np.arange(-0.05, 0, 0.005)])

plt.show()
