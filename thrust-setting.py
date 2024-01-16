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


V_appr = 50.        # [m/s]

# Generate J values in the specified range
J_values = np.linspace(0.5, 3, 100)

# Calculate CT values for each J
CT_values = get_CT(J_values)

# Plot the results
plt.plot(J_values, CT_values, label='CT(J)')
plt.title('CT vs J')
plt.xlabel('J')
plt.ylabel('CT')
plt.legend()
plt.grid(True)
plt.show()