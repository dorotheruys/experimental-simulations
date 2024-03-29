import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from General.Pathfinder import get_file_path


def df_velocity_filter_tailoff(V_target: int):
    # if V_target == 10:
    #     # Reset V_target to 20
    #     V_target = 20
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
    print(filtered_df)
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


def df_velocity_filter(df, V_target: int):
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


# def lift_interference_old(df_uncor, df_tailoff):
#     aoa_uncor = df_uncor["rounded_AoA"]
#
#     # Use the 'isin' function to filter rows in 'df_tailoff' where 'AoA' matches any value in 'aoa_series'
#     # Note: tailoff is already rounded
#     filtered = df_tailoff[df_tailoff['AoA'].isin(aoa_uncor)]
#
#     # Extract the 'CL' column and convert it to a numpy array
#     CLw = filtered["CL"].values
#     CLa = filtered["CLa"].values
#
#     delta = 0.106  # Boundary correction factor
#     S_over_c = 0.2172 / 0.165  # Of main wing
#     tau2 = 1  # (placeholder) # Depends on tail, gotta check
#
#     d_aoa_uw = delta * S_over_c * CLw
#     d_aoa_sc = tau2 * d_aoa_uw
#     d_Cd_w = delta * S_over_c * CLw ** 2
#     d_aoa = d_aoa_uw + d_aoa_sc
#     d_CM25c = 1 / 8 * d_aoa_sc * CLa
#
#     aoa_cor = aoa_uncor.values + d_aoa
#     CD_cor = df_uncor["CD"].values + d_Cd_w
#     CM25c_cor = df_uncor["CMpitch25c"].values + d_CM25c
#     return aoa_cor, CD_cor, CM25c_cor


def lift_interference(df):
    delta = 0.104  # Boundary correction factor
    # S_over_C = 0.2172 / 0.165  # Of main wing  # old
    # Sref = 0.0736284708406532
    # C_tunnel = 2.07
    S_over_C = 0.03556930958485662  # Based on stuff above
    tau2_wing = 0.1                 #l/B=0.045
    tau2_tail = 0.7                 #l/B=0.3

    df_tailon = generate_cl_alpha(df)
    #dCM_dalphatail = 5.73 * 3.22 * 0.165  # CLalpha of airfoil (found online) * arm

    df_correction_factors = pd.DataFrame(columns=['dAoA', 'dCD', 'dCM25c'])
    for index, row in df.iterrows():
        V = row["rounded_v"]
        J = row['rounded_J']
        aoa_uncor = row["rounded_AoA"]

        df_tailoff = df_velocity_filter_tailoff(V)
        df_tailoff = df_tailoff[df_tailoff["AoA"] == aoa_uncor]

        CLw = df_tailoff["CL"].values[0]
        CLa = df_tailoff["CLa"].values[0]
        d_alpha_tail = delta * S_over_C * CLw * (1 + tau2_tail)

        df_tailon_filtered = df_tailon[(df_tailon['rounded_AoA'] == aoa_uncor) & (df_tailon['rounded_J']==J) & (df_tailon['rounded_v']== V)]   #

        CLa_tailon = df_tailon_filtered['CLa'].values

        CLa_tail = CLa_tailon-CLa           #Calculate effects of tail

        dCM_dalphatail = CLa_tail * 3.22 * 0.165    #Multiply CLa_tail with distance from htail to main wing for moment coefficient

        d_aoa_uw = delta * S_over_C * CLw
        d_aoa_sc = tau2_wing * d_aoa_uw
        d_aoa = d_aoa_uw + d_aoa_sc
        d_Cd_w = delta * S_over_C * CLw ** 2
        d_CM25c_uw = 1 / 8 * d_aoa_sc * CLa
        d_CM25c_t = dCM_dalphatail * d_alpha_tail
        d_CM25c = d_CM25c_uw + d_CM25c_t

        # Create a temporary DataFrame to hold the current row
        df_temp = pd.DataFrame([[d_aoa, d_Cd_w, d_CM25c]], columns=['dAoA', 'dCD', 'dCM25c'])

        # Drop empty or all-NA columns from df_temp
        df_correction_factors = df_correction_factors.dropna(axis=1, how='all')

        # Append the temporary DataFrame to the main DataFrame
        df_correction_factors = pd.concat([df_correction_factors, df_temp], ignore_index=True)

        # Add the lift interferences and create new columns
        df_correction_factors['AoA cor'] = df['rounded_AoA'] + df_correction_factors['dAoA']
        df_correction_factors['CD cor'] = df['CDbcor'] + df_correction_factors['dCD']
        df_correction_factors['CM cor'] = df['CMbcor'] + df_correction_factors['dCM25c']
    df_correction_factors = pd.concat([df, df_correction_factors], axis=1)
    return df_correction_factors

# def main_old():
#     plot_checks = False
#     V_target = 20
#     J_target = 1.6
#
#     filename = "bal_sorted2.csv"
#     folder = "Sort_data"
#
#     df = pd.read_csv(get_file_path(filename=filename, folder=folder))
#
#     df_to_process = df_velocity_filter(df, V_target)
#     df_to_process = df_to_process[df_to_process["rounded_J"] == J_target]
#     print(df_to_process)
#
#     df_tailoff = df_velocity_filter_tailoff(V_target)
#
#     aoa_new, CD_new, CM_new = lift_interference_old(df_to_process, df_tailoff)
#
#     aoa_old, CD_old, CM_old = df_to_process["AoA"], df_to_process["CD"], df_to_process["CMpitch25c"]
#
#     if plot_checks:
#         fig, ax = plt.subplots()
#         ax.scatter(aoa_old, CD_old, label='Old Data')
#         ax.scatter(aoa_new, CD_new, label='New Data')
#         ax.set_xlabel('AoA')
#         ax.set_ylabel('CD')
#         ax.legend()
#         ax.grid(True)
#         plt.show()
#
#         fig, ax = plt.subplots()
#         ax.scatter(aoa_old, df_to_process["CL"], label='Old Data')
#         ax.scatter(aoa_new, df_to_process["CL"], label='New Data')
#         ax.set_xlabel('AoA')
#         ax.set_ylabel('CL')
#         ax.legend()
#         ax.grid(True)
#         plt.show()
#
#         fig, ax = plt.subplots()
#         ax.scatter(aoa_old, CM_old, label='Old Data')
#         ax.scatter(aoa_new, CM_new, label='New Data')
#         ax.set_xlabel('AoA')
#         ax.set_ylabel('CM')
#         ax.legend()
#         ax.grid(True)
#         plt.show()

# def main():
#     filename = "bal_sorted2.csv"
#     folder = "Sort_data"
#
#     df = pd.read_csv(get_file_path(filename=filename, folder=folder))
#
#     print(df)
#
#
# if __name__ == "__main__":
#     main()
