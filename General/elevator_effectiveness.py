"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_from_dataframe, get_function_set
from Corrections.Lift_interference import df_velocity_filter_tailoff
from General.trim_point import get_cm_cg_cor_all_elevator, trim_points_all_aoa


# def get_aoa_combis(aoa):
#     combis = [[{'rounded_AoA': aoa}, {'rounded_v': 40}]]
#         # ,
#         #       [{'rounded_AoA': aoa}, {'rounded_v': 20}],
#         #       [{'rounded_AoA': aoa}, {'rounded_v': 10}]]
#     return combis
#
#
# def get_cm_vs_elevator(cm_datapoints, plot):
#     # Extract each CM from the data (and reset the indices of the zero angle)
#     CM_min15 = pd.concat([cm_datapoints, pd.DataFrame({'delta_e': [-15]*len(cm_datapoints)}), bal_sorted_min15['CMpitch']], axis=1)
#     CM_0 = pd.concat([bal_sorted_0[['AoA', 'rounded_AoA', 'V', 'rounded_v', 'J_M1', 'rounded_J']], pd.DataFrame({'delta_e': [0]*len(bal_sorted_0)}), bal_sorted_0['CMpitch'].reset_index(drop=True)], axis=1)
#     CM_15 = pd.concat([cm_datapoints, pd.DataFrame({'delta_e': [15]*len(cm_datapoints)}), bal_sorted_15['CMpitch']], axis=1)
#
#     # Make one large dataframe of all relevant data points to construct the graph
#     CM_df = pd.concat([CM_min15, CM_0, CM_15], axis=0, ignore_index=True)
#
#     # Get a dataframe for one specific AoA
#     CM_df_AoA7 = get_function_set(CM_df, {'rounded_AoA': 7}, None)
#
#     # Plot
#     if plot is None:
#         cm_deltae_plotting_lst = get_function_from_dataframe(CM_df_AoA7, 1, 'delta_e', 'CMpitch', tunnel_prop_combi, np.linspace(-20, 20, 50), None, None)
#     else:
#         cm_deltae_plotting_lst = get_function_from_dataframe(CM_df_AoA7, 1, 'delta_e', 'CMpitch', tunnel_prop_combi, np.linspace(-20, 20, 50), f'$\\delta_e$ [deg]', r'$C_M$ [-]')
#
#     return cm_deltae_plotting_lst
#
#
# def get_slope_cm_vs_aoa(cm_datapoints):
#     # Make an array with all Cm coefficients and polyfit to line to return the slopes aka Cm delta
#     CM_array = np.array([bal_sorted_min15['CMpitch'], bal_sorted_0_sliced['CMpitch'], bal_sorted_15['CMpitch']])
#     delta_e_array = [-15, 0, 15]    # deg
#     coeff_CM = np.polyfit(np.transpose(delta_e_array), CM_array, 1)
#
#     # Make a dataframe consisting the slopes, AoA, V and K
#     cm_slope = pd.DataFrame(data=({'CM_de': coeff_CM[0]}))
#
#     dcm_dataframe = pd.concat([cm_datapoints, cm_slope], axis=1)
#
#     # Get plot for AoA versus dCM/d delta_e, for each V & J combination
#     dcm_ddeltae_plotting_lst = get_function_from_dataframe(dcm_dataframe, 2, 'AoA', 'CM_de', tunnel_prop_combi, np.linspace(-6, 20, 26), f'$\\alpha$ [deg]', r'$\frac{\partial C_M}{\partial \delta_e}$ [-]')
#
#     return dcm_ddeltae_plotting_lst

