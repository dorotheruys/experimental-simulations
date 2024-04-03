"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_set
from Corrections.Lift_interference import df_velocity_filter_tailoff
from General.trim_point import get_cm_cg_cor_all_elevator, l_cg, l_ac_ac, data_corrected_min15, data_corrected_0, data_corrected_15, get_function_from_dataframe

tunnel_prop_combi_Re = [[{'V cor': 40}, {'rounded_J': 1.6}],
                     [{'V cor': 20}, {'rounded_J': 1.6}]]

used_aoa = [[{'AoA cor': -5}, None],
            [{'AoA cor': 7}, None],
            [{'AoA cor': 12}, None],
            [{'AoA cor': 14}, None]]

used_deltae_V = [[{'V cor': 40}, {'delta_e': -15}],
              [{'V cor': 40}, {'delta_e': 0}],
              [{'V cor': 40}, {'delta_e': 15}]]

if __name__ == "__main__":
    # Get the tail-off data
    data_tailoff_40 = df_velocity_filter_tailoff(40)
    data_tailoff_20 = df_velocity_filter_tailoff(20)
    tail_off_data = [data_tailoff_20, data_tailoff_20, data_tailoff_40]

    # Determine the corrected CM for all tunnel velocities
    CM_cg_cor = get_cm_cg_cor_all_elevator(tail_off_data, [data_corrected_min15, data_corrected_0, data_corrected_15], l_ac_ac, l_cg)
    CM_cg_cor['LD cor'] = CM_cg_cor['CL_total cor'] / CM_cg_cor['CD cor']

    # Slice per elevator deflection
    CM_cg_cor_min15 = get_function_set(CM_cg_cor, {'delta_e': -15}, None)
    CM_cg_cor_0 = get_function_set(CM_cg_cor, {'delta_e': 0}, None)
    CM_cg_cor_15 = get_function_set(CM_cg_cor, {'delta_e': 15}, None)

    # Get the same datapoints for delta_e = 0 as the others have
    CM_cg_cor_0_sliced_lst = []
    for item in used_aoa:
        CM_cg_cor_0_slice = get_function_set(CM_cg_cor_0, item[0], None)
        CM_cg_cor_0_sliced_lst.append(CM_cg_cor_0_slice)
    CM_cg_cor_0_sliced = pd.concat(CM_cg_cor_0_sliced_lst, axis=0)

    # 1. CL vs alpha with J = 1.6, delta_e = 0
    get_function_from_dataframe(CM_cg_cor_0, 2, 'AoA cor', 'CL_total cor', tunnel_prop_combi_Re, np.linspace(-6, 15, 100), 'AoA', 'CL')

    # 2. CD vs CL with J = 1.6, delta_e = 0
    get_function_from_dataframe(CM_cg_cor_0, 4, 'CL_total cor', 'CD cor', tunnel_prop_combi_Re, np.linspace(-0.3, 1.5, 100), 'CL', 'CD')

    # 3. Cm vs AoA with J = 1.6, delta_e = 0
    get_function_from_dataframe(CM_cg_cor_0, 5, 'AoA cor', 'CM_total', tunnel_prop_combi_Re, np.linspace(-6, 15, 100), 'AoA', 'CM')

    # 4. CL/CD vs AoA with J = 1.6, delta_e = 0
    get_function_from_dataframe(CM_cg_cor_0, 6, 'AoA cor', 'LD cor', tunnel_prop_combi_Re, np.linspace(-6, 15, 100), 'AoA', 'LD')

    plt.show()
