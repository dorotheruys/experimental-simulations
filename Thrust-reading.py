import numpy as np
def thrust_initial(Cx,Cz,Fx,Fz):
    phi_y = np.arctan((Fz - Cz) / (Cx - Fx))
    thrust = (Fz-Cz)/(np.sin(phi_y))
    return phi_y, thrust

Cx =
Cz =
Fx_initial =
Fz_initial =

phi_y, thrust = thrust_initial(Cx,Cz,Fx_initial,Fz_initial)

def thrust(Cx,Fx,phi_y):
