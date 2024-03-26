"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_from_dataframe, get_function_set


def get_aoa_combis(aoa):
    combis = [[{'rounded_AoA': aoa}, {'rounded_v': 40}]]
        # ,
        #       [{'rounded_AoA': aoa}, {'rounded_v': 20}],
        #       [{'rounded_AoA': aoa}, {'rounded_v': 10}]]
    return combis


def get_cm_vs_elevator(cm_datapoints, plot):
    # Extract each CM from the data (and reset the indices of the zero angle)
    CM_min15 = pd.concat([cm_datapoints, pd.DataFrame({'delta_e': [-15]*len(cm_datapoints)}), bal_sorted_min15['CMpitch']], axis=1)
    CM_0 = pd.concat([bal_sorted_0[['AoA', 'rounded_AoA', 'V', 'rounded_v', 'J_M1', 'rounded_J']], pd.DataFrame({'delta_e': [0]*len(bal_sorted_0)}), bal_sorted_0['CMpitch'].reset_index(drop=True)], axis=1)
    CM_15 = pd.concat([cm_datapoints, pd.DataFrame({'delta_e': [15]*len(cm_datapoints)}), bal_sorted_15['CMpitch']], axis=1)

    # Make one large dataframe of all relevant data points to construct the graph
    CM_df = pd.concat([CM_min15, CM_0, CM_15], axis=0, ignore_index=True)

    # Get a dataframe for one specific AoA
    CM_df_AoA7 = get_function_set(CM_df, {'rounded_AoA': 7}, None)

    # Plot
    if plot is None:
        cm_deltae_plotting_lst = get_function_from_dataframe(CM_df_AoA7, 2, 'delta_e', 'CMpitch', tunnel_prop_combi, np.linspace(-20, 20, 50), None, None)
    else:
        cm_deltae_plotting_lst = get_function_from_dataframe(CM_df_AoA7, 2, 'delta_e', 'CMpitch', tunnel_prop_combi, np.linspace(-20, 20, 50), f'$\\delta_e$ [deg]', r'$C_M$ [-]')

    return cm_deltae_plotting_lst


def get_slope_cm_vs_aoa(cm_datapoints):
    # Make an array with all Cm coefficients and polyfit to line to return the slopes aka Cm delta
    CM_array = np.array([bal_sorted_min15['CMpitch'], bal_sorted_0_sliced['CMpitch'], bal_sorted_15['CMpitch']])
    delta_e_array = [-15, 0, 15]    # deg
    coeff_CM = np.polyfit(np.transpose(delta_e_array), CM_array, 1)

    # Make a dataframe consisting the slopes, AoA, V and K
    cm_slope = pd.DataFrame(data=({'CM_de': coeff_CM[0]}))

    dcm_dataframe = pd.concat([cm_datapoints, cm_slope], axis=1)

    # Get plot for AoA versus dCM/d delta_e, for each V & J combination
    dcm_ddeltae_plotting_lst = get_function_from_dataframe(dcm_dataframe, 2, 'AoA', 'CM_de', tunnel_prop_combi, np.linspace(-6, 20, 26), f'$\\alpha$ [deg]', r'$\frac{\partial C_M}{\partial \delta_e}$ [-]')

    return dcm_ddeltae_plotting_lst


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

# Get the datapoints at which the CM were made
cm_data_points = bal_sorted_15.loc[:, ['AoA', 'rounded_AoA', 'V', 'rounded_v', 'J_M1', 'rounded_J']]

if __name__ == "__main__":
    # 1. Get CM vs delta_e curve
    get_cm_vs_elevator(cm_data_points, True)

    # 2. Get dCM/d delta_e vs AoA curve
    # get_slope_cm_vs_aoa(cm_data_points)

    # Get plot for AoA vs CL, for each V & J combination
    get_function_from_dataframe(bal_sorted_15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), f'$\\alpha$ [deg]', f'$C_L$ [-]')

    # Get plot for CD vs CL, for each V & J combination
    # get_function_from_dataframe(bal_sorted_15, 2, 'CL', 'CD', tunnel_prop_combi, np.linspace(-1, 1.7, 26), f'$C_L$ [-]', f'$C_D$ [-]')

    plt.show()
