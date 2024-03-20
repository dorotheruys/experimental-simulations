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


def plot_from_dataframe(dataframe, x_name, y_name, inp_lst):
    """
    Plots data from a dataframe.
    :param dataframe: A dataframe of the tunnel data
    :param x_name: name of the dataset to be used for x values
    :param y_name: name of the dataset to be used for y values
    :param inp_lst: list of combinations of tunnel and propeller speed
    :return: a plot of the submitted data
    """
    fig, ax = plt.subplots()
    # X axis for curve fitting
    x_axis = np.linspace(-5, 25, 26)

    for i in range(len(inp_lst)):
        dat = get_set(dataframe, inp_lst[i][0], inp_lst[i][1])

        # Use a polynomial data fit ## order 2
        curve_fit = np.poly1d(np.polyfit(dat[x_name], dat[y_name], 2))
        lab = 'V = '+str(round(np.mean(dat['V']))) + '  , J = ' + str(round(np.mean(dat['J_M1']), 1))

        ax.plot(x_axis, curve_fit(x_axis), '-.', color=colors[i], abel=lab)
        ax.scatter(dat[x_name], dat[y_name], olor=colors[i])
        ax.legend()

    ax.grid()
    ax.set_ylabel(x_name)
    ax.set_xlabel(y_name)

plot_from_dataframe(bal_sorted_min15, '')
