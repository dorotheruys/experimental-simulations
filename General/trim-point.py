"""
Strategy:
1. Use CL and tunnel speed as input
2. Use the CL-alpha curve to get alpha at that point
3. Use the CM-alpha curve to get CM at that point
4. Use the CM-delta_e curve to get delta_e at that point

Aerodynamic centre of the wing and elevator is assumed to be at 33% MAC
Centre of gravity of entire aircraft (real-life, not model) is assumed to be slightly aft of the AC for controllability and stability
Therefore, c_cg = 35% MAC

@author: dorotheruys
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from General.data_function_maker import get_function_from_dataframe, extract_from_list_classes
from General.elevator_effectiveness import get_cm_vs_elevator
from Corrections.Lift_interference import df_velocity_filter_tailoff

def get_aoa_from_cl(elevator_defl: int, CL_des: float, tunnel_speed: int, propeller_speed: float):
    """

    :param elevator_defl: input elevator deflection in degrees (options: -15, 0, 15)
    :param CL_des:
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
    coefficients = extract_from_list_classes(CL_alpha_function, tunnel_speed, propeller_speed).poly_coeff
    poly_func = np.poly1d(coefficients)

    # Get the intersections between y = CL and the functions
    intersections = poly_func - CL_des

    return


# Get the data
bal_sorted_min15 = pd.read_csv('../Sort_data/bal_sorted1.csv')
bal_sorted_0 = pd.read_csv('../Sort_data/bal_sorted2.csv')
bal_sorted_15 = pd.read_csv('../Sort_data/bal_sorted3.csv')

bal_sorted_min15_zero = pd.read_csv('../Sort_data/delta_neg15_zero.csv')
data_tailoff_40 = df_velocity_filter_tailoff(40)
data_tailoff_20 = df_velocity_filter_tailoff(20)

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
