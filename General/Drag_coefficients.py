import pandas as pd
from General.Data_sorting import *
import matplotlib.pyplot as plt
from General.Thrust_calculation import drag_interpolation

def drag_coefficients(J,V,CL_unc):
    prop_setting = df['rounded_J'] == J
    tunnel_velocity = df['rounded_v'] == V
    filtered_df = df.loc[(prop_setting) & (tunnel_velocity)].copy()     #Filter the dataframe to find rows with set J and V
    #filtered_df['CL_positive'] = filtered_df['CL'] ** 2
    CL_array = filtered_df['CL'].values                                 #Find relevant lift coefficients
    #windmilling = df['rounded_J'] == 17
    #windmilling_df = df.loc[(windmilling) & (tunnel_velocity)].copy()
    CD_curve = drag_interpolation(V)                                    #Interpolation for drag curve
    unique_aoa = filtered_df['rounded_AoA'].unique()
    CD_array = CD_curve(unique_aoa)                                     #Find drag coefficients as function of aoa
    negative_indices = np.where(unique_aoa < 0)[0]                      #Remove negative aoa for drag analysis
    CL_positive_array = np.delete(CL_array, negative_indices)
    CL_squared_array = CL_positive_array**2
    CD_positive_array = np.delete(CD_array, negative_indices)

    linear_indices = 6                                                  #Set indices for linear region

    #Curve fittings for linear and quadratic region
    CDi_coefficients = np.polyfit(CL_squared_array[:linear_indices], CD_positive_array[:linear_indices], deg=1)
    CDi_fitted_curve = np.poly1d(CDi_coefficients)
    CDs_coefficients = np.polyfit(CL_squared_array[(linear_indices-1):], CD_positive_array[(linear_indices-1):], deg=2)
    CDs_fitted_curve = np.poly1d(CDs_coefficients)

    CD0 = CDi_fitted_curve(0)
    CDi = CDi_fitted_curve(CL_unc**2)-CD0

    #Compute CDs if relevant
    CL_unc_index = np.searchsorted(CL_positive_array, CL_unc)
    if CL_unc_index < linear_indices:
        CDs = 0
    else:
        CDs = CDs_fitted_curve(CL_unc**2)-CDi-CD0

    CD_unc = CD0+CDi+CDs
    plt.plot(CL_squared_array, CDi_fitted_curve(CL_squared_array))
    plt.plot(CL_squared_array, CDs_fitted_curve(CL_squared_array))
    plt.scatter(CL_squared_array, CD_positive_array)
    plt.xlabel('CL^2')
    plt.ylabel('CD')
    #plt.show()
    # Show the plot

    return CD0, CDi, CDs, CD_unc

#print(drag_coefficients(1.6,40, 1))
