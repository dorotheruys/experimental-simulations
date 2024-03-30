"""
@author: dorotheruys
"""

import numpy as np
import pandas as pd
from General.data_function_maker import get_function_set


def get_decoupled_lift(df_data: pd.DataFrame, df_data_tailoff: pd.DataFrame, tunnel_speed: [int, float]):
    """
    A function that calculates the total lift, lift due to wing and lift due to horizontal tailplane
    :param df_data: Data from the windtunnel on one tunnel speed!
    :param df_data_tailoff: Data from the tail off experiment for the relevant tunnel speed only!
    :param tunnel_speed: tunnel speed
    :return: the input dataframe but with added columns of CL_wing and CL_tail
    """

    # Extract the lift coefficient from the tail-off data and interpolate
    df_wing = df_data_tailoff[['AoA', 'CL']]
    CL_wing_poly_coeff = np.poly1d(np.polyfit(df_wing['AoA'], df_wing['CL'], 2))

    # Construct a new dataframe including a tail-off lift coefficient for the AoA in the data and lift coefficient for the tail
    df_data['CL_wing'] = CL_wing_poly_coeff(df_data['AoA'])
    df_data['CL_tail'] = df_data['CL cor'] - df_data['CL_wing']

    df_data = df_data.rename(columns={'CL cor': 'CL_total cor'})
    return df_data


def get_cm_cg_corrected(df_data: pd.DataFrame, df_data_tailoff: list, arm_ac_wing: float, arm_ac_ht: float, arm_cg: float, mac_wing: float):
    """
    A function to get the pitch model coefficient for all tunnel velocity due to lift and virtually added weight
    :param df_data: Wind tunnel data
    :param df_data_tailoff: tail-off data for all tunnel speeds
    :param arm_ac_wing: chord-wise location aerodynamic centre main wing
    :param arm_ac_ht: chord-wise location aerodynamic centre horizontal tailplane
    :param arm_cg: chord-wise location centre of gravity
    :param mac_wing: reference model weight
    :return:
    """
    df_data_lst = []
    for i, tunnel_speed in enumerate([10., 20., 40.]):
        velocity_relevant_data = get_function_set(df_data, {'V': tunnel_speed}, None)
        df_data_decoupled_lift = get_decoupled_lift(velocity_relevant_data, df_data_tailoff[i], tunnel_speed)
        df_data_lst.append(df_data_decoupled_lift)
    df_data_complete = pd.concat(df_data_lst, axis=0)

    df_data_complete['CM_due_to_lift'] = -(arm_ac_wing / mac_wing) * df_data_complete['CL_wing'] - (arm_ac_ht / mac_wing) * df_data_complete['CL_tail']
    df_data_complete['CM_0.25c_total'] = df_data_complete['CM_due_to_lift'] + (arm_cg / mac_wing) * df_data_complete['CL_total cor']

    return df_data_complete.sort_index()


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
    CM_ref_15 = get_cm_cg_corrected(bal_data[2], tailoff_data, arm_ac_w, arm_ac_ht, arm_cg, ref_chord)
    CM_ref_min15 = get_cm_cg_corrected(bal_data[0], tailoff_data, arm_ac_w, arm_ac_ht, arm_cg, ref_chord)
    CM_ref_0 = get_cm_cg_corrected(bal_data[1], tailoff_data, arm_ac_w, arm_ac_ht, arm_cg, ref_chord)

    return pd.concat([CM_ref_min15, CM_ref_0, CM_ref_15], axis=0)
