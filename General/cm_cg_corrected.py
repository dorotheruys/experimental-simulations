"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd
from General.data_function_maker import get_function_set


def get_decoupled_lift(df_data: pd.DataFrame, df_data_tailoff: pd.DataFrame, tunnel_speed: int):
    """
    A function that calculates the total lift, lift due to wing and lift due to horizontal tailplane
    :param df_data: Data from the windtunnel
    :param df_data_tailoff: Data from the tail off experiment
    :param tunnel_speed: tunnel speed
    :return: a dataframe containing: AoA, tunnel speed, propeller speed, total CL, tail-off CL and CL due to horizontal tailplane
    """
    # Get the relevant data based on the tunel speed
    df_total_relevant_data = get_function_set(df_data, {'rounded_v': tunnel_speed}, None)

    # Extract the lift coefficient from the tail-off data and interpolate
    df_wing = df_data_tailoff[['AoA', 'CL']]
    CL_wing_poly_coeff = np.poly1d(np.polyfit(df_wing['AoA'], df_wing['CL'], 2))

    # Construct a new dataframe including a tail-off lift coefficient for the AoA in the data and lift coefficient for the tail
    # merged_df = df_total_relevant_data
    df_total_relevant_data['CL_wing'] = CL_wing_poly_coeff(df_total_relevant_data['AoA'])
    df_total_relevant_data['CL_tail'] = df_total_relevant_data['CL'] - df_total_relevant_data['CL_wing']

    # Make a pretty dataframe for output
    # result_df = merged_df[['AoA', 'rounded_v', 'V', 'rounded_J', 'delta_e', 'CL', 'CL_wing', 'CL_tail']]
    df_total_relevant_data = df_total_relevant_data.rename(columns={'CL': 'CL_total'})
    return df_total_relevant_data


def get_cm_cg_corrected(df_data: pd.DataFrame, df_data_tailoff: pd.DataFrame, tunnel_speed: [int, float], arm_ac_wing: float, arm_ac_ht: float, arm_cg: float, mac_wing: float):
    """
    A function to get the pitch model coefficient for a specific tunnel velocity due to lift and virtually added weight
    :param df_data: Wind tunnel data
    :param df_data_tailoff: tail-off data for a specific tunnel speed
    :param tunnel_speed:
    :param arm_ac_wing: chord-wise location aerodynamic centre main wing
    :param arm_ac_ht: chord-wise location aerodynamic centre horizontal tailplane
    :param arm_cg: chord-wise location centre of gravity
    :param mac_wing: reference model weight
    :return: dataframe consisting of 'rounded_AoA', 'rounded_v', 'rounded_J', 'CL_total', 'CL_tailoff', 'CL_HT' and 'CM_vir'
    """
    df_data_result = get_decoupled_lift(df_data, df_data_tailoff, tunnel_speed)

    df_data_result['CM_due_to_lift'] = -(arm_ac_wing / mac_wing) * df_data_result['CL_wing'] - (arm_ac_ht / mac_wing) * df_data_result['CL_tail']
    df_data_result['CM_0.25c_total'] = df_data_result['CM_due_to_lift'] + (arm_cg / mac_wing) * df_data_result['CL_total']

    return df_data_result


def get_cm_cg_cor_all_elevator(tailoff_data: list, bal_data: list, arm_ac_w: float, arm_ac_ht: float, arm_cg: float, ref_chord: float):
    """
    A function to get the CM corrected for centre of gravity for all elevator deflections.
    :param tailoff_data: list of tail-off data for tunnel velocities 10, 20 and 40 m/s
    :param bal_data: list of balance data for different elevator deflections: -15, 0, 15 deg
    :param arm_ac_w: arm of the aerodynamic centre of the wing
    :param arm_ac_ht: arm of the aerodynamic centre of the horizontal tail
    :param arm_cg: arm of the centre of gravity
    :param ref_chord: reference chord length to non-dimensionalise the moment (eg: MAC of the wing)
    :return: a dataframe consisting of new columns CL_wing, CL_tail, CM due to lift, total CM (the cg corrected one)
    """
    CM_ref_lst = []
    for i, V in enumerate([10, 20, 40]):
        relevant_tailoff_data = tailoff_data[i]
        CM_ref_15 = get_cm_cg_corrected(bal_data[2], relevant_tailoff_data, V, arm_ac_w, arm_ac_ht, arm_cg, ref_chord)
        CM_ref_min15 = get_cm_cg_corrected(bal_data[0], relevant_tailoff_data, V, arm_ac_w, arm_ac_ht, arm_cg, ref_chord)
        CM_ref_0 = get_cm_cg_corrected(bal_data[1], relevant_tailoff_data, V, arm_ac_w, arm_ac_ht, arm_cg, ref_chord)

        CM_ref_complete = pd.concat([CM_ref_min15, CM_ref_0, CM_ref_15], axis=0)
        CM_ref_lst.append(CM_ref_complete)

    CM_ref_result = pd.concat(CM_ref_lst, axis=0)

    return CM_ref_result
