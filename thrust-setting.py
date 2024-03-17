import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
def func(J, CT):
    return -0.0051 * J**4 + 0.0959 * J**3 - 0.5888 * J**2 + 1.0065 * J - 0.1353 - CT
def get_prop_rpm(CT):
    V_inf = 40.     # [m/s]
    D = 0.2032      # [m]
    initial_guess = 2.

    J = fsolve(func, initial_guess, args=(CT))
    ang_speed = V_inf / (J * D)

    return ang_speed

def get_CT(J):
    CT = -0.0051 * J**4 + 0.0959 * J**3 - 0.5888 * J**2 + 1.0065 * J - 0.1353
    return CT

def get_CP(J):
    Cp = -0.0093 * J**4 + 0.1832 * J**3 - 1.1784 * J**2 + 2.2005 * J - 0.5180
    return Cp

def get_eff(J):
    eta = J*get_CT(J)/get_CP(J)
    return eta

V_appr = 50.        # [m/s]

# Generate J values in the specified range help
J_values = np.linspace(0.8, 5, 100)

# Calculate CT values for each J
CT_values = get_CT(J_values)

# Calculate CT values for each J
CP_values = get_CP(J_values)

# Calculate efficiency values for each J
eff_values = get_eff(J_values)

#Experimental data
CT_exp = [0.24, 0.195, 0.16, 0.125, 0.08, 0.02]
J_exp = [1.8, 1.9, 2, 2.1, 2.2, 2.3]
# Plot the results
plt.plot(J_values, CT_values, label='Relationship')
plt.plot(J_exp, CT_exp, label='Experimental')
#plt.plot(J_values, eff_values, label='Efficiency')
plt.title('CT vs J')
plt.xlabel('J')
plt.ylabel('CT')
plt.legend()
plt.grid(True)
plt.show()