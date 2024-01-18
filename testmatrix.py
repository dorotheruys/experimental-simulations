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


def get_testmatrix_with_time(df, total_time_start, first_setpoint_duration):
    # Calculate differences
    AoA_diff = df["AoA"].diff().abs()
    elevator_diff = df["Elevator"].diff().abs()
    velocity_diff = df["Tunnel velocity"].diff().abs()
    propset_diff = df["propeller setting"].diff().abs()

    # Initialize point_time with dt_sampling for all points
    point_time = pd.Series([first_setpoint_duration + dt_sampling] + [dt_sampling] * (len(df) - 1))

    # Add time for AoA_diff
    point_time[1:] += AoA_diff[1:] * dt_aoa_per_deg + dt_recalibrate

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


def randomize_testmatrix(df, AoA_and_propset=False, AoA_and_tunnelvelocity=False, all_variables=False):
    # Check that only one boolean parameter is True
    if sum([AoA_and_propset, AoA_and_tunnelvelocity, all_variables]) > 1:
        raise ValueError("Only one of AoA_and_propset, AoA_and_tunnelvelocity, and all_variables can be True.")

    elif AoA_and_propset:
        # Group the DataFrame by elevator and tunnel velocity  # Thus randomizing AoA and propeller setting
        grouped = df.groupby(["Elevator", "Tunnel velocity"])
    elif AoA_and_tunnelvelocity:
        # Group the DataFrame by elevator and propeller setting # Thus randomizing AoA and tunnel velocity
        grouped = df.groupby(["Elevator", "propeller setting"])
    elif all_variables:
        # Group the DataFrame by elevator only # Thus randomizing AoA, tunnel velocity and propeller setting
        grouped = df.groupby(["Elevator"])
    else:
        # Group the DataFrame by elevator, tunnel velocity and propeller setting #thus only randomizing AoA
        grouped = df.groupby(["Elevator", "Tunnel velocity", "propeller setting"])

    # Create a list to store the randomized smaller DataFrames
    randomized_dfs = []

    for i, (_, data) in enumerate(grouped):
        # Randomize the order of rows in the smaller DataFrame. Using i makes sure the seed is different
        randomized_data = data.sample(frac=1, random_state=i)
        # Add the randomized DataFrame to the list
        randomized_dfs.append(randomized_data)

    # Concatenate the randomized DataFrames back into a single DataFrame
    randomized_df = pd.concat(randomized_dfs)

    # Reset the index of the DataFrame
    randomized_df = randomized_df.reset_index(drop=False)
    return randomized_df

def propfreq_from_J_V(J, V):
    D = 0.2032  # [m]
    return V/(J*D)


# Define times for component changes in seconds
dt_aoa_per_deg = 2
dt_tunnel_startup = 3 * 60
dt_freestream_flow = 1 * 60
dt_sampling = 15
dt_elevator_adjust = 12.5 * 60
dt_propset = 30
dt_recalibrate = 15

time_before_start = 15 * 60

# Set ranges for variables
n_angles = [-5, 7, 12, 14]  # [deg]
n_elevator = [-15, 0 ,15]  # [deg]
n_windspeed = [10, 20, 40]  # [m/s]
n_prop = [0, 1, 2, 3]  # [rpm]

# # # Below is a smaller version to use when changing shit
# n_angles = [-5, 8, 14]  # [deg]
# n_elevator = [0,7,15]  # [deg]
# n_windspeed = [1,10]  # [m/s]
# n_prop = [20,1]  # [rpm]

use_randomized_testmatrix = True

if __name__ == "__main__":
    # Generate the points
    testmatrix_wind_on = get_test_matrix(n_elevator, n_windspeed, n_prop, n_angles)
    testmatrix_wind_off = get_test_matrix([0], [0], [0], n_angles)

    # Add randomization steps here: This allows us to check the effect of randomizing more stuff
    if use_randomized_testmatrix:
        testmatrix_wind_off_random = randomize_testmatrix(testmatrix_wind_off)  # not giving boolean options as they are not relevant

        # For the wind on stuff, options are available to add more randomization and to see how it impacts the matrix
        testmatrix_wind_on_random = randomize_testmatrix(testmatrix_wind_on, AoA_and_propset=False,
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