def get_CL_for_trim(data, tunnel_speed, propeller_speed, aoa_combis):
    data_sliced_V40_J18 = get_function_set(data, {'V cor': tunnel_speed}, {'rounded_J': propeller_speed})

    # A list of CL vs delta_e function for each AoA: -5, 7, 12, 14 for 1 V-J combi
    CL_vs_delta_e_functions = get_function_from_dataframe(data_sliced_V40_J18, 1, 'delta_e', 'CL_total cor', aoa_combis, np.linspace(-20, 20, 200), 'delta_e', 'CL')

    # A list of CM vs delta_e functions for each AoA: -5, 7, 12, 14 for 1 V-J combi
    function_lst = trim_points_all_aoa(data_sliced_V40_J18, [[{'V cor': tunnel_speed}, {'rounded_J': propeller_speed}]])

    AoA_trim_lst = []
    CL_trim_lst = []
    for i, function in enumerate(function_lst):
        delta_e_trim = function[0].trim_point

        CL_delta_e_function = CL_vs_delta_e_functions[i]
        CL_trim_AoA = CL_delta_e_function.poly_coeff(delta_e_trim)

        AoA_trim_lst.append(function[0].trim_aoa)
        CL_trim_lst.append(CL_trim_AoA)
    return


tunnel_prop_combi = [[{'V cor': 40}, {'rounded_J': 1.6}],
                     [{'V cor': 40}, {'rounded_J': 1.8}],
                     [{'V cor': 40}, {'rounded_J': 3.5}],
                     [{'V cor': 20}, {'rounded_J': 1.6}],
                     [{'V cor': 10}, {'rounded_J': 1.6}]]

used_aoa = [[{'AoA cor': -5}, None],
            [{'AoA cor': 7}, None],
            [{'AoA cor': 12}, None],
            [{'AoA cor': 14}, None]]

# chord-wise location assumptions
MAC_w = 0.165       # [m]
MAC_HT = 0.149      # [m]
l_ac_w = (0.33 - 0.25) * MAC_w
l_ac_ht = 3.22 * MAC_w + (0.33 - 0.25) * MAC_HT
l_cg = (0.35 - 0.25) * MAC_w

# Assumed approach AoA

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
        CM_cg_cor_0_slice = get_function_set(CM_cg_cor_0, item[0], None)
        CM_cg_cor_0_sliced_lst.append(CM_cg_cor_0_slice)
    CM_cg_cor_0_sliced = pd.concat(CM_cg_cor_0_sliced_lst, axis=0)


    # data_sliced_V40_J18 = get_function_set(CM_cg_cor, {'V cor': 40}, {'rounded_J': 1.8})
    # get_function_from_dataframe(data_sliced_V40_J18, 1, 'delta_e', 'CL_total cor', used_aoa, np.linspace(-20, 20, 200), 'delta_e', 'CL')
    # get_function_from_dataframe(data_sliced_V40_J18, 2, 'AoA cor', 'CL_total cor', [[{'V cor': 40}, {'rounded_J': 1.8}]], np.linspace(-10, 20, 100), 'AoA', 'CL')

    # CM_function_lst = trim_points_all_aoa(data_sliced_V40_J18, [[{'V cor': 40}, {'rounded_J': 1.8}]])
    get_CL_for_trim(CM_cg_cor, 40, 1.8, used_aoa)

    # Get plot for AoA vs CL, for each V & J combination
    get_function_from_dataframe(CM_cg_cor_0_sliced, 2, 'AoA cor', 'CL_total cor', tunnel_prop_combi, np.linspace(-10, 20, 100), f'$\\alpha$ [deg]', f'$C_L$ [-]')

    # Get plot for AoA vs CM, for each V & J combination
    get_function_from_dataframe(CM_cg_cor_0_sliced, 2, 'AoA cor', 'CM_0.25c_total', tunnel_prop_combi, np.linspace(-10, 20, 100), f'$\\alpha$ [deg]', f'$C_M$ [-]')

    # Get plot for CD vs CL, for each V & J combination
    get_function_from_dataframe(CM_cg_cor_0_sliced, 2, 'CL_total cor', 'CD cor', tunnel_prop_combi, np.linspace(-1, 1.7, 100), f'$C_L$ [-]', f'$C_D$ [-]')

    plt.show()
