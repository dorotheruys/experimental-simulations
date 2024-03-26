import pandas as pd
from General.Data_sorting import df
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

def Thrust_estimation1(J,V,AoA):
    #windmilling = df['rounded_J'] == 17
    tunnel_velocity = df['rounded_v'] == V
    prop_setting = df['rounded_J'] == J
    aoa_setting = df['rounded_AoA'] == AoA
    #windmilling_df = df.loc[(windmilling) & (tunnel_velocity) & (aoa_setting)].copy()
    #windmilling_drag = windmilling_df['CD'].iloc[0]
    windmilling_df = Windmilling_dragcoefficients()
    windmilling_df = windmilling_df[(windmilling_df['rounded_AoA'] == AoA)].copy()
    windmilling_drag = windmilling_df['CD_windmilling'].iloc[0]
    filtered_df = df.loc[(prop_setting) & (tunnel_velocity) & (aoa_setting)].copy()
    tancoef = filtered_df['CD'].iloc[0]
    return -(tancoef-windmilling_drag)/np.cos(AoA*np.pi/180)

 #Thrust_estimation1(3.5,40,7))
def Thrust_estimation2(J,V,AoA):
    tunnel_velocity = df['rounded_v'] == V
    prop_setting = df['rounded_J'] == J
    aoa_setting = df['rounded_AoA'] == AoA
    curve = drag_interpolation()
    windmilling_drag = curve(AoA)
    filtered_df = df.loc[(prop_setting) & (tunnel_velocity) & (aoa_setting)].copy()
    tancoef = filtered_df['CD'].iloc[0]
    return -(tancoef-windmilling_drag)/np.cos(AoA*np.pi/180)

def Windmilling_dragcoefficients():
    upper_advance_ratio = df['rounded_J'] == 1.8
    lower_advance_ratio = df['rounded_J'] == 3.5
    tunnel_velocity = df['rounded_v'] == 40
    upper_linear_regime = df.loc[(upper_advance_ratio) & (tunnel_velocity)]
    lower_linear_regime = df.loc[(lower_advance_ratio) & (tunnel_velocity)]
    upper_resulting_CD = upper_linear_regime['CD']
    lower_resulting_CD = lower_linear_regime['CD']
    lower_resulting_CD = lower_resulting_CD.drop(lower_resulting_CD.index[1])  #Remove zero AoA
    lst_CD_windmilling = []
    if len(upper_resulting_CD)!=len(lower_resulting_CD):
        print('Lengths are not the same')
    else:
        for i in range(0,len(upper_resulting_CD)):
            slope = (upper_resulting_CD.iloc[i]-lower_resulting_CD.iloc[i])/(1.8-3.5)
            CD_windmilling = upper_resulting_CD.iloc[i]+slope*(2.415-1.8)       #2.415 is the average windmilling advance ratio between experimental and relational
            lst_CD_windmilling.append(CD_windmilling)
    windmilling_df = pd.DataFrame({
        'rounded_AoA': upper_linear_regime['rounded_AoA'].reset_index(drop=True),
        'CD_windmilling': lst_CD_windmilling
    })
    return windmilling_df



def drag_interpolation():
    # windmilling = df['rounded_J'] == 17
    # tunnel_velocity = df['rounded_v'] == V
    # windmilling_df = df.loc[(windmilling) & (tunnel_velocity)].copy()
    # windmilling_drag = windmilling_df['CD'].values
    # windmilling_aoa = windmilling_df['rounded_AoA'].values
    windmilling_df = Windmilling_dragcoefficients()
    windmilling_drag = windmilling_df['CD_windmilling'].values
    windmilling_aoa = windmilling_df['rounded_AoA'].values
    coefficients = np.polyfit(windmilling_aoa, windmilling_drag, deg=4)
    fitted_curve = np.poly1d(coefficients)
    # aoa = df['rounded_AoA'].unique()
    # plt.scatter(windmilling_aoa, windmilling_drag)
    # plt.plot(aoa, fitted_curve(aoa), color='red', label='Fitted Curve')
    # plt.xlabel('AoA')
    # plt.ylabel('CD')
    # plt.show()
    return fitted_curve

#print(Thrust_estimation2(1.6,40,11))
#Append thrust coefficient to dataframe
# for index, row in df.iterrows():
#     rounded_J = row['rounded_J']
#     rounded_v = row['rounded_v']
#     rounded_AoA = row['rounded_AoA']
#
#     new_value = Thrust_estimation1(rounded_J, 40, rounded_AoA)
#     new_value = "{:.10f}".format(new_value)
#     df.at[index, 'Thrust coefficient'] = new_value
#
# print(df)
#
# # Specify the file path where you want to save the CSV file
# csv_file_path = 'Sort_data/bal_neg15_corrected.csv'
#
# # Use the to_csv() method to save the dataframe to a CSV file
# df.to_csv(csv_file_path, index=False)


#Old code
# aoa_lst = [-5,7,12,14]
#
# for aoa in aoa_lst:
#     print(Thrust_estimation1(1.6,40, aoa))
#     print(Thrust_estimation2(1.6, 40, aoa))