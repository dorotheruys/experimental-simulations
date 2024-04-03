import pandas as pd
from General.Data_sorting import specific_old_file, specific_cor_file
from General.data_function_maker import *
from Corrections.Support_tare_correction import *
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 25})
pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

def Windmilling_dragcoefficients(V, df):
    #Define set advance ratio's and velocity
    first_advance_ratio = df['rounded_J'] == 1.6
    upper_advance_ratio = df['rounded_J'] == 1.8
    V40_guess = 2.43                            #(2.359+2.5)/2
    V20_guess = 2.33                            #(2.359+2.5)/2-0.1
    V10_guess = 2.28                            #(2.359+2.5)/2-0.15
    lower_advance_ratio = df['rounded_J'] == 3.5
    tunnel_velocity = df['rounded_v'] == 40
    aoa_lst = [-5, 7, 12, 14]
    General_AoA_values = df['rounded_AoA'].isin(aoa_lst)

    #Find CX for all advance ratio's and V=40 m/s
    #Only interested in angles of attack -5, 7, 12, 14
    first_advance_regime = df.loc[(first_advance_ratio) & (tunnel_velocity) & (General_AoA_values)]
    upper_linear_regime = df.loc[(upper_advance_ratio) & (tunnel_velocity) & (General_AoA_values)]
    lower_linear_regime = df.loc[(lower_advance_ratio) & (tunnel_velocity) & (General_AoA_values)]
    first_resulting_CD = first_advance_regime['CD_strut_cor']
    upper_resulting_CD = upper_linear_regime['CD_strut_cor']
    lower_resulting_CD = lower_linear_regime['CD_strut_cor']

    #Find slope and windmilling drag between J=1.8 and J=3.5 for V=40
    lst_CD_windmilling = []
    if len(upper_resulting_CD)!=len(lower_resulting_CD):
        print('Lengths are not the same')
    else:
        slope_lst = []
        for i in range(0,len(upper_resulting_CD)):
            slope = (upper_resulting_CD.iloc[i]-lower_resulting_CD.iloc[i])/(1.8-3.5)
            slope_lst.append(slope)
            CD_windmilling = upper_resulting_CD.iloc[i]+slope*(V40_guess-1.8)       #2.415 is the average windmilling advance ratio between experimental and relational
            lst_CD_windmilling.append(CD_windmilling)
    windmilling_df = pd.DataFrame({
        'rounded_AoA': upper_linear_regime['rounded_AoA'].reset_index(drop=True),
        'CD_windmilling': lst_CD_windmilling
    })

    #Find windmilling drag for other velocities than 40 m/s
    if V!=40:
        lst_difference = []
        lst_CD = []
        # Only points available are at J=1.6
        slow = df.loc[(df['rounded_J'] == 1.6) & (df['rounded_v'] == V) & (General_AoA_values)]
        slow_CD = slow['CD_strut_cor']
        for i in range(len(aoa_lst)):
            #Baseline from 40 m/s at J=1.6
            baseline = first_resulting_CD.iloc[i]
            #Value for slower velocity at J=1.6
            CD = slow_CD.iloc[int(i)]
            lst_CD.append(CD)
            #Calculate difference
            if V==10:
                lst_difference.append(baseline - CD - slope_lst[i] * (V40_guess - V10_guess))   #Also account for different J for windmilling
            elif V==20:
                lst_difference.append(baseline-CD-slope_lst[i]*(V40_guess-V20_guess))           #Also account for different J for windmilling
        #Apply difference
        windmilling_df['CD_windmilling'] = windmilling_df['CD_windmilling'] - lst_difference

    #Plotting may or may not work
    # J = [1.6, 1.8, V40_guess, 3.5]
    # CD_w = windmilling_df['CD_windmilling'].values
    # if V==40:
    #     CD = [first_resulting_CD.iloc[1], upper_resulting_CD.iloc[1], CD_w[1], lower_resulting_CD.iloc[1]]
    #     plt.scatter(aoa_lst,[first_resulting_CD.iloc[0],first_resulting_CD.iloc[1],first_resulting_CD.iloc[2],first_resulting_CD.iloc[3]])

    # CD_nowindmill = [first_resulting_CD.iloc[1], upper_resulting_CD.iloc[1], lower_resulting_CD.iloc[1]]
    # J = [1.6,1.8,3.5]
    # coefficients = np.polyfit(J, CD_nowindmill, deg=2)
    # fitted_curve = np.poly1d(coefficients)
    # J_array = np.arange(1.6,3.51,0.1)
    # plt.plot(J_array,fitted_curve(J_array))
    # plt.scatter(J, CD_nowindmill)
    # plt.show()
    return windmilling_df

def drag_interpolation(V, df):
    #Interpolate windmilling drag coefficient for all angles of attack
    windmilling_df = Windmilling_dragcoefficients(V, df)
    windmilling_drag = windmilling_df['CD_windmilling'].values
    windmilling_aoa = windmilling_df['rounded_AoA'].values
    coefficients = np.polyfit(windmilling_aoa, windmilling_drag, deg=4)
    fitted_curve = np.poly1d(coefficients)
    #Plotting
    # aoa = df['rounded_AoA'].unique()
    # plt.scatter(windmilling_aoa, windmilling_drag)
    # plt.plot(aoa, fitted_curve(aoa), color='red', label='Fitted Curve')
    # plt.xlabel('AoA')
    # plt.ylabel('CD')
    # plt.show()
    return fitted_curve

def Thrust_estimation(J, V, AoA, df, cor):
    if cor==False:
        # Find windmilling drag coefficients for uncorrected data
        curve = drag_interpolation(V, df)
        windmilling_drag = curve(AoA)
    elif cor==True:
        # Find windmilling drag coefficients for corrected data
        prop_setting = df['rounded_J'] == J
        tunnel_velocity = df['rounded_v'] == V
        aoa = df['rounded_AoA'] == AoA
        windmilling_df = df.loc[(prop_setting) & (tunnel_velocity) & (aoa)]
        windmilling_drag = windmilling_df['CD cor'].values

    # Interpolate CX data for all angles of attack
    tunnel_prop_combis = [[{'rounded_v': V}, {'rounded_J': J}]]
    CX_alpha_function = get_function_from_dataframe(df, 10, 'AoA', 'CD_strut_cor', tunnel_prop_combis, np.linspace(-6, 20, 26),
                                                    None, None)
    CX_array = CX_alpha_function[0].poly_coeff(np.arange(-5, 14.1, 1))
    #Find tangential coefficient for desired angle of attack in range -5.......14
    tancoef = CX_array[int(AoA + 5)]
    #Calculate thrust coefficient
    thrust_coefficient = -(tancoef - windmilling_drag) / np.cos(AoA * np.pi / 180)

    # Plotting may or may not work
    # aoa = np.arange(-5,14.1,1)
    # plt.plot(aoa, curve(aoa), label='Windmill')
    # plt.scatter(short_aoa, tancoef)
    # plt.plot(aoa,CD_array, label='Not windmill')
    # plt.legend()
    # lst_coef = []
    # for angle in aoa:
    #     tancoef = CD_array[int(angle+5)]
    #     thrust_coefficient = -(tancoef-curve(angle))/np.cos(AoA*np.pi/180)
    #     lst_coef.append(tancoef)
    # plt.plot(aoa,lst_coef, label='thrust coefficient')
    return thrust_coefficient

#Function to calculate the corrected thrust coefficient
def CT_corrected(df):
    cor = True
    df_thrust_correction = pd.DataFrame(columns=['CT cor'])
    for index, row in df.iterrows():
        J = row['rounded_J']
        V = row["rounded_v"]
        AoA = row['rounded_AoA']

        CT = Thrust_estimation(J, V, AoA, df, cor)

        # Create a temporary DataFrame to hold the current row
        df_temp = pd.DataFrame([CT], columns=['CT cor'])

        # Drop empty or all-NA columns from df_temp
        df_thrust_correction = df_thrust_correction.dropna(axis=1, how='all')

        # Append the temporary DataFrame to the main DataFrame
        df_thrust_correction = pd.concat([df_thrust_correction, df_temp], ignore_index=True)
    df_thrust_correction = pd.concat([df, df_thrust_correction], axis=1)
    return df_thrust_correction

#Used to inspect certain data
def main():
    cor = False
    df = specific_cor_file()
    J_lst = [1.6, 1.8, 3.5]
    CT = []
    for J in J_lst:
        CT.append(Thrust_estimation(float(J),40,7, df, cor))
    CT = np.insert(CT, 2, 0)
    J_lst = [1.6, 1.8, 2.413, 3.5]
    plt.plot(J_lst, CT, label='V=40 m/s, AoA=7, de=0')
    plt.grid()
    plt.legend()
    plt.xlabel('J')
    plt.ylabel('Corrected CT')
    plt.show()

if __name__ == "__main__":
    main()

# J = [1.6,1.8,3.5]
# n = [123.02, 109.36, 56.24]
# CT = []
# coef_lst = []
# for j in J:
#     CT.append(Thrust_estimation(j,40,7))
# # coefficients = np.polyfit(coef_lst, J, deg=2)
# # fitted_curve = np.poly1d(coefficients)
# # J_array = np.linspace(-0.0045,0.13,100)
# plt.plot(J,CT)
# plt.xlabel('Advance ratio')
# plt.ylabel('Thrust coefficient')
# plt.show()