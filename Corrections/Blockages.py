
from General.Drag_coefficients import drag_coefficients
from General.Thrust_calculation import *

def Solidblockage():
    K3f = 0.91     #d/l=0.10
    K3n = 0.93     #d=sqrt(0.0007921/0.345/pi)*2 l=0.345 d/l=0.15
    tau1 = 0.88    #B/H=1.5 2b/B=0.775
    C = 1.8*1.25-0.3**2/2*4 #Removed the corners
    V_fus = 0.0160632
    V_nac = 0.0007921
    K1_w = 0.965   #t/c=0.09395930576700445
    K1_ht = 0.96   #t/c=0.0838504
    K1_vt = 0.97   #t/c=0.09455764705882352
    V_w = 0.09395930576700445*0.165**2*1.397
    V_ht = 0.0838504*0.149**2*0.576
    V_vt = 0.09455764705882352*0.17**2*0.258
    e_sb_f = tau1 * (K3f * V_fus + K3n * V_nac) / (C ** 1.5)
    e_sb_w = tau1 * (K1_w * V_w + K1_ht * V_ht + K1_vt * V_vt) / (C ** 1.5)
    e_sb = e_sb_f + e_sb_w
    return e_sb

def Wakeblockage(J,V,CL,df):
    CD0, CDi, CDs, CD_unc = drag_coefficients(J,V,CL,df)
    D_fuselage = 0.14
    t_c_wing = 0.09395930576700445
    mac_wing = 0.165
    b_wing = 1.397
    D_prop = 0.2032
    t_c_vtail = 0.09455764705882352
    mac_vtail = 0.17
    b_vtail = 0.258

    S_ref = np.pi * D_fuselage ** 2 / 4 + t_c_wing * mac_wing * b_wing + np.pi * 2 * D_prop ** 2 / 4 + t_c_vtail * mac_vtail * b_vtail
    C_tunnel = 1.8*1.25-0.3**2/2*4
    e_wbt = S_ref / (4 * C_tunnel) * CD0
    e_wbs = 5 * S_ref / (4 * C_tunnel) * (CD_unc-CD0-CDi)

    e_wbt = e_wbt + e_wbs
    return e_wbt

def slipstream(J,V,AoA, df):
    thrust_coefficient1 = Thrust_estimation(J,V,AoA, df)
    Dprop = 0.2032
    Sp = np.pi / 4 * Dprop ** 2
    C = 1.8*1.25-0.3**2/2*4
    n = V/(Dprop*J)
    prop_setting = df['rounded_J'] == J
    tunnel_velocity = df['rounded_v'] == V
    filtered_df = df.loc[(prop_setting) & (tunnel_velocity)].copy()
    rho = filtered_df['rho'].mean()
    thrust = thrust_coefficient1 * rho * n ** 2 * Dprop ** 4
    thrust_coefficient2 = thrust/(rho*V**2*Sp)
    e_ss = - thrust_coefficient2/(2*np.sqrt(1+2*thrust_coefficient2))*2*Sp/C
    return e_ss

def Full_blockage(df):
    df_blockage_corrections = pd.DataFrame(columns=['V cor', 'q cor', 'CDbcor', 'CMbcor', 'CL cor'])
    for index, row in df.iterrows():
        #Solid blockage
        e_sb = Solidblockage()

        #Wake blockage
        J = row['rounded_J']
        Vunc = row["rounded_v"]
        CLunc = row['CL_thrust_cor']
        e_wbt = Wakeblockage(J, Vunc, CLunc, df)

        #Slipstream blockage
        AoA = row['rounded_AoA']
        e_ss = slipstream(J, Vunc, AoA, df)

        #Total blockage
        e_total = e_sb+e_wbt+e_ss

        #Other variables
        qunc = row['q']
        CDunc = row['Drag coefficient']
        CMunc = row['CMpitch25c_strut_cor']
        #Corrections
        V = Vunc*(1+e_total)
        q = qunc*(1+e_total)**2
        CL = CLunc*(1+e_total)**(-2)
        CD = CDunc*(1+e_total)**(-2)
        CM = CMunc * (1 + e_total) ** (-2)

        add_columns = [V, q, CD, CM, CL]

        # Create a temporary DataFrame to hold the current row
        df_temp = pd.DataFrame([add_columns], columns=['V cor', 'q cor', 'CDbcor', 'CMbcor', 'CL cor'])

        # Drop empty or all-NA columns from df_temp
        df_blockage_corrections = df_blockage_corrections.dropna(axis=1, how='all')

        # Append the temporary DataFrame to the main DataFrame
        df_blockage_corrections = pd.concat([df_blockage_corrections, df_temp], ignore_index=True)
    df_blockage_corrections = pd.concat([df, df_blockage_corrections], axis=1)
    return df_blockage_corrections