from General.Thrust_calculation import *

def slipstream(J,V,AoA):
    thrust_coefficient1 = Thrust_estimation(J,V,AoA)
    Dprop = 0.2032
    Sp = np.pi / 4 * Dprop ** 2
    C = 1.29 * 0.89 * 1.397 ** 2
    n = V/(Dprop*J)
    prop_setting = df['rounded_J'] == J
    tunnel_velocity = df['rounded_v'] == V
    filtered_df = df.loc[(prop_setting) & (tunnel_velocity)].copy()
    rho = filtered_df['rho'].mean()
    thrust = thrust_coefficient1 * rho * n ** 2 * Dprop ** 4
    thrust_coefficient2 = thrust/(rho*V**2*Sp)
    e_ss = - thrust_coefficient2/(2*np.sqrt(1+2*thrust_coefficient2))*Sp/C
    return e_ss

print(slipstream(1.6,40,1))