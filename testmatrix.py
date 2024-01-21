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


def randomize_testmatrix(df, AoA_and_propset=False, AoA_and_tunnelvelocity=False, all_variables=False):
    # Check that only one boolean parameter is True
    if sum([AoA_and_propset, AoA_and_tunnelvelocity, all_variables]) > 1:
        raise ValueError("Only one of AoA_and_propset, AoA_and_tunnelvelocity, and all_variables can be True.")

    elif AoA_and_propset:
        # Group the DataFrame by elevator and tunnel velocity  # Thus randomizing AoA and propeller setting
        grouped = df.groupby(["Elevator", "Tunnel velocity"], dropna=False)
    elif AoA_and_tunnelvelocity:
        # Group the DataFrame by elevator and propeller setting # Thus randomizing AoA and tunnel velocity
        grouped = df.groupby(["Elevator", "propeller setting"], dropna=False)
    elif all_variables:
        # Group the DataFrame by elevator only # Thus randomizing AoA, tunnel velocity and propeller setting
        grouped = df.groupby(["Elevator"], dropna=False)
    else:
        # Group the DataFrame by elevator, tunnel velocity and propeller setting #thus only randomizing AoA
        grouped = df.groupby(["Elevator", "Tunnel velocity", "propeller setting"], dropna=False)

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
    randomized_df = randomized_df.reset_index(drop=True)
    return randomized_df


def get_testmatrix_with_time(df, total_time_start, first_setpoint_duration):
    # Calculate differences
    AoA_diff = df["AoA"].diff().abs()
    elevator_diff = df["Elevator"].diff().abs()
    velocity_diff = df["Tunnel velocity"].diff().abs()

    def custom_diff(series):
        diff = [0]  # Initialize the difference series
        for i in range(1, len(series)):
            if pd.isnull(series[i - 1]) and pd.isnull(series[i]):
                # If both values are NaN, the difference is 0
                diff.append(0)
            elif pd.isnull(series[i - 1]) or pd.isnull(series[i]):
                # If one of the values is NaN, the difference is nonzero (here we use np.nan to represent it)
                diff.append(np.nan)
            else:
                # If neither value is NaN, calculate the actual difference
                diff.append(abs(series[i] - series[i - 1]))
        return pd.Series(diff)

    # Use the custom function to calculate the difference
    propset_diff = custom_diff(df["propeller setting"])

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


def convert_testmatrix_J_to_Hz(df):
    # Check if inputs are valid
    if (df["propeller setting"] == 0).any():
        raise ValueError("Advance ratio cannot be 0")
    # Define a lambda function to convert J to Hz using the formula V / (J * 0.2032)
    propfreq_from_J_V = lambda J, V: V / (J * 0.2032)

    # Apply the lambda function to the 'propeller setting' and 'Tunnel velocity' columns of the DataFrame
    df["propeller setting"] = df.apply(lambda row: propfreq_from_J_V(row["propeller setting"], row["Tunnel velocity"]),
                                       axis=1)

    return df


def export_excel(df):
    # Please don't touch this function. Git and Excel are a bit of an unpleasant combination and this function is here to make sure you really need to make that excel sheet, and can't just accidentally make it
    print()
    print("Are you 100% certain you want to actually generate a new Excel sheet?")
    response = input("Type \'yes\' if you want to proceed")
    if response == "yes":
        print("Don't forget to deal correctly with this excel sheet in context of GitHub")
        print("As in, don't add it to GitHub unless you have a very good reason")
        response_2 = input("Do you understand that message?")
        if response_2 == "yes":
            print("Okay, your call ¯\_(ツ)_/¯")
            df.to_excel("Testmatrix.xlsx", index=False)
            print("Excel sheet generated")
        else:
            print("You chose wisely")
            print("No Excel sheet generated")
    else:
        print("You chose wisely")
        print("No Excel sheet generated")
    print(
        "One final note: If the Excel sheet is added to github, pleas always change the name after making changes, otherwise we'll override once we rerun this program.")


# Define times for component changes in seconds
dt_aoa_per_deg = 2
dt_tunnel_startup = 3 * 60
dt_freestream_flow = 1 * 60
dt_sampling = 15
dt_elevator_adjust = 12.5 * 60
dt_propset = 30
dt_recalibrate = 15

time_before_start = 15 * 60

time_between_wind_off_and_on = 3 * 60  # feels like we should have some time before we get going, just for contingency

# Set ranges for variables
AoA_values = [-5, 7, 12, 14]  # [deg]
Elevator_values = [-15, 0, 15]  # [deg]
Tunnel_velocity_values = [10, 20, 40]  # [m/s]
prop_J_values = [1.25, 1.9, np.nan, 3]  # [rpm]

# # # Below is a smaller version to use when changing shit
# AoA_values = [10, 0]  # [deg]
# Elevator_values = [10]  # [deg]
# Tunnel_velocity_values = [40]  # [m/s]
# prop_J_values = [1.25, 2.25, np.nan, 4]  # [rpm]

use_randomized_testmatrix = True
generate_excel_sheet = True  # No need to make this true unless you have a good reason

if __name__ == "__main__":
    # Generate the points
    testmatrix_wind_on = get_test_matrix(Elevator_values, Tunnel_velocity_values, prop_J_values, AoA_values)
    testmatrix_wind_off = get_test_matrix([0], [0], [0], AoA_values)

    # Add randomization steps here: This allows us to check the effect of randomizing more stuff
    if use_randomized_testmatrix:
        testmatrix_wind_off = randomize_testmatrix(
            testmatrix_wind_off)  # not giving boolean options as they are not relevant

        # For the wind on stuff, options are available to add more randomization and to see how it impacts the matrix
        testmatrix_wind_on = randomize_testmatrix(testmatrix_wind_on, AoA_and_propset=False,
                                                         AoA_and_tunnelvelocity=False, all_variables=False)


    # Add time
    testmatrix_wind_off_with_time, total_time_wind_off = get_testmatrix_with_time(testmatrix_wind_off,
                                                                                  time_before_start,
                                                                                  abs(AoA_values[
                                                                                          0]) * dt_aoa_per_deg)
    testmatrix_wind_on_with_time, total_time_wind_on = get_testmatrix_with_time(testmatrix_wind_on,
                                                                                total_time_wind_off + time_between_wind_off_and_on,
                                                                                dt_tunnel_startup)

    # Change propeller setting from Advance ratio to Hz:
    testmatrix_wind_on_with_time = convert_testmatrix_J_to_Hz(testmatrix_wind_on_with_time)

    print(f"Testmatrix for wind off measurements")
    print(testmatrix_wind_off_with_time)
    print(f"Testmatrix for wind on measurements")
    print(testmatrix_wind_on_with_time)
    print(f"Total expected time: {datetime.timedelta(seconds=int(total_time_wind_on))}")

    if generate_excel_sheet:
        combined_matrices = pd.concat([testmatrix_wind_off_with_time, testmatrix_wind_on_with_time], ignore_index=True)
        export_excel(combined_matrices)
