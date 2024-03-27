import pandas as pd
from General.Data_sorting import df
from General.data_function_maker import *
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 25})
pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

# Old stuff
# def Thrust_estimation1(J,V,AoA):
#     #windmilling = df['rounded_J'] == 17
#     tunnel_velocity = df['rounded_v'] == V
#     prop_setting = df['rounded_J'] == J
#     aoa_setting = df['rounded_AoA'] == AoA
#     #windmilling_df = df.loc[(windmilling) & (tunnel_velocity) & (aoa_setting)].copy()
#     #windmilling_drag = windmilling_df['CD'].iloc[0]
#     windmilling_df = Windmilling_dragcoefficients()
#     windmilling_df = windmilling_df[(windmilling_df['rounded_AoA'] == AoA)].copy()
#     windmilling_drag = windmilling_df['CD_windmilling'].iloc[0]
#     filtered_df = df.loc[(prop_setting) & (tunnel_velocity) & (aoa_setting)].copy()
#     tancoef = filtered_df['CD'].iloc[0]
#     return -(tancoef-windmilling_drag)/np.cos(AoA*np.pi/180)

def Windmilling_dragcoefficients(V):
    first_advance_ratio = df['rounded_J'] == 1.6
    upper_advance_ratio = df['rounded_J'] == 1.8
    V40_guess = 2.43                            #(2.359+2.5)/2
    V20_guess = 2.33                            #(2.359+2.5)/2-0.1
    V10_guess = 2.28                            #(2.359+2.5)/2-0.15
    lower_advance_ratio = df['rounded_J'] == 3.5
    tunnel_velocity = df['rounded_v'] == 40
    first_advance_regime = df.loc[(first_advance_ratio) & (tunnel_velocity)]
    upper_linear_regime = df.loc[(upper_advance_ratio) & (tunnel_velocity)]
    lower_linear_regime = df.loc[(lower_advance_ratio) & (tunnel_velocity)]
    first_resulting_CD = first_advance_regime['CD']
    upper_resulting_CD = upper_linear_regime['CD']
    lower_resulting_CD = lower_linear_regime['CD']
    if len(lower_resulting_CD) == 5:
        lower_resulting_CD = lower_resulting_CD.drop(lower_resulting_CD.index[1])  #Remove zero AoA
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
    aoa_lst = [-5, 7, 12, 14]
    if V!=40:

        lst_difference = []
        lst_CD = []
        i=0
        slow = df.loc[(df['rounded_J'] == 1.6) & (df['rounded_v'] == V)]
        slow_CD = slow['CD']
        for aoa in aoa_lst:
            baseline = first_resulting_CD.iloc[int(aoa+5)]
            if V==10:
                CD = slow_CD.iloc[int(i)]
                lst_difference.append(baseline - CD - slope_lst[i] * (V40_guess - V10_guess))   #Also account for different J for windmilling
                lst_CD.append(CD)
            elif V==20:
                CD = slow_CD.iloc[int(aoa+5)]
                lst_difference.append(baseline-CD-slope_lst[i]*(V40_guess-V20_guess))           #Also account for different J for windmilling
                lst_CD.append(CD)
            i += 1
        #plt.scatter(1.6, slow_CD.iloc[2])
        #plt.scatter(aoa_lst, lst_CD)
        windmilling_df['CD_windmilling'] = windmilling_df['CD_windmilling'] - lst_difference
    J = [1.6, 1.8, V40_guess, 3.5]
    CD_w = windmilling_df['CD_windmilling'].values
    if V==40:
        CD = [first_resulting_CD.iloc[17], upper_resulting_CD.iloc[1], CD_w[1], lower_resulting_CD.iloc[1]]
        #plt.scatter(aoa_lst,[first_resulting_CD.iloc[0],first_resulting_CD.iloc[12],first_resulting_CD.iloc[17],first_resulting_CD.iloc[19]])

    # CD_nowindmill = [first_resulting_CD.iloc[1], upper_resulting_CD.iloc[1], lower_resulting_CD.iloc[1]]
    # J = [1.6,1.8,3.5]
    # coefficients = np.polyfit(J, CD_nowindmill, deg=2)
    # fitted_curve = np.poly1d(coefficients)
    # J_array = np.arange(1.6,3.51,0.1)
    # plt.plot(J_array,fitted_curve(J_array))
    # plt.scatter(J, CD_nowindmill)
    # plt.show()
    return windmilling_df

# Vlst = [40,20,10]
# for V in Vlst:
#     windmill_df = Windmilling_dragcoefficients(V)
#     aoa = windmill_df['rounded_AoA'].values
#     CD_windmill = windmill_df['CD_windmilling'].values
#     plt.plot(aoa,CD_windmill)
# plt.show()

def drag_interpolation(V):
    windmilling_df = Windmilling_dragcoefficients(V)
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


def Thrust_estimation(J, V, AoA):
    # Old stuff
    # tunnel_velocity = df['rounded_v'] == V
    # prop_setting = df['rounded_J'] == J
    # aoa_setting = df['rounded_AoA'] == AoA
    # filtered_df = df.loc[(prop_setting) & (tunnel_velocity)].copy()
    # tancoef = filtered_df['CD'].values
    # short_aoa = filtered_df['rounded_AoA'].values

    # Find willing drag coefficients
    curve = drag_interpolation(V)
    windmilling_drag = curve(AoA)

    # Interpolate CD data for all angles of attack
    tunnel_prop_combi = [[{'rounded_v': V}, {'rounded_J': J}]]
    CD_alpha_function = get_function_from_dataframe(df, 10, 'AoA', 'CD', tunnel_prop_combi, np.linspace(-6, 20, 26),
                                                    None, None)
    CD_array = CD_alpha_function[0].poly_coeff(np.arange(-5, 14.1, 1))
    tancoef = CD_array[int(AoA + 5)]
    thrust_coefficient = -(tancoef - windmilling_drag) / np.cos(AoA * np.pi / 180)

    # Plotting stuff
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


# J = [1.6,1.8,3.5]
# CT = []
# coef_lst = []
# for j in J:
#     CT.append(Thrust_estimation(j,40,7)[0])
#     coef_lst.append(Thrust_estimation(j,40,7)[1])
# coefficients = np.polyfit(coef_lst, J, deg=2)
# fitted_curve = np.poly1d(coefficients)
# J_array = np.linspace(-0.0045,0.13,100)
# plt.plot(J_array,fitted_curve(J_array))
# plt.scatter(coef_lst, J)
# plt.xlabel('Advance ratio')
# plt.ylabel('Drag coefficient from BAL_forces.m')
# plt.show()