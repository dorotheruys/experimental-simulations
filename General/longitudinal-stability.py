"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_from_dataframe, get_function_set
from General.trim_point import get_cm_cg_cor_all_elevator
from Corrections.Lift_interference import df_velocity_filter_tailoff


tunnel_prop_combi = [[{'V cor': 40}, {'rounded_J': 1.6}],
                     [{'V cor': 40}, {'rounded_J': 1.8}],
                     [{'V cor': 40}, {'rounded_J': 3.5}],
                     [{'V cor': 20}, {'rounded_J': 1.6}],
                     [{'V cor': 10}, {'rounded_J': 1.6}]]

used_aoa = [{'AoA cor': -5},
            {'AoA cor': 7},
            {'AoA cor': 12},
            {'AoA cor': 14}]

# chord-wise location assumptions
MAC_w = 0.165       # [m]
MAC_HT = 0.149      # [m]
l_ac_w = (0.33 - 0.25) * MAC_w
l_ac_ht = 3.22 * MAC_w + (0.33 - 0.25) * MAC_HT
l_cg = (0.35 - 0.25) * MAC_w

# Slice the zero deflection array such that the new dataframe contains the same data points
rows = [0, 12, 17, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 42, 47, 49]


if __name__ == "__main__":
    # Get the data
    data_corrected_min15 = pd.read_csv('../Sort_data/cor_data_min15.csv')
    data_corrected_0 = pd.read_csv('../Sort_data/cor_data_0.csv')
    data_corrected_15 = pd.read_csv('../Sort_data/cor_data_15.csv')

    # Get the tail-off data
    data_tailoff_40 = df_velocity_filter_tailoff(40)
    data_tailoff_20 = df_velocity_filter_tailoff(20)
    tail_off_data = [data_tailoff_20, data_tailoff_20, data_tailoff_40]

    # Determine the corrected CM for all tunnel velocities
    CM_cg_cor = get_cm_cg_cor_all_elevator(tail_off_data, [data_corrected_min15, data_corrected_0, data_corrected_15], l_ac_w, l_ac_ht, l_cg, MAC_w)

    CM_cg_cor_min15 = get_function_set(CM_cg_cor, {'delta_e': -15}, None)
    CM_cg_cor_0 = get_function_set(CM_cg_cor, {'delta_e': 0}, None)
    CM_cg_cor_15 = get_function_set(CM_cg_cor, {'delta_e': 15}, None)

    CM_cg_cor_0_sliced_lst = []
    for item in used_aoa:
        CM_cg_cor_0_slice = get_function_set(CM_cg_cor_0, item, None)
        CM_cg_cor_0_sliced_lst.append(CM_cg_cor_0_slice)
    CM_cg_cor_0_sliced = pd.concat(CM_cg_cor_0_sliced_lst, axis=0)

    # Plot CM vs AoA for delta = -15
    get_function_from_dataframe(CM_cg_cor_min15, 2, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    # Plot CM vs AoA for delta = 0
    get_function_from_dataframe(CM_cg_cor_0_sliced, 2, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    # Plot CM vs AoA for delta = 15
    get_function_from_dataframe(CM_cg_cor_15, 2, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    plt.show()
