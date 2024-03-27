import numpy as np
from General.Drag_coefficients import drag_coefficients

def Solidblockage():
    K3f = 0.91     #d/l=0.10
    K3n = 0.93     #d=sqrt(0.0007921/0.345/pi)*2 l=0.345 d/l=0.15
    tau1 = 0.88    #B/H=1.5 2b/B=0.775
    C = 1.8*1.25-0.3**2/2*4
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

Solidblockage()

def Wakeblockage(J,V,CL):
    CD0, CDi, CDs, CD_unc = drag_coefficients(J,V,CL)
    D_fuselage = 0.14
    t_c_wing = 0.09395930576700445
    mac_wing = 0.165
    b_wing = 1.397
    D_prop = 0.2032
    t_c_vtail = 0.09455764705882352
    mac_vtail = 0.17
    b_vtail = 0.258

    S_ref = np.pi * D_fuselage ** 2 / 4 + t_c_wing * mac_wing * b_wing + np.pi * D_prop ** 2 / 4 + t_c_vtail * mac_vtail * b_vtail
    C_tunnel = 1.8*1.25-0.3**2/2*4
    e_wbt = S_ref / (4 * C_tunnel) * CD0
    e_wbs = 5 * S_ref / (4 * C_tunnel) * (CD_unc-CD0-CDi)

    e_wbt = e_wbt + e_wbs
    return e_wbt

print(Wakeblockage(1.6,40,2))