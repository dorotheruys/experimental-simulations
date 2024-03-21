import pandas as pd


def df_velocity_filter(V_target: int):
    df = pd.read_excel("TailOffData.xlsx", sheet_name="AoS = 0 deg")
    df = df.drop("AoS", axis=1)
    margin = 0.1  # [m/s]
    filtered_df = df[(df['Vinf'] >= V_target - margin) & (df['Vinf'] <= V_target + margin)]
    filtered_df = filtered_df.reset_index(drop=True)
    return filtered_df


def average_40(df_original):
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



