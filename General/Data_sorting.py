import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

filename = int(input('Enter elevator deflection (1, 2 or 3): '))

if filename==1:
    df = pd.read_csv('../Sort_data/bal_sorted1.csv')
elif filename==2:
    df = pd.read_csv('../Sort_data/bal_sorted2.csv')

    # There were two similar rows with the same angle of attack in bal_sorted2. Took the average of them
    # double_aoa_rows = df[(df['rounded_AoA'] == 4) & (df['rounded_v'] == 20)]
    # row_indices = double_aoa_rows.index
    # average_values = (df.loc[row_indices[0]] + df.loc[row_indices[1]]) / 2
    # df.loc[row_indices[0]] = average_values
    # df.drop(row_indices[1], inplace=True)
    # df.reset_index(drop=True, inplace=True)
elif filename == 3:
    df = pd.read_csv('../Sort_data/bal_sorted3.csv')
else:
    print('WRONG FILE SPECIFIED')



# tunnel_velocity = df['rounded_v'] == 40
# aoa_setting = df['rounded_AoA'] == 7
# df = df.loc[(tunnel_velocity) & (aoa_setting)].copy()
# #df.plot(x='rounded_J', y='FX', kind='scatter', title='Scatter Plot of Fx vs J')
# j = df['J_M1'].values
# ct = df['Thrust coefficient'].values
#
# j = j[:-1]
# ct = ct[:-1]
# curve_fit=np.poly1d(np.polyfit(j,ct,2))
# def get_CT(J):
#     CT = -0.0051 * J**4 + 0.0959 * J**3 - 0.5888 * J**2 + 1.0065 * J - 0.1353
#     return CT
#
# # Generate J values in the specified range help
# J_values = np.linspace(0.8, 5, 100)
#
# # Calculate CT values for each J
# CT_values = get_CT(J_values)
#
# #Experimental data
# CT_exp = [0.24, 0.195, 0.16, 0.125, 0.08, 0.02]
# J_exp = [1.8, 1.9, 2, 2.1, 2.2, 2.3]
# # Plot the results
# j_array = np.arange(0,30,1)
# #plt.plot(j_array,curve_fit(j_array), label='curvefit')
# plt.plot(j,ct,label='windtunnel data')
# plt.plot(J_values, CT_values, label='Relationship')
# plt.plot(J_exp, CT_exp, label='Experimental')
# plt.grid()
# plt.legend()
# # Show the plot
# plt.show()