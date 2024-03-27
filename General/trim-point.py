"""
Strategy:
1. Use CL and tunnel speed as input
2. Use the CL-alpha curve to get alpha at that point
3. Determine the lift due to the wing with the tail-off data & determine the lift due to the elevator by taking the
    difference between the tail-off data and the complete data.
4. Add a virtual centre of gravity by scaling the weight of the ATR aircraft using the Froude number
5. This new CM should be the one that is trimmed and therefore the trimming point will be where this graph
    crosses x = 0.

Aerodynamic centre of the wing and elevator is assumed to be at 33% MAC.
Centre of gravity of entire aircraft (real-life, not model) is assumed to be slightly aft of the AC for
controllability and stability. Therefore, c_cg = 40% MAC

@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_from_dataframe, extract_from_list_classes, get_function_set
from Corrections.Lift_interference import df_velocity_filter_tailoff


def get_correct_data_based_on_elevator(elevator_defl: int, tunnel_prop_combi):
    if elevator_defl == -15:
        return get_function_from_dataframe(bal_sorted_min15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    elif elevator_defl == 0:
        return get_function_from_dataframe(bal_sorted_0, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    elif elevator_defl == 15:
        return get_function_from_dataframe(bal_sorted_15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    else:
        print("This elevator deflection is not in the database.")
        return


def get_aoa_from_cl(elevator_defl: int, cl_des: float, tunnel_speed: int, propeller_speed: float, tunnel_prop_combi):
    """
    A function that extracts the angle of attack for a given lift coefficients for a combination between
    tunnel speed, propeller speed and elevator deflection.
    :param elevator_defl: input elevator deflection in degrees (options: -15, 0, 15)
    :param cl_des:
    :param tunnel_speed:
    :param propeller_speed:
    :param tunnel_prop_combi:
    :return:
    """

    CL_alpha_function = get_correct_data_based_on_elevator(elevator_defl, tunnel_prop_combi)

    # Extract the poly coefficients from the relevant class and make a function
    poly1d_func = extract_from_list_classes(CL_alpha_function, tunnel_speed, propeller_speed)
    AoA_range = np.linspace(-6, 20, 200)
    function = poly1d_func(AoA_range)

    # Get the intersections between y = CL and the functions
    intersections = []
    for i, CL in enumerate(function):
        if abs(CL - cl_des) < 0.001:
            intersections.append([AoA_range[i], CL])
        else:
            continue
    intersections_array = np.array(intersections)

    return intersections_array


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
    merged_df = df_total_relevant_data
    merged_df['CL_wing'] = CL_wing_poly_coeff(merged_df['AoA'])
    merged_df['CL_tail'] = merged_df['CL'] - merged_df['CL_wing']

    # Make a pretty dataframe for output
    result_df = merged_df[['AoA', 'rounded_v', 'V', 'rounded_J', 'delta_e', 'CL', 'CL_wing', 'CL_tail']]
    result_df = result_df.rename(columns={'CL': 'CL_total'})
    return result_df


def get_cm_due_to_lift_virtual_weight(df_data: pd.DataFrame, df_data_tailoff: pd.DataFrame, tunnel_speed: int, l_ac_wing: float, l_ac_ht: float, l_cg: float, mac_wing: float):
    """
    A function to get the pitch model coefficient for a specific tunnel velocity due to lift and virtually added weight
    :param df_data: Wind tunnel data
    :param df_data_tailoff: tail-off data for a specific tunnel speed
    :param tunnel_speed:
    :param l_ac_wing: chord-wise location aerodynamic centre main wing
    :param l_ac_ht: chord-wise location aerodynamic centre horizontal tailplane
    :param l_cg: chord-wise location centre of gravity
    :param mac_wing: reference model weight
    :return: dataframe consisting of 'rounded_AoA', 'rounded_v', 'rounded_J', 'CL_total', 'CL_tailoff', 'CL_HT' and 'CM_vir'
    """
    df_data_result = get_decoupled_lift(df_data, df_data_tailoff, tunnel_speed)

    df_data_result['CM_due_to_lift'] = -(l_ac_wing / mac_wing) * df_data_result['CL_wing'] - (l_ac_ht / mac_wing) * df_data_result['CL_tail']
    df_data_result['CM_0.25c_total'] = df_data_result['CM_due_to_lift'] + (l_cg / mac_wing) * df_data_result['CL_total']

    # V_J_combis = [[{'rounded_v': tunnel_speed}, {'rounded_J': 1.6}],
    #               [{'rounded_v': tunnel_speed}, {'rounded_J': 1.8}],
    #               [{'rounded_v': tunnel_speed}, {'rounded_J': 3.5}]]
    #
    # get_function_from_dataframe(df_data_result, 2, 'AoA', 'CM_0.25c_total', V_J_combis, np.linspace(-6, 15, 50), f'$\\alpha$', f'$C_M$')

    return df_data_result


# if __name__ == "__main__":

# Get the data
bal_sorted_min15 = pd.read_csv('../Sort_data/bal_sorted1.csv')
bal_sorted_min15 = pd.concat([bal_sorted_min15, pd.DataFrame({'delta_e': [-15]*len(bal_sorted_min15)})], axis=1)

bal_sorted_0 = pd.read_csv('../Sort_data/bal_sorted2.csv')
bal_sorted_0 = pd.concat([bal_sorted_0, pd.DataFrame({'delta_e': [0]*len(bal_sorted_0)})], axis=1)

bal_sorted_15 = pd.read_csv('../Sort_data/bal_sorted3.csv')
bal_sorted_15 = pd.concat([bal_sorted_15, pd.DataFrame({'delta_e': [15]*len(bal_sorted_15)})], axis=1)

# Get the tail-off data
data_tailoff_40 = df_velocity_filter_tailoff(40)
rounded_AoA_40 = data_tailoff_40['AoA'].round()
data_tailoff_40.insert(1, 'rounded_AoA', rounded_AoA_40)

data_tailoff_20 = df_velocity_filter_tailoff(20)
rounded_AoA_20 = data_tailoff_20['AoA'].round()
data_tailoff_20.insert(1, 'rounded_AoA', rounded_AoA_20)

tunnel_prop_combi = [[{'rounded_v': 40}, {'rounded_J': 1.6}],
                     [{'rounded_v': 40}, {'rounded_J': 1.8}],
                     [{'rounded_v': 40}, {'rounded_J': 3.5}],
                     [{'rounded_v': 20}, {'rounded_J': 1.6}],
                     [{'rounded_v': 10}, {'rounded_J': 1.6}]]

# Calculate the reference model using the reference aircraft ATR-72
ref_tunnel_vel = 10.                        # [m/s]
MTOW_ref_ac = (22800. - 0.5 * 5000) * 9.80665              # [N]
cruice_vel_ref_ac = 510 * 10**3 / 3600      # [m/s]

# chord-wise location assumptions
MAC_w = 0.165       # [m]
MAC_HT = 0.149      # [m]
arm_ac_w = (0.33 - 0.25) * MAC_w
arm_ac_ht = 3.22 * MAC_w + (0.33 - 0.25) * MAC_HT
arm_cg = (0.35 - 0.25) * MAC_w

# Loop through the different tunnel velocities
tail_off_data = [data_tailoff_20, data_tailoff_20, data_tailoff_40]
CM_ref_lst = []
for i, V in enumerate([10, 20, 40]):
    relevant_tailoff_data = tail_off_data[i]
    CM_ref_15 = get_cm_due_to_lift_virtual_weight(bal_sorted_15, relevant_tailoff_data, V, arm_ac_w, arm_ac_ht, arm_cg, MAC_w)
    CM_ref_min15 = get_cm_due_to_lift_virtual_weight(bal_sorted_min15, relevant_tailoff_data, V, arm_ac_w, arm_ac_ht, arm_cg, MAC_w)
    CM_ref_0 = get_cm_due_to_lift_virtual_weight(bal_sorted_0, relevant_tailoff_data, V, arm_ac_w, arm_ac_ht, arm_cg, MAC_w)

    CM_ref_complete = pd.concat([CM_ref_min15, CM_ref_0, CM_ref_15], axis=0)
    CM_ref_lst.append(CM_ref_complete)

CM_ref_result = pd.concat(CM_ref_lst, axis=0)

# Get CM vs delta_e for AoA = 7
CM_ref_relevant = get_function_set(CM_ref_result, {'AoA': 7}, None)
get_function_from_dataframe(CM_ref_relevant, 1, 'delta_e', 'CM_0.25c_total', tunnel_prop_combi, np.linspace(-20, 20, 50), f'$\\delta_e$ [deg]', f'$C_M$ [-]')
plt.show()
