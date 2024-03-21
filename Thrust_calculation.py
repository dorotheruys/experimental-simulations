import pandas as pd
from Data_sorting import df
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

def Thrust_estimation1(J,V,AoA):
    windmilling = df['rounded_J'] == 17
    tunnel_velocity = df['rounded_v'] == V
    prop_setting = df['rounded_J'] == J
    aoa_setting = df['rounded_AoA'] == AoA
    windmilling_df = df.loc[(windmilling) & (tunnel_velocity) & (aoa_setting)].copy()
    windmilling_drag = windmilling_df['CD'].iloc[0]
    filtered_df = df.loc[(prop_setting) & (tunnel_velocity) & (aoa_setting)].copy()
    tancoef = filtered_df['CD'].iloc[0]
    return -(tancoef-windmilling_drag)/np.cos(AoA*np.pi/180)

def Thrust_estimation2(J,V,AoA):
    tunnel_velocity = df['rounded_v'] == V
    prop_setting = df['rounded_J'] == J
    aoa_setting = df['rounded_AoA'] == AoA
    curve = drag_interpolation(V)
    windmilling_drag = curve(AoA)
    filtered_df = df.loc[(prop_setting) & (tunnel_velocity) & (aoa_setting)].copy()
    tancoef = filtered_df['CD'].iloc[0]
    return -(tancoef-windmilling_drag)/np.cos(AoA*np.pi/180)

def drag_interpolation(V):
    windmilling = df['rounded_J'] == 17
    tunnel_velocity = df['rounded_v'] == V
    windmilling_df = df.loc[(windmilling) & (tunnel_velocity)].copy()
    windmilling_drag = windmilling_df['CD'].values
    windmilling_aoa = windmilling_df['rounded_AoA'].values
    coefficients = np.polyfit(windmilling_aoa, windmilling_drag, deg=4)
    fitted_curve = np.poly1d(coefficients)

    # print(fitted_curve)
    # plt.scatter(windmilling_aoa, windmilling_drag)
    # plt.plot(aoa, fitted_curve(aoa), color='red', label='Fitted Curve')
    # plt.xlabel('AoA')
    # plt.ylabel('CD')
    # plt.show()
    return fitted_curve

for index, row in df.iterrows():
    rounded_J = row['rounded_J']
    rounded_v = row['rounded_v']
    rounded_AoA = row['rounded_AoA']

    new_value = Thrust_estimation1(rounded_J, rounded_v, rounded_AoA)
    new_value = "{:.10f}".format(new_value)
    df.at[index, 'Thrust coefficient'] = new_value

print(df)

# Specify the file path where you want to save the CSV file
csv_file_path = 'Sort_data/bal_neg15_corrected.csv'

# Use the to_csv() method to save the dataframe to a CSV file
df.to_csv(csv_file_path, index=False)

# aoa_lst = [-5,7,12,14]
#
# for aoa in aoa_lst:
#     print(Thrust_estimation1(1.6,40, aoa))
#     print(Thrust_estimation2(1.6, 40, aoa))