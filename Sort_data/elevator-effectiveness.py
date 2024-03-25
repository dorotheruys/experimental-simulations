"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import os
from General.data_function_maker import get_function_from_dataframe

current_dir = os.path.dirname(os.path.abspath(__file__))

file1 = os.path.join(current_dir, 'bal_sorted1.csv')
file2 = os.path.join(current_dir, 'bal_sorted2.csv')
file3 = os.path.join(current_dir, 'bal_sorted3.csv')

bal_sorted_min15 = pd.read_csv(file1)
bal_sorted_0 = pd.read_csv(file2)
bal_sorted_15 = pd.read_csv(file3)


# Slice the zero deflection array such that the new dataframe contains the same data points
rows = [0, 12, 17, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 42, 47, 49]
bal_sorted_0_sliced1 = bal_sorted_0.iloc[rows]
bal_sorted_0_sliced = pd.concat([bal_sorted_0_sliced1, bal_sorted_0[50:]])

# Make an array with all Cm coefficients and polyfit to line to return the slopes aka Cm delta
CM_array = np.array([bal_sorted_min15['CMpitch'], bal_sorted_0_sliced['CMpitch'], bal_sorted_15['CMpitch']])
CM_df = pd.DataFrame(data=())
delta_e_array_deg = [-15, 0, 15]    # deg
coeff_CM = np.polyfit(np.transpose(delta_e_array_deg), CM_array, 1)

# Make a dataframe consisting the slopes, AoA, V and K
cm_slope = pd.DataFrame(data=({'CM_de': coeff_CM[0]}))
cm_datapoints = bal_sorted_15.loc[:, ['AoA', 'rounded_AoA', 'V', 'rounded_v', 'J_M1', 'rounded_J']]
dcm_dataframe = pd.concat([cm_datapoints, cm_slope], axis=1)

tunnel_prop_combi = [[{'rounded_v': 40}, {'rounded_J': 1.6}],
                     [{'rounded_v': 40}, {'rounded_J': 1.8}],
                     [{'rounded_v': 40}, {'rounded_J': 3.5}],
                     [{'rounded_v': 20}, {'rounded_J': 1.6}],
                     [{'rounded_v': 10}, {'rounded_J': 1.6}],
                     [{'rounded_v': 40}, {'rounded_J': 17}],
                     [{'rounded_v': 20}, {'rounded_J': 17}],
                     [{'rounded_v': 10}, {'rounded_J': 17}]]

# Get plot for AoA versus dCM/d delta_e, for each V & J combination
cm_plotting_lst = get_function_from_dataframe(dcm_dataframe, 2, 'AoA', 'CM_de', tunnel_prop_combi, np.linspace(-6, 20, 26), f'$\\alpha$ [deg]', r'$\frac{\partial C_M}{\partial \delta_e}$ [-]')

# Get plot for AoA vs CL, for each V & J combination
get_function_from_dataframe(bal_sorted_15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), f'$\\alpha$ [deg]', f'$C_L$ [-]')

# Get plot for CD vs CL, for each V & J combination
get_function_from_dataframe(bal_sorted_15, 2, 'CL', 'CD', tunnel_prop_combi, np.linspace(-1, 1.7, 26), f'$C_L$ [-]', f'$C_D$ [-]')


plt.show()
