import pandas as pd
import matplotlib.pyplot as plt


def df_velocity_filter_tailoff(V_target: int):
    df = pd.read_excel("TailOffData.xlsx", sheet_name="AoS = 0 deg")
    df = df.drop("AoS", axis=1)
    margin = 0.5  # [m/s]
    filtered_df = df[(df['Vinf'] >= V_target - margin) & (df['Vinf'] <= V_target + margin)]
    filtered_df.loc[:,"AoA"] = filtered_df.loc[:,"AoA"].round()  # Round AoA
    filtered_df = filtered_df.reset_index(drop=True)
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


def df_velocity_filter(filename, V_target: int):
    df = pd.read_csv(file1)
    margin = 0.5  # [m/s]
    filtered_df = df[(df['V'] >= V_target - margin) & (df['V'] <= V_target + margin)]
    filtered_df = filtered_df.reset_index(drop=True)
    return filtered_df


def lift_interference(df_uncor, df_tailoff):
    aoa_uncor = df_uncor["rounded_AoA"]

    aoa_series = pd.Series(aoa_uncor)

    # Use the 'isin' function to filter rows in 'df_tailoff' where 'AoA' matches any value in 'aoa_series'
    filtered = df_tailoff[df_tailoff['AoA'].isin(aoa_series)]

    # Extract the 'CL' column and convert it to a numpy array
    CLw = filtered['CL'].values

    delta = 0.106  # Boundary correction factor
    S_over_c = 0.2172 / 0.165  # Of main wing
    tau2 = 1  # (placeholder) # Depends on tail, gotta check

    d_aoa_uw = delta * S_over_c * CLw
    d_aoa_sc = tau2 * d_aoa_uw
    d_Cd_w = delta * S_over_c * CLw ** 2
    d_aoa = d_aoa_uw + d_aoa_sc
    # add formula for d_Cw

    aoa_cor = aoa_uncor.values + d_aoa
    CD_cor = df_uncor["CD"].values + d_Cd_w
    return aoa_cor, CD_cor



if __name__ == "__main__":
    V_target = 40

    file1 = "../Sort_data/bal_sorted1.csv"

    df_to_process = df_velocity_filter(file1, V_target)
    df_to_process = df_to_process[df_to_process["rounded_J"] == 3.5]
    df_tailoff = average_40_tailoff(df_velocity_filter_tailoff(V_target))

    aoa_new, CD_new = lift_interference(df_to_process, df_tailoff)
    aoa_old, CD_old = df_to_process["AoA"], df_to_process["CD"]

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


