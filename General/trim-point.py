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
controllability and stability. Therefore, c_cg = 35% MAC

@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_from_dataframe, extract_from_list_classes
from General.elevator_effectiveness import get_cm_vs_elevator
from Corrections.Lift_interference import df_velocity_filter_tailoff


def get_aoa_from_cl(elevator_defl: int, cl_des: float, tunnel_speed: int, propeller_speed: float):
    """
    A function that extracts the angle of attack for a given lift coefficients for a combination between
    tunnel speed, propeller speed and elevator deflection.
    :param elevator_defl: input elevator deflection in degrees (options: -15, 0, 15)
    :param cl_des:
    :param tunnel_speed:
    :param propeller_speed:
    :return:
    """
    if elevator_defl == -15:
        CL_alpha_function = get_function_from_dataframe(bal_sorted_min15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    elif elevator_defl == 0:
        CL_alpha_function = get_function_from_dataframe(bal_sorted_0, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    elif elevator_defl == 15:
        CL_alpha_function = get_function_from_dataframe(bal_sorted_15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    else:
        print("This elevator deflection is not in the database.")
        return

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


def get_cm_due_to_lift(df_data, df_data_to):

    return


# Get the data
bal_sorted_min15 = pd.read_csv('../Sort_data/bal_sorted1.csv')
bal_sorted_0 = pd.read_csv('../Sort_data/bal_sorted2.csv')
bal_sorted_15 = pd.read_csv('../Sort_data/bal_sorted3.csv')

bal_sorted_min15_zero = pd.read_csv('../Sort_data/delta_neg15_zero.csv')
data_tailoff_40 = df_velocity_filter_tailoff(40)
# data_tailoff_20 = df_velocity_filter_tailoff(20)

cm_data_points = bal_sorted_15.loc[:, ['AoA', 'rounded_AoA', 'V', 'rounded_v', 'J_M1', 'rounded_J']]

# Slice the zero deflection array such that the new dataframe contains the same data points
rows = [0, 12, 17, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 42, 47, 49]
bal_sorted_0_sliced1 = bal_sorted_0.iloc[rows]
bal_sorted_0_sliced = pd.concat([bal_sorted_0_sliced1, bal_sorted_0[50:]])

tunnel_prop_combi = [[{'rounded_v': 40}, {'rounded_J': 1.6}],
                     [{'rounded_v': 40}, {'rounded_J': 1.8}],
                     [{'rounded_v': 40}, {'rounded_J': 3.5}],
                     [{'rounded_v': 20}, {'rounded_J': 1.6}],
                     [{'rounded_v': 10}, {'rounded_J': 1.6}],
                     [{'rounded_v': 40}, {'rounded_J': 17}],
                     [{'rounded_v': 20}, {'rounded_J': 17}],
                     [{'rounded_v': 10}, {'rounded_J': 17}]]

if __name__ == "__main__":
    get_aoa_from_cl(15, 1., 40, 1.6)
    # Generate the required curves
    # CL_alpha_function_min15 = get_function_from_dataframe(bal_sorted_min15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    # CL_alpha_function_0 = get_function_from_dataframe(bal_sorted_0_sliced, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)
    # CL_alpha_function_15 = get_function_from_dataframe(bal_sorted_15, 2, 'AoA', 'CL', tunnel_prop_combi, np.linspace(-6, 20, 26), None, None)

    # CM_alpha_function_min15 = get_function_from_dataframe(bal_sorted_min15, 2, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), None, None)
    # CM_alpha_function_0 = get_function_from_dataframe(bal_sorted_0_sliced, 2, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), None, None)
    # CM_alpha_function_15 = get_function_from_dataframe(bal_sorted_15, 2, 'AoA', 'CMpitch', tunnel_prop_combi, np.linspace(-6, 20, 50), None, None)
    #
    # CM_deltae_function = get_cm_vs_elevator(cm_data_points, None)

    plt.show()
