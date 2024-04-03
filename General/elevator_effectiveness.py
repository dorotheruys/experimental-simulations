"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_from_dataframe, get_function_set
from Corrections.Lift_interference import df_velocity_filter_tailoff
from General.trim_point import get_cm_cg_cor_all_elevator, trim_points_all_aoa, l_cg, l_ac_ac, data_corrected_min15, data_corrected_0, data_corrected_15
from Plotting.plotter import PlotData

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


def get_slope_cm_delta(df_cm_data_min15, df_cm_data_0, df_cm_data_15):
    # sort to make sure the columns have the same order
    df_cm_data_min15 = df_cm_data_min15.sort_values(by=['rounded_v', 'rounded_J'])
    df_cm_data_0 = df_cm_data_0.sort_values(by=['rounded_v', 'rounded_J'])
    df_cm_data_15 = df_cm_data_15.sort_values(by=['rounded_v', 'rounded_J'])

    # Make an array with all Cm coefficients
    CM_array = np.array([df_cm_data_min15['CM_total'], df_cm_data_0['CM_total'], df_cm_data_15['CM_total']])
    delta_e_array = [-15, 0, 15]    # deg

    # Polyfit to line to return the slopes aka Cm delta
    coeff_CM_deltae = np.polyfit(np.transpose(delta_e_array), CM_array, 1)

    # Make a dataframe consisting the slopes, AoA, V and K
    dCM_ddelta_e_arr = coeff_CM_deltae[0]

    # Get the corresponding conditions
    AoA_arr = np.array(df_cm_data_min15['AoA'].to_list())
    J_arr = np.array(df_cm_data_min15['rounded_J'].to_list())
    V_arr = np.array(df_cm_data_min15['V cor'].to_list())

    return pd.DataFrame(data=({'AoA': AoA_arr.round(), 'AoA cor': AoA_arr, 'V cor': V_arr, 'rounded_J': J_arr, 'dCm_dDelta_e': dCM_ddelta_e_arr}))


def get_clcd_for_trim(data, tunnel_speed, propeller_speed, aoa_combis):
    data_sliced_VJ = get_function_set(data, {'V cor': tunnel_speed}, {'rounded_J': propeller_speed})

    # A list of CL vs delta_e function for each AoA: -5, 7, 12, 14 for 1 V-J combi (lists containing 4 functions)
    CL_vs_delta_e_functions = get_function_from_dataframe(data_sliced_VJ, 1, 'delta_e', 'CL_total cor', aoa_combis, np.linspace(-20, 20, 200), None, None)
    CD_vs_delta_e_functions = get_function_from_dataframe(data_sliced_VJ, 1, 'delta_e', 'CD cor', aoa_combis, np.linspace(-20, 20, 200), None, None)

    # A list of CM vs delta_e functions for each AoA: -5, 7, 12, 14 for 1 V-J combi
    function_lst = trim_points_all_aoa(data_sliced_VJ, [[{'V cor': tunnel_speed}, {'rounded_J': propeller_speed}]])

    # Find the CL, CD trim for each AoA: -5, 7, 12, 14
    AoA_trim_lst = []
    delta_e_trim_lst = []
    CL_trim_lst = []
    CD_trim_lst = []
    CLCD_trim_lst = []
    for i, function in enumerate(function_lst):
        delta_e_trim = function[0].trim_point

        CL_delta_e_function = CL_vs_delta_e_functions[i]
        CL_trim_AoA = CL_delta_e_function.poly_coeff(delta_e_trim)

        CD_delta_e_function = CD_vs_delta_e_functions[i]
        CD_trim_AoA = CD_delta_e_function.poly_coeff(delta_e_trim)

        CLCD_trim_AoA = CL_trim_AoA / CD_trim_AoA

        AoA_trim_lst.append(function[0].trim_aoa)
        delta_e_trim_lst.append(function[0].trim_point)
        CL_trim_lst.append(CL_trim_AoA)
        CD_trim_lst.append(CD_trim_AoA)
        CLCD_trim_lst.append(CLCD_trim_AoA)

    df_aoa_cl_cd = pd.DataFrame(data=({'AoA': AoA_trim_lst, 'delta_e trim': delta_e_trim_lst, 'rounded_v': [tunnel_speed for i in range(len(AoA_trim_lst))], 'V cor': [tunnel_speed for i in range(len(AoA_trim_lst))], 'rounded_J': [propeller_speed for i in range(len(AoA_trim_lst))], 'CL_total trim': CL_trim_lst, 'CD trim': CD_trim_lst, 'Coeff LD trim': CLCD_trim_lst}))
    return df_aoa_cl_cd


def get_data_for_j(full_data, combi_lst, xname, yname, legendname):
    xy_datapoints = []
    labels_lst = []
    for c in combi_lst:
        relevant_data = get_function_set(full_data, c[0], c[1])
        xpoints = relevant_data[xname].tolist()
        ypoints = relevant_data[yname].tolist()

        if 'AoA' in legendname:
            AoA_rounded = round(np.mean(relevant_data['AoA']))
            label = f'$\\alpha$ = {AoA_rounded} deg'
        elif 'delta' in legendname:
            delta_e_rounded = round(np.mean(relevant_data['delta_e']))
            label = f'$\\delta_e$ = {delta_e_rounded} deg'

        xy_datapoints.append(xpoints)
        xy_datapoints.append(ypoints)
        labels_lst.append(label)

    return xy_datapoints, labels_lst


tunnel_prop_combi = [[{'V cor': 40}, {'rounded_J': 1.6}],
                     [{'V cor': 40}, {'rounded_J': 1.8}],
                     [{'V cor': 40}, {'rounded_J': 3.5}]]

tunnel40_prop_combi = [[{'V cor': 40}, {'rounded_J': 1.6}],
                       [{'V cor': 40}, {'rounded_J': 1.8}],
                       [{'V cor': 40}, {'rounded_J': 3.5}]]

used_aoa = [[{'AoA cor': -5}, None],
            [{'AoA cor': 7}, None],
            [{'AoA cor': 12}, None],
            [{'AoA cor': 14}, None]]

used_aoa_V = [[{'V cor': 40}, {'AoA': 7}],
              [{'V cor': 40}, {'AoA': 12}],
              [{'V cor': 40}, {'AoA': 14}]]

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

    # Get the CL and CD for the trimmed condition for each combination of V and J
    trim_VJs_lst = []
    for combi in tunnel_prop_combi:
        tunnel_speed_val = combi[0]['V cor']
        propeller_speed_val = combi[1]['rounded_J']

        df_trim_VJ = get_clcd_for_trim(CM_cg_cor, tunnel_speed_val, propeller_speed_val, used_aoa)
        trim_VJs_lst.append(df_trim_VJ)

    df_trim_CL_CD = pd.concat(trim_VJs_lst, axis=0)

    latex_data = df_trim_CL_CD[['AoA', 'rounded_J', 'delta_e trim', 'CL_total trim', 'CD trim', 'Coeff LD trim']].round(2)
    latex_table = latex_data.to_latex(index=False, float_format="%.2f")
    with open(f'../Figures/aer-perf-table.tex', 'w') as f:
        f.write(latex_table)

    # 1. Plot CL trim vs AoA
    # get_function_from_dataframe(df_trim_CL_CD, 2, 'AoA', 'CL_total trim', tunnel_prop_combi, np.linspace(-6, 15, 100), 'AoA', 'CL')

    # 2. Plot CD trim vs CL trim
    # get_function_from_dataframe(df_trim_CL_CD, 8, 'CL_total trim', 'CD trim', tunnel40_prop_combi, np.linspace(-1, 2, 100), 'AoA', 'CD')

    # 3. Plot CL/CD trim vs J
    # CLCD_datapoints, CLCD_labels_lst = get_data_for_j(df_trim_CL_CD, used_aoa_V, 'rounded_J', 'Coeff LD trim', 'AoA')
    # PlotData('rounded_J', 'Coeff LD trim', np.linspace(0, 4.5, 100), CLCD_datapoints, 'curvefit', CLCD_labels_lst)

    # 4. Plot CM vs delta_e for AoA = 7
    # df_CM_AoA7 = get_function_set(CM_cg_cor, {'AoA cor': 7}, None)
    # get_function_from_dataframe(df_CM_AoA7, 1, 'delta_e', 'CM_total', tunnel40_prop_combi, np.linspace(-16, 20, 100), 'deltae', 'CM')

    # 5. Plot dCM/dDelta_e vs J
    df_dCM_ddelta_e = get_slope_cm_delta(CM_cg_cor_min15, CM_cg_cor_0_sliced, CM_cg_cor_15)
    # dCMdDelta_e_data_lst, dCMdDelta_e_label_lst = get_data_for_j(df_dCM_ddelta_e, used_aoa_V, 'rounded_J', 'dCm_dDelta_e', 'AoA')
    # PlotData('rounded_J', 'dCm_dDelta_e', np.linspace(1.5, 4, 100), dCMdDelta_e_data_lst, 'curvefit', dCMdDelta_e_label_lst)

    latex_data = df_dCM_ddelta_e[['AoA', 'V cor', 'rounded_J', 'dCm_dDelta_e']].round(4)
    latex_table = latex_data.to_latex(index=False, float_format="%.4f")
    with open(f'../Figures/el-eff-table.tex', 'w') as f:
        f.write(latex_table)

    plt.show()
