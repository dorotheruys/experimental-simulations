import numpy as np

from Plotting.plotter import PlotData
from General.Data_sorting import specific_old_file, specific_cor_file
from Sort_data.Remove_windmill_data import *
import matplotlib.pyplot as plt

def aoa_CL(V,J):
    df_cor = specific_cor_file()

    df_old = df_cor.loc[(df_cor['rounded_v'] == V) & (df_cor['rounded_J'] == J)]
    aoa_old = df_old['rounded_AoA'].values
    CL_old = df_old['CL'].values

    V_low = V - 1
    V_high = V + 1

    df_cor = df_cor.loc[(df_cor['V cor'] >= V_low) & (df_cor['V cor'] <= V_high) & (df_cor['rounded_J'] == J)]
    aoa_cor = df_cor['AoA cor'].values
    CL_cor = df_cor['CL cor'].values

    x_range_array = aoa_old

    adjustment = 0.1 * max(x_range_array)

    # Adjust the range
    range = [x_range_array[0] - adjustment] + [x + adjustment / (len(x_range_array) - 2) for x in
                                               x_range_array[1:-1]] + [x_range_array[-1] + adjustment]

    PlotData('AoA', 'CL', aoa_old, [aoa_old, CL_old, aoa_cor, CL_cor], 'lists', ['Uncorrected', 'Corrected'])
    return

def aoa_CD(V,J):
    df_cor = specific_cor_file()

    df_old = df_cor.loc[(df_cor['rounded_v'] == V) & (df_cor['rounded_J'] == J)]
    aoa_old = df_old['rounded_AoA'].values
    CD_old = df_old['Drag coefficient'].values

    V_low = V - 1
    V_high = V +1

    df_cor = df_cor .loc[(df_cor['V cor'] >= V_low) & (df_cor['V cor'] <= V_high) & (df_cor['rounded_J'] == J)]
    aoa_cor = df_cor['AoA cor'].values
    CD_cor = df_cor['CD cor'].values

    x_range_array = aoa_old

    adjustment = 0.1 * max(x_range_array)

    # Adjust the range
    range = [x_range_array[0] - adjustment] + [x + adjustment / (len(x_range_array) - 2) for x in
                                               x_range_array[1:-1]] + [x_range_array[-1] + adjustment]

    PlotData('AoA', 'CD', aoa_old, [aoa_old, CD_old, aoa_cor, CD_cor], 'lists', ['Uncorrected', 'Corrected'])
    return

def aoa_CM(V,J):
    df_cor = specific_cor_file()

    df_old = df_cor.loc[(df_cor['rounded_v'] == V) & (df_cor['rounded_J'] == J)]
    aoa_old = df_old['rounded_AoA'].values
    CM_old = df_old['CMpitch25c'].values

    V_low = V - 1
    V_high = V + 1

    df_cor = df_cor.loc[(df_cor['V cor'] >= V_low) & (df_cor['V cor'] <= V_high) & (df_cor['rounded_J'] == J)]
    aoa_cor = df_cor['AoA cor'].values
    CM_cor = df_cor['CM cor'].values

    x_range_array = aoa_old

    adjustment = 0.1 * max(x_range_array)

    # Adjust the range
    range = [x_range_array[0] - adjustment] + [x + adjustment / (len(x_range_array) - 2) for x in
                                               x_range_array[1:-1]] + [x_range_array[-1] + adjustment]

    PlotData('AoA', 'CM', range, [aoa_old, CM_old, aoa_cor, CM_cor], 'lists', ['Uncorrected', 'Corrected'])

    return

def CD_CL(V,J):
    df_cor = specific_cor_file()

    df_old = df_cor.loc[(df_cor['rounded_v'] == V) & (df_cor['rounded_J'] == J)]
    CL_old = df_old['CL'].values
    CD_old = df_old['Drag coefficient'].values

    V_low = V - 1
    V_high = V + 1

    df_cor = df_cor .loc[(df_cor['V cor'] >= V_low) & (df_cor['V cor'] <= V_high) & (df_cor['rounded_J'] == J)]
    CL_cor = df_cor['CL cor'].values
    CD_cor = df_cor['CD cor'].values

    x_range_array = CL_old

    adjustment = 0.05 * max(x_range_array)

    # Adjust the range
    # range = [x_range_array[0] - adjustment] + [x + adjustment / (len(x_range_array) - 2) for x in x_range_array[1:-1]] + [x_range_array[-1] + adjustment]
    range = np.linspace(x_range_array[0] - adjustment, x_range_array[-1] + adjustment, 100)

    # a, b, c = np.polyfit(CL_old, CD_old, deg=2)
    #
    # plot_inverse_second_degree_polynomial(a, b, c, x_range_array)
    # plt.scatter(CD_old,CL_cor)

    PlotData('CL', 'CD', range, [CL_old, CD_old, CL_cor, CD_cor], 'curvefit', ['Uncorrected', 'Corrected'])
    return

def J_CT(V,AoA):
    df_cor = specific_cor_file()

    df_old = df_cor.loc[(df_cor['rounded_v'] == V) & (df_cor['rounded_AoA'] == AoA)]
    J_old = df_old['rounded_J'].values
    CT_old = df_old['Thrust coefficient'].values

    V_low = V - 1
    V_high = V + 1

    df_cor = df_cor .loc[(df_cor['V cor'] >= V_low) & (df_cor['V cor'] <= V_high) & (df_cor['rounded_AoA'] == AoA)]
    J_cor = df_cor['rounded_J'].values
    CT_cor = df_cor['CT cor'].values

    x_range_array = J_old

    adjustment = 0.05 * max(x_range_array)

    # Adjust the range
    # range = [x_range_array[0] - adjustment] + [x + adjustment / (len(x_range_array) - 2) for x in x_range_array[1:-1]] + [x_range_array[-1] + adjustment]
    range = np.linspace(x_range_array[0] - adjustment, x_range_array[-1] + adjustment, 100)

    # a, b, c = np.polyfit(CL_old, CD_old, deg=2)
    #
    # plot_inverse_second_degree_polynomial(a, b, c, x_range_array)
    # plt.scatter(CD_old,CL_cor)

    PlotData('J', 'CT', range, [J_old, CT_old, J_cor, CT_cor], 'lists', ['Uncorrected', 'Corrected'])
    return

# J = [1.6]
# for j in J:
#     CD_CL(40, j)
# aoa = [7]
# for angle in aoa:
#     J_CT(40, angle)
# plt.show()