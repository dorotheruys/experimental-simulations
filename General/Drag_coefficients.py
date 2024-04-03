from General.Thrust_calculation import *

def drag_coefficients(J,V,CL_unc,df):
    # prop_setting = df['rounded_J'] == J
    # tunnel_velocity = df['rounded_v'] == V
    # filtered_df = df.loc[(prop_setting) & (tunnel_velocity)].copy()     #Filter the dataframe to find rows with set J and V
    #Find an interpolate relevant lift coefficients
    tunnel_prop_combi = [[{'rounded_v': V}, {'rounded_J': J}]]
    CL_alpha_function = get_function_from_dataframe(df, 2, 'AoA', 'CL_thrust_cor', tunnel_prop_combi,np.linspace(-6, 20, 26),None,None)
    CL_array = CL_alpha_function[0].poly_coeff(np.arange(-5,14.1,1))

    CD_curve = drag_interpolation(V, df)                                     #Interpolation for drag curve
    unique_aoa = np.arange(-5,14.1,1)#filtered_df['rounded_AoA'].unique()
    CD_array = CD_curve(unique_aoa)                                     #Find drag coefficients as function of aoa
    negative_indices = np.where(unique_aoa < 0)[0]                      #Remove negative aoa for drag analysis
    CL_positive_array = np.delete(CL_array, negative_indices)
    CL_squared_array = CL_positive_array**2
    CD_positive_array = np.delete(CD_array, negative_indices)


    linear_indices = 8                                                 #Set indices for linear region
    R_squared = 0                                                       #Temporary value
    # While loop to find appropriate R value for linear part of CD vs CL^2
    while R_squared < 0.965:
    #Curve fittings for linear and quadratic region
        CDi_coefficients = np.polyfit(CL_squared_array[:linear_indices], CD_positive_array[:linear_indices], deg=1)
        CDi_fitted_curve = np.poly1d(CDi_coefficients)

        correlation_matrix = np.corrcoef(CD_positive_array[:linear_indices], CDi_fitted_curve(CL_squared_array[:linear_indices]))
        R_squared = correlation_matrix[0, 1] ** 2
        linear_indices = linear_indices-1
    CDs_coefficients = np.polyfit(CL_squared_array[(linear_indices-1):], CD_positive_array[(linear_indices-1):], deg=4)
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

    #Plotting
    plt.plot(CL_squared_array, CDi_fitted_curve(CL_squared_array))
    plt.plot(CL_squared_array, CDs_fitted_curve(CL_squared_array))
    plt.scatter(CL_squared_array, CD_positive_array)
    plt.xlabel('CL^2')
    plt.ylabel('CD')
    #plt.show()
    return CD0, CDi, CDs, CD_unc

#Separate drag and thrust coefficients
def CD_CT(df):
    cor = False
    df_drag_thrust_coefficient = pd.DataFrame(columns=['Drag coefficient', 'Thrust coefficient'])
    for index, row in df.iterrows():
        Vunc = row["rounded_v"]
        J = row["rounded_J"]
        curve = drag_interpolation(Vunc, df)
        AoA = row['rounded_AoA']
        CDunc = curve(AoA)
        CT = Thrust_estimation(J,Vunc,AoA, df, cor)

        add_columns = [CDunc, CT]

        # Create a temporary DataFrame to hold the current row
        df_temp = pd.DataFrame([add_columns], columns=['Drag coefficient', 'Thrust coefficient'])

        # Drop empty or all-NA columns from df_temp
        df_drag_thrust_coefficient = df_drag_thrust_coefficient.dropna(axis=1, how='all')

        # Append the temporary DataFrame to the main DataFrame
        df_drag_thrust_coefficient = pd.concat([df_drag_thrust_coefficient, df_temp], ignore_index=True)
    df_drag_thrust_coefficient = pd.concat([df, df_drag_thrust_coefficient], axis=1)
    #Correct for thrust influence on lift
    df_drag_thrust_coefficient['CL_thrust_cor'] = df_drag_thrust_coefficient['CL_strut_cor'] - df_drag_thrust_coefficient['Thrust coefficient'] * np.sin(df_drag_thrust_coefficient['rounded_AoA']*np.pi/180)
    return df_drag_thrust_coefficient
