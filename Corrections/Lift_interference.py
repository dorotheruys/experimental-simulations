import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from General.Pathfinder import get_file_path


def df_velocity_filter_tailoff(V_target: int):
    if V_target == 10:
        print("Reset V_target to 20")
        V_target = 20
    tailoff_path = get_file_path("TailOffData.xlsx", 'Corrections')
    df = pd.read_excel(tailoff_path, sheet_name="AoS = 0 deg")
    df = df.drop("AoS", axis=1)
    margin = 0.5  # [m/s]
    filtered_df = df[(df['Vinf'] >= V_target - margin) & (df['Vinf'] <= V_target + margin)]
    filtered_df.loc[:, "AoA"] = filtered_df.loc[:, "AoA"].round()  # Round AoA
    filtered_df = filtered_df.reset_index(drop=True)
    if V_target == 40:
        filtered_df = average_40_tailoff(filtered_df)
    filtered_df = generate_cl_alpha(filtered_df)
    return filtered_df


def average_40_tailoff(df_original):
    # Get the first 11 rows and the last 11 rows
    first_half = df_original.iloc[:11]
    second_half = df_original.iloc[20:31]

    # Reset the index of the second half so it matches with the first half
    second_half.reset_index(drop=True, inplace=True)

    # Calculate the average
    average_df = (first_half + second_half) / 2

    df_new = pd.concat([df_original.iloc[11:20], average_df], ignore_index=True, sort=False)
    df_return = df_new.sort_values(by=['AoA'], ascending=True)
    return df_return.reset_index(drop=True)


def generate_cl_alpha(df):
    df['CLa'] = df["CL"].diff() / df["AoA"].diff()
    df.loc[0, 'CLa'] = df['CLa'].iloc[1]  # Set value of first CLa to value of second CLa to prevent NaN
    df["CLa"] = df["CLa"] * 180 / np.pi  # Convert from deg^-1 to rad^-1 for CLa
    return df


def df_velocity_filter(file1, V_target: int):
    df = pd.read_csv(file1)

    # There were two similar rows with the same angle of attack in 0_corrected. Took the average of them
    double_aoa_rows = df[(df['rounded_AoA'] == 4) & (df['rounded_v'] == 20)]
    row_indices = double_aoa_rows.index
    average_values = (df.loc[row_indices[0]] + df.loc[row_indices[1]]) / 2
    df.loc[row_indices[0]] = average_values
    df.drop(row_indices[1], inplace=True)
    df.reset_index(drop=True, inplace=True)
    margin = 0.5  # [m/s]
    filtered_df = df[(df['V'] >= V_target - margin) & (df['V'] <= V_target + margin)]
    filtered_df = filtered_df.reset_index(drop=True)
    return filtered_df


def lift_interference(df_uncor, df_tailoff):
    aoa_uncor = df_uncor["rounded_AoA"]

    # Use the 'isin' function to filter rows in 'df_tailoff' where 'AoA' matches any value in 'aoa_series'
    # Note: tailoff is already rounded
    filtered = df_tailoff[df_tailoff['AoA'].isin(aoa_uncor)]

    # Extract the 'CL' column and convert it to a numpy array
    CLw = filtered["CL"].values
    CLa = filtered["CLa"].values

    delta = 0.106  # Boundary correction factor
    S_over_c = 0.2172 / 0.165  # Of main wing
    tau2 = 1  # (placeholder) # Depends on tail, gotta check

    d_aoa_uw = delta * S_over_c * CLw
    d_aoa_sc = tau2 * d_aoa_uw
    d_Cd_w = delta * S_over_c * CLw ** 2
    d_aoa = d_aoa_uw + d_aoa_sc
    d_CM25c = 1 / 8 * d_aoa_sc * CLa

    aoa_cor = aoa_uncor.values + d_aoa
    CD_cor = df_uncor["CD"].values + d_Cd_w
    CM25c_cor = df_uncor["CMpitch25c"].values + d_CM25c
    return aoa_cor, CD_cor, CM25c_cor


def main():
    V_target = 10
    J_target = 1.6

    file1 = get_file_path(filename="bal_sorted2.csv", folder="Sort_data")

    df_to_process = df_velocity_filter(file1, V_target)
    df_to_process = df_to_process[df_to_process["rounded_J"] == J_target]

    df_tailoff = df_velocity_filter_tailoff(V_target)

    aoa_new, CD_new, CM_new = lift_interference(df_to_process, df_tailoff)
    aoa_old, CD_old, CM_old = df_to_process["AoA"], df_to_process["CD"], df_to_process["CMpitch25c"]

    fig, ax = plt.subplots()
    ax.scatter(aoa_old, CD_old, label='Old Data')
    ax.scatter(aoa_new, CD_new, label='New Data')
    ax.set_xlabel('AoA')
    ax.set_ylabel('CD')
    ax.legend()
    ax.grid(True)
    plt.show()

    fig, ax = plt.subplots()
    ax.scatter(aoa_old, df_to_process["CL"], label='Old Data')
    ax.scatter(aoa_new, df_to_process["CL"], label='New Data')
    ax.set_xlabel('AoA')
    ax.set_ylabel('CL')
    ax.legend()
    ax.grid(True)
    plt.show()

    fig, ax = plt.subplots()
    ax.scatter(aoa_old, CM_old, label='Old Data')
    ax.scatter(aoa_new, CM_new, label='New Data')
    ax.set_xlabel('AoA')
    ax.set_ylabel('CM')
    ax.legend()
    ax.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
