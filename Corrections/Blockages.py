import numpy as np
from Corrections.Drag_coefficients import drag_coefficients

def Solidblockage():
    K3f = 0.91
    K3n = 0.93
    tau1 = 0.88
    C = 2.25
    V_fus = 0.0160632
    V_nac = 0.0007921
    K1_w = 1 #placeholder, find correct value
    K1_ht = 1.01
    K1_vt = 1.01
    V_w = 0.0030229
    V_ht = 0.0009751
    V_vt = 0.0003546

    e_sb_f = tau1 * (K3f * V_fus + K3n * V_nac) / (C ** 1.5)
    e_sb_w = tau1 * (K1_w * V_w + K1_ht * V_ht + K1_vt * V_vt) / (C ** 1.5)
    e_sb = e_sb_f + e_sb_w
    return e_sb

def Wakeblockage(J,V,CL):
    CD0, CDi, CDs, CD_unc = drag_coefficients(J,V,CL)
    D_fuselage = 0.14
    t_c_wing = 0.1
    mac_wing = 0.165
    b_wing = 1.397
    D_prop = 0.2032
    t_c_vtail = 0.15
    mac_vtail = 0.17
    b_vtail = 0.258

    S_ref = np.pi * D_fuselage ** 2 / 4 + t_c_wing * mac_wing * b_wing + np.pi * D_prop / 4 + t_c_vtail * mac_vtail * b_vtail
    C_tunnel = b_wing ** 2 * 1.29 * 0.98

    e_wbt = S_ref / (4 * C_tunnel) * CD0
    e_wbs = 5 * S_ref / (4 * C_tunnel) * (CD_unc-CD0-CDi)

    e_wbt = e_wbt + e_wbs;
    return e_wbt

print(Wakeblockage(1.6,40,2))