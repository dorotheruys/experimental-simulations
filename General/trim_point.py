"""
Strategy:
1. Use CL and tunnel speed as input
2. Use the CL-alpha curve to get alpha at that point
3. Determine the lift due to the wing with the tail-off data & determine the lift due to the elevator by taking the
    difference between the tail-off data and the complete data.
4. Add a virtual centre of gravity by assuming W = L
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
from General.data_function_maker import get_function_from_dataframe, get_function_set, extract_from_list_classes
from Corrections.Lift_interference import df_velocity_filter_tailoff
from General.cm_cg_corrected import get_cm_cg_cor_all_elevator


def get_correct_data_based_on_elevator(elevator_defl: int, tunnel_prop_combi):
    if elevator_defl == -15:
        return get_function_from_dataframe(data_corrected_min15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    elif elevator_defl == 0:
        return get_function_from_dataframe(data_corrected_0, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    elif elevator_defl == 15:
        return get_function_from_dataframe(data_corrected_15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
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
    for j, CL in enumerate(function):
        if abs(CL - cl_des) < 0.001:
            intersections.append([AoA_range[j], CL])
        else:
            continue
    intersections_array = np.array(intersections)

    return intersections_array


def find_trim_points_per_aoa(aoa_data, aoa, order, combis):
    functionclass_CM_lst = get_function_from_dataframe(aoa_data, order, 'delta_e', 'CM_total', combis, np.linspace(-20, 20, 200), None, None)

    for CM_function in functionclass_CM_lst:
        roots_x = np.roots(CM_function.poly_coeff.coefficients)
        if len(roots_x) == 1:
            CM_function.trim_point = roots_x[0]
            CM_function.trim_aoa = aoa_data['AoA cor'].mean()
        else:
            print("Multiple roots. Adjust code.")
    return functionclass_CM_lst


def trim_points_all_aoa(CM_data, combis):
    """
    :param CM_data: data for all CMs
    :return: a list containing for 4 AoA each 5 functions for the 5 different combinations of V and J
    """
    CM_data_lst = []
    for aoa in [-5, 7, 12, 14]:
        # Find the trim point for 1 AoA
        CM_data_relevant = get_function_set(CM_data, {'AoA': aoa}, None)
        CM_function_AOA_lst = find_trim_points_per_aoa(CM_data_relevant, aoa, 1, combis)

        CM_data_lst.append(CM_function_AOA_lst)

    return CM_data_lst


def plot_trim_vs_aoa(CM_data_function_lst):
    x_lst = []
    y_lst = []
    V_r_lst = []
    V_lst = []
    J_lst = []
    combi_lst = []
    for functionlst in CM_data_function_lst:
        for function in functionlst:
            x_lst.append(function.trim_aoa)
            y_lst.append(function.trim_point)
            V_r_lst.append(5 * round(function.tunnel_speed / 5))        # round on integers of 5
            V_lst.append(function.tunnel_speed)
            J_lst.append(function.propeller_speed)
            combi_lst.append([{'V cor': function.tunnel_speed}, {'rounded_J': function.propeller_speed}])

    data = [{'AoA': x, 'delta_e trim': y, 'rounded_v': v_r, 'V cor': v, 'rounded_J': j} for x, y, v_r, v, j in zip(x_lst, y_lst, V_r_lst, V_lst, J_lst)]
    df_trim_vs_aoa = pd.DataFrame(data=data)
    get_function_from_dataframe(df_trim_vs_aoa, 2, 'AoA', 'delta_e trim', prop_tunnel_combis, np.linspace(-6, 15, 100), f'$\\alpha$ [deg]', f'$\\delta_e$ trim')
    return


# Initialize
prop_tunnel_combis = [[{'V cor': 40}, {'rounded_J': 1.6}],
                     [{'V cor': 40}, {'rounded_J': 1.8}],
                     [{'V cor': 40}, {'rounded_J': 3.5}]]

# chord-wise location assumptions
MAC_w = 0.165       # [m]
MAC_HT = 0.149      # [m]
l_ac_w = (0.33 - 0.25) * MAC_w
l_ac_ac = 3.22
l_cg = (0.5 - 0.25)

# Get the data
data_corrected_min15 = pd.read_csv('../Sort_data/cor_data_min15_V2.csv')
data_corrected_0 = pd.read_csv('../Sort_data/cor_data_0_V2.csv')
data_corrected_15 = pd.read_csv('../Sort_data/cor_data_15_V2.csv')


if __name__ == "__main__":
    ### Other approach stuff
    # # Plot CM vs delta_e per AoA
    # df_data_complete = pd.concat([data_corrected_min15, data_corrected_0, data_corrected_15], axis=0)
    #
    # for one_aoa in [7]:
    #     # plt.title(f'$\\alpha$ = {aoa} deg')
    #     data_relevant = get_function_set(df_data_complete, {'AoA': one_aoa}, None)
    #     get_function_from_dataframe(data_relevant, 1, 'delta_e', 'CM cor', prop_tunnel_combis, np.linspace(-20, 20, 100), 'deltae', 'CM')
    #
    # get_function_from_dataframe(data_corrected_0, 2, 'AoA cor', 'CM cor', prop_tunnel_combis, np.linspace(-10, 20, 100), 'AoA', 'CM')

    # # Get the tail-off data
    data_tailoff_40 = df_velocity_filter_tailoff(40)
    data_tailoff_20 = df_velocity_filter_tailoff(20)
    tail_off_data = [data_tailoff_20, data_tailoff_20, data_tailoff_40]

    # Determine the corrected CM for all tunnel velocities
    CM_cg_cor = get_cm_cg_cor_all_elevator(tail_off_data, [data_corrected_min15, data_corrected_0, data_corrected_15], l_ac_ac, l_cg)

    # Find the trim points
    CM_function_lst = trim_points_all_aoa(CM_cg_cor, prop_tunnel_combis)

    # Plot
    plot_trim_vs_aoa(CM_function_lst)
    # CM_cg_cor_function_lst = get_function_from_dataframe(CM_cg_cor_relevant, 1, 'delta_e', 'CM_total', prop_tunnel_combis, np.linspace(-20, 20, 50), f'$\\delta_e$ [deg]', f'$C_M$ [-]')

    plt.show()
