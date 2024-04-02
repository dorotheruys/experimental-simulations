"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_set
from Corrections.Lift_interference import df_velocity_filter_tailoff
from General.trim_point import get_cm_cg_cor_all_elevator, l_cg, l_ac_ac, data_corrected_min15, data_corrected_0, data_corrected_15, get_function_from_dataframe
from General.elevator_effectiveness import get_data_for_j
from Plotting.plotter import PlotData


def get_slope_cm_aoa(df_cm_data):
    df_CM_AoA_min5 = get_function_set(df_cm_data, {'AoA cor': -5}, None).sort_values(by=['rounded_v', 'rounded_J'])
    df_CM_AoA_7 = get_function_set(df_cm_data, {'AoA cor': 7}, None).sort_values(by=['rounded_v', 'rounded_J'])
    df_CM_AoA_12 = get_function_set(df_cm_data, {'AoA cor': 12}, None).sort_values(by=['rounded_v', 'rounded_J'])
    df_CM_AoA_14 = get_function_set(df_cm_data, {'AoA cor': 14}, None).sort_values(by=['rounded_v', 'rounded_J'])

    # Make an array with all Cm coefficients
    CM_arr = np.array([df_CM_AoA_min5['CM_total'], df_CM_AoA_7['CM_total'], df_CM_AoA_12['CM_total'], df_CM_AoA_14['CM_total']])
    AoA_arr = [-5, 7, 12, 14]

    # Polyfit to line to return the slopes aka Cm delta
    coeff_CM_aoa = np.polyfit(np.transpose(AoA_arr), CM_arr, 1)

    # Make a dataframe consisting the slopes, AoA, V and K
    dCM_dAlpha_arr = coeff_CM_aoa[0]

    # Get the corresponding delta_e
    delta_e_arr = np.array(df_CM_AoA_min5['delta_e'].to_list())

    # Get the full corresponding AoA
    AoA_full_arr = np.array(df_CM_AoA_min5['AoA cor'].to_list())

    # Get the corresponding J
    J_arr = np.array(df_CM_AoA_min5['rounded_J'].to_list())

    # Get the corresponding V
    V_arr = np.array(df_CM_AoA_min5['V cor'].to_list())

    return pd.DataFrame(data=({'delta_e': delta_e_arr, 'AoA': AoA_full_arr, 'AoA cor': AoA_full_arr, 'V cor': V_arr, 'rounded_J': J_arr, 'dCm_dAoA': dCM_dAlpha_arr}))


tunnel_prop_combi = [[{'V cor': 40}, {'rounded_J': 1.6}],
                     [{'V cor': 40}, {'rounded_J': 1.8}],
                     [{'V cor': 40}, {'rounded_J': 3.5}]]

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

    # Plot CM vs AoA for delta = -15
    # get_function_from_dataframe(CM_cg_cor_min15, 1, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    # Plot CM vs AoA for delta = 0
    # get_function_from_dataframe(CM_cg_cor_0_sliced, 1, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 18, 100), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    # Plot CM vs AoA for delta = 15
    # get_function_from_dataframe(CM_cg_cor_15, 1, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    # Plot dCmdAlpha vs J
    # df_dCM_dAoA = get_slope_cm_aoa(CM_cg_cor)
    # df_dCM_dAoA_lst, df_dCM_dAoA_labels_lst = get_data_for_j(df_dCM_dAoA, used_deltae_V, 'rounded_J', 'dCm_dAoA', 'delta_e')
    # PlotData('rounded_J', 'dCm_dAoA', np.linspace(1.5, 4, 100), df_dCM_dAoA_lst, 'curvefit', df_dCM_dAoA_labels_lst)

    plt.show()
