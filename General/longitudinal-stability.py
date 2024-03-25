"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_from_dataframe

# Get the data
bal_sorted_min15 = pd.read_csv('../Sort_data/bal_sorted1.csv')
bal_sorted_0 = pd.read_csv('../Sort_data/bal_sorted2.csv')
bal_sorted_15 = pd.read_csv('../Sort_data/bal_sorted3.csv')

tunnel_prop_combi = [[{'rounded_v': 40}, {'rounded_J': 1.6}],
                     [{'rounded_v': 40}, {'rounded_J': 1.8}],
                     [{'rounded_v': 40}, {'rounded_J': 3.5}],
                     [{'rounded_v': 20}, {'rounded_J': 1.6}],
                     [{'rounded_v': 10}, {'rounded_J': 1.6}],
                     [{'rounded_v': 40}, {'rounded_J': 17}],
                     [{'rounded_v': 20}, {'rounded_J': 17}],
                     [{'rounded_v': 10}, {'rounded_J': 17}]]

# Slice the zero deflection array such that the new dataframe contains the same data points
rows = [0, 12, 17, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 42, 47, 49]
bal_sorted_0_sliced1 = bal_sorted_0.iloc[rows]
bal_sorted_0_sliced = pd.concat([bal_sorted_0_sliced1, bal_sorted_0[50:]])

if __name__ == "__main__":
    # Plot CM vs AoA for delta = -15
    get_function_from_dataframe(bal_sorted_min15, 2, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    # Plot CM vs AoA for delta = 0
    get_function_from_dataframe(bal_sorted_0_sliced, 2, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    # Plot CM vs AoA for delta = 15
    get_function_from_dataframe(bal_sorted_15, 2, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    plt.show()
