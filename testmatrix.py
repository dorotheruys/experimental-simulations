import datetime
import itertools

import numpy as np
import pandas as pd


def get_test_matrix(n_elevator, n_windspeed, n_prop, n_angles):
    dummy = [n_elevator, n_windspeed, n_prop, n_angles]
    comb = list(itertools.product(*dummy))
    mat = np.zeros((len(comb), 4))
    for i in range(4):
        for j in range(len(comb)):
            mat[j, i] = comb[j][i]
    mat = pd.DataFrame(mat, columns=['Elevator', 'Tunnel velocity', 'propeller setting', 'AoA'])
    return mat


# calculates time for wind on
def wind_on(na, n_p, nv, n_e):
    a = len(na)
    b = len(n_p)
    c = len(nv)
    d = len(n_e)
    prop_onoff = 15 * 60
    c_ele = 15 * 60
    c_tunnel_v = 2 * 60
    c_alpha = 25
    t_samp = 7  # sampling time per point
    c_prop_set = 30
    set1 = a * c_alpha * b + b * c_prop_set
    set2 = set1 * c + c * c_tunnel_v
    set3 = set2 * d + d * c_ele
    sampling_time = a * b * c * d * t_samp
    return (set3 + sampling_time) / 60  # return time in minutes


def wind_off(na):
    a = len(na)
    prop_onoff = 15 * 60
    c_ele = 15 * 60
    c_tunnel_v = 2 * 60
    c_alpha = a * 2 + 20
    t_samp = 10
    prop_set = 30

    return (a * (c_alpha - 1) + prop_onoff) / 60  # return time in minutes


def get_testmatrix_with_time(df, total_time_start, first_setpoint_duration):
    # Calculate differences
    AoA_diff = df["AoA"].diff().abs()
    elevator_diff = df["Elevator"].diff().abs()
    velocity_diff = df["Tunnel velocity"].diff().abs()
    propset_diff = df["propeller setting"].diff().abs()

    # Initialize point_time with dt_sampling for all points
    point_time = pd.Series([first_setpoint_duration + dt_sampling] + [dt_sampling] * (len(df) - 1))

    # Add time for AoA_diff
    point_time[1:] += AoA_diff[1:] * dt_aoa_per_deg +15

    # Add time for velocity_diff and propset_diff only if the corresponding value in elevator_diff is zero
    point_time[1:] += ((velocity_diff[1:] != 0) & (elevator_diff[1:] == 0)) * dt_freestream_flow
    point_time[1:] += ((propset_diff[1:] != 0) & (elevator_diff[1:] == 0)) * dt_propset

    # Add time for elevator_diff
    point_time[1:] += (elevator_diff[1:] != 0) * (dt_elevator_adjust + dt_tunnel_startup)

    # Calculate total_time
    total_time = point_time.cumsum()
    total_time += total_time_start
    total_time_final = total_time.iloc[-1]

    def convert_to_hms(series):  # function to convert time from seconds to hr:min:sec
        return series.apply(lambda x: pd.to_timedelta(x, unit='s').components).apply(
            lambda x: '{:02}:{:02}:{:02}'.format(x.hours, x.minutes, x.seconds))

    df["setpoint time"] = convert_to_hms(point_time)
    df["total time"] = convert_to_hms(total_time)

    return df, total_time_final  # Returns dataframe and also final time (final time in seconds)


def randomize_AoA(df, AoA_and_propset=False, AoA_and_tunnelvelocity=False, all_variables=False):
    # Check that only one boolean parameter is True
    if sum([AoA_and_propset, AoA_and_tunnelvelocity, all_variables]) > 1:
        raise ValueError("Only one of AoA_and_propset, AoA_and_tunnelvelocity, and all_variables can be True.")

    elif AoA_and_propset:
        df = df.sort_values(['Elevator', 'Tunnel velocity', 'propeller setting']).groupby(
            ['Elevator', 'Tunnel velocity'], sort=False).apply(lambda x: x.sample(frac=1, random_state=1)).reset_index(
            drop=True)
    elif AoA_and_tunnelvelocity:
        df = df.sort_values(['Elevator', 'Tunnel velocity', 'propeller setting']).groupby(
            ['Elevator', 'propeller setting'], sort=False).apply(
            lambda x: x.sample(frac=1, random_state=2)).reset_index(drop=True)
    elif all_variables:
        df = df.sort_values(['Elevator', 'Tunnel velocity', 'propeller setting']).groupby(['Elevator'],
                                                                                          sort=False).apply(
            lambda x: x.sample(frac=1, random_state=3)).reset_index(drop=True)
    else:
        df = df.sort_values(['Elevator', 'Tunnel velocity', 'propeller setting']).groupby(
            ['Elevator', 'Tunnel velocity', 'propeller setting'], sort=False).apply(
            lambda x: x.sample(frac=1, random_state=4)).reset_index(drop=True)
    return df


# Define times for component changes in seconds
dt_aoa_per_deg = 2
dt_tunnel_startup = 3 * 60
dt_freestream_flow = 1 * 60
dt_sampling = 15
dt_elevator_adjust = 12.5 * 60
dt_propset = 30

time_before_start = 15 * 60

# Set ranges for variables
n_angles = [-5, 7, 12, 14]  # [deg]
n_elevator = [-15, 0,15]  # [deg]
n_windspeed = [20, 30, 40]  # [m/s]
n_prop = [0, 1, 2,3]  # [rpm]

# # Below is a smaller version to use when changing shit
# n_angles = [-5, 14]  # [deg]
# n_elevator = [0,15]  # [deg]
# n_windspeed = [40, 60]  # [m/s]
# n_prop = [2, 10]  # [rpm]

# 15+5 for tunnel prep, 10 for trimming  # Yeah so this is outdated BS ~ Koen

use_randomized_testmatrix = True

if __name__ == "__main__":
    # total_time = wind_on(n_angles, n_prop, n_windspeed, n_elevator) + wind_off(n_angles) + 15 + 5 + 10
    # print(f"total time estimat:= {datetime.timedelta(minutes=total_time)} using old method")
    # print()

    # Generate the points
    testmatrix_wind_on = get_test_matrix(n_elevator, n_windspeed, n_prop, n_angles)
    testmatrix_wind_off = get_test_matrix([0], [0], [0], n_angles)
    # print("Test matrices before time calc")
    # print(testmatrix_wind_on)

    # Add randomization steps here: This allows us to check the effect of randomizing more stuff
    if use_randomized_testmatrix:
        testmatrix_wind_off_random = randomize_AoA(
            testmatrix_wind_off)  # not giving boolean options as they are not relevant

        # For the wind on stuff, options are available to add more randomization and to see how it impacts the matrix
        testmatrix_wind_on_random = randomize_AoA(testmatrix_wind_on, AoA_and_propset=False,
                                                  AoA_and_tunnelvelocity=False, all_variables=False)
        testmatrix_wind_off_with_time, total_time_wind_off = get_testmatrix_with_time(testmatrix_wind_off_random,
                                                                                      time_before_start,
                                                                                      abs(n_angles[0]) * dt_aoa_per_deg)
        testmatrix_wind_on_with_time, total_time_wind_on = get_testmatrix_with_time(testmatrix_wind_on_random,
                                                                                    total_time_wind_off,
                                                                                    dt_tunnel_startup)
    else:
        testmatrix_wind_off_with_time, total_time_wind_off = get_testmatrix_with_time(testmatrix_wind_off,
                                                                                      time_before_start,
                                                                                      abs(n_angles[0]) * dt_aoa_per_deg)
        testmatrix_wind_on_with_time, total_time_wind_on = get_testmatrix_with_time(testmatrix_wind_on,
                                                                                    total_time_wind_off,
                                                                                    dt_tunnel_startup)

    print(f"Testmatrix for wind off measurements")
    print(testmatrix_wind_off_with_time)

    print(f"Testmatrix for wind on measurements")
    print(testmatrix_wind_on_with_time)
    print(f"Total expected time: {datetime.timedelta(seconds=int(total_time_wind_on))}")
