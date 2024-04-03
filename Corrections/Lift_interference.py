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
    filtered_df.rename(columns={'CM25c': 'CMpitch25c'}, inplace=True)
    filtered_df = generate_cm025_alpha(filtered_df)
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


def generate_cl_alpha_cor(df):
    df['CLa'] = df["CL cor"].diff() / df["AoA"].diff()
    df.loc[0, 'CLa'] = df['CLa'].iloc[1]  # Set value of first CLa to value of second CLa to prevent NaN
    df["CLa"] = df["CLa"] * 180 / np.pi  # Convert from deg^-1 to rad^-1 for CLa
    return df


def generate_cm025_alpha(df):
    df['CM25ca'] = df["CMpitch25c"].diff() / df["AoA"].diff()
    df.loc[0, 'CM25ca'] = df['CM25ca'].iloc[1]  # Set value of first CMa to value of second CLa to prevent NaN
    df["CM25ca"] = df["CM25ca"] * 180 / np.pi  # Convert from deg^-1 to rad^-1 for CMa
    return df


def generate_cm025_alpha_cor(df):
    df['CM25ca'] = df["CMbcor"].diff() / df["AoA"].diff()
    df.loc[0, 'CM25ca'] = df['CM25ca'].iloc[1]  # Set value of first CMa to value of second CLa to prevent NaN
    df["CM25ca"] = df["CM25ca"] * 180 / np.pi  # Convert from deg^-1 to rad^-1 for CMa
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


def lift_interference(df):
    delta = 0.104  # Boundary correction factor
    S_over_C = 0.05123562777917539
    tau2_wing = 0.15  # l/B=0.045
    tau2_tail = 0.75  # l/B=0.3

    df_tailon = generate_cl_alpha_cor(df)
    df_tailon_m = generate_cm025_alpha(df)

    df_correction_factors = pd.DataFrame(columns=['dAoA', 'dCD', 'dCM25c'])
    for index, row in df.iterrows():
        V = row["rounded_v"]
        J = row['rounded_J']
        aoa_uncor = row["rounded_AoA"]

        df_tailoff = df_velocity_filter_tailoff(V)
        df_tailoff = df_tailoff[df_tailoff["AoA"] == aoa_uncor]

        # Tail off data
        CLw = df_tailoff["CL"].values[0]
        CLa = df_tailoff["CLa"].values[0]
        CMa = df_tailoff["CM25ca"].values[0]
        d_alpha_tail = delta * S_over_C * CLw * (1 + tau2_tail)

        # Tail contributions
        df_tailon_m_filtered = df_tailon_m[(df_tailon['rounded_AoA'] == aoa_uncor) & (df_tailon_m['rounded_J'] == J) & (
                df_tailon_m['rounded_v'] == V)]  #
        CMa_tailon = df_tailon_m_filtered['CM25ca'].values[0]
        CLa_tailon = df_tailon_m_filtered['CLa'].values[0]

        # Isolate tail slope
        CMa_tail = CMa_tailon - CMa

        # AoA changes contribution (in radians)
        d_aoa_uw = delta * S_over_C * CLw
        d_aoa_sc = tau2_wing * d_aoa_uw
        d_aoa = d_aoa_uw + d_aoa_sc

        # Drag change
        d_Cd_w = delta * S_over_C * CLw ** 2

        # Moment change
        d_CM25c_uw = 1 / 8 * d_aoa_sc * CLa_tailon
        d_CM25c_t = CMa_tail * d_alpha_tail
        d_CM25c = d_CM25c_uw - d_CM25c_t

        # Create a temporary DataFrame to hold the current row
        df_temp = pd.DataFrame([[d_aoa, d_Cd_w, d_CM25c]], columns=['dAoA', 'dCD', 'dCM25c'])

        # Drop empty or all-NA columns from df_temp
        df_correction_factors = df_correction_factors.dropna(axis=1, how='all')

        # Append the temporary DataFrame to the main DataFrame
        df_correction_factors = pd.concat([df_correction_factors, df_temp], ignore_index=True)

        # Add the lift interferences and create new columns
        df_correction_factors['AoA cor'] = df['rounded_AoA'] + df_correction_factors['dAoA'] * 180 / np.pi
        df_correction_factors['CD cor'] = df['CDbcor'] + df_correction_factors['dCD']
        df_correction_factors['CM cor'] = df['CMbcor'] + df_correction_factors['dCM25c']

    df_correction_factors = pd.concat([df, df_correction_factors], axis=1)
    return df_correction_factors


