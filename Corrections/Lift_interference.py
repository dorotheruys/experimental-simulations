import pandas as pd

def import_tailoff():
    df = pd.read_excel("TailOffData.xlsx", sheet_name="AoS = 0 deg")
    df = df.drop("AoS", axis=1)
    return df

def df_velocity_filter(df, V_target: int):
    margin = 0.1  # [m/s]
    filtered_df = df[(df['Vinf'] >= V_target-margin) & (df['Vinf'] <= V_target+margin)]
    return filtered_df


df = import_tailoff()
print(df)
df_V20 = df_velocity_filter(df, 20)
print(df_V20)





