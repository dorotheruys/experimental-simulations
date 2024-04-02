import numpy as np

from Plotting.plotter import PlotData
from General.Data_sorting import specific_old_file, specific_cor_file
from Sort_data.Remove_windmill_data import *
import matplotlib.pyplot as plt

def aoa_CL(V,J, filename):
    df_cor = specific_cor_file(filename)

    df_old = df_cor.loc[(df_cor['rounded_v'] == V) & (df_cor['rounded_J'] == J)]
    aoa_old = df_old['rounded_AoA'].values
    CL_old = df_old['CL'].values
    V_low = V - 1
    V_high = V + 1

    df_cor = df_cor.loc[(df_cor['V cor'] >= V_low) & (df_cor['V cor'] <= V_high) & (df_cor['rounded_J'] == J)]
    aoa_cor = df_cor['AoA cor'].values
    CL_cor = df_cor['CL cor'].values

    # Adjust the range
    range = np.linspace(-10, 20, 100)
    old = np.vstack((aoa_old, CL_old)).tolist()
    cor = np.vstack((aoa_cor, CL_cor)).tolist()
    #PlotData('AoA', 'CL', range, [aoa_old, CL_old, aoa_cor, CL_cor], 'curvefit', ['Uncorrected', 'Corrected'])
    return range, old, cor

def aoa_CL_plot(filename):
    J = [1.8, 3.5]
    old_lst = []
    cor_lst = []
    for j in J:
        range, old, cor = aoa_CL(40, j, filename)
        old_lst.append(old)
        cor_lst.append(cor)
    PlotData('AoA', 'CL', range, [old_lst[0][0], old_lst[0][1], cor_lst[0][0], cor_lst[0][1], old_lst[1][0], old_lst[1][1],  cor_lst[1][0], cor_lst[1][1]], 'curvefit', [ 'Uncorrected J=1.8', 'Corrected J=1.8', 'Uncorrected J=3.5',  'Corrected J=3.5'])
    plt.show()
    return

def aoa_CD(V,J, filename):
    df_cor = specific_cor_file(filename)

    df_old = df_cor.loc[(df_cor['rounded_v'] == V) & (df_cor['rounded_J'] == J)]
    aoa_old = df_old['rounded_AoA'].values
    CD_old = df_old['Drag coefficient'].values
    V_low = V - 1
    V_high = V +1

    df_cor = df_cor .loc[(df_cor['V cor'] >= V_low) & (df_cor['V cor'] <= V_high) & (df_cor['rounded_J'] == J)]
    aoa_cor = df_cor['AoA cor'].values
    CD_cor = df_cor['CD cor'].values

    # Adjust the range
    range = np.linspace(-10, 20, 100)
    old = np.vstack((aoa_old, CD_old)).tolist()
    cor = np.vstack((aoa_cor, CD_cor)).tolist()
    #PlotData('AoA', 'CD', range, [aoa_old, CD_old, aoa_cor, CD_cor], 'curvefit', ['Uncorrected', 'Corrected'])
    return range, old, cor

def aoa_CD_plot(filename):
    J = [1.8, 3.5]
    old_lst = []
    cor_lst = []
    for j in J:
        range, old, cor = aoa_CD(40, j, filename)
        old_lst.append(old)
        cor_lst.append(cor)
    PlotData('AoA', 'CD', range, [old_lst[0][0], old_lst[0][1], cor_lst[0][0], cor_lst[0][1], old_lst[1][0], old_lst[1][1],  cor_lst[1][0], cor_lst[1][1]], 'curvefit', [ 'Uncorrected J=1.8', 'Corrected J=1.8', 'Uncorrected J=3.5',  'Corrected J=3.5'])
    plt.show()
    return

def aoa_CM(V,J, filename):
    df_cor = specific_cor_file(filename)

    df_old = df_cor.loc[(df_cor['rounded_v'] == V) & (df_cor['rounded_J'] == J)]
    aoa_old = df_old['rounded_AoA'].values
    CM_old = df_old['CMpitch25c'].values

    V_low = V - 1
    V_high = V + 1

    df_cor = df_cor.loc[(df_cor['V cor'] >= V_low) & (df_cor['V cor'] <= V_high) & (df_cor['rounded_J'] == J)]
    aoa_cor = df_cor['AoA cor'].values
    CM_cor = df_cor['CM cor'].values

    range = np.linspace(-10, 20, 100)
    old = np.vstack((aoa_old, CM_old)).tolist()
    cor = np.vstack((aoa_cor, CM_cor)).tolist()
    #PlotData('AoA', 'CM', range, [aoa_old, CM_old, aoa_cor, CM_cor], 'curvefit', ['Uncorrected', 'Corrected']
    return range, old, cor

def aoa_CM_plot(filename):
    J = [1.8, 3.5]
    old_lst = []
    cor_lst = []
    for j in J:
        range, old, cor = aoa_CM(40, j, filename)
        old_lst.append(old)
        cor_lst.append(cor)
    PlotData('AoA', 'CM', range, [old_lst[0][0], old_lst[0][1], cor_lst[0][0], cor_lst[0][1], old_lst[1][0], old_lst[1][1],  cor_lst[1][0], cor_lst[1][1]], 'curvefit', [ 'Uncorrected J=1.8', 'Corrected J=1.8', 'Uncorrected J=3.5',  'Corrected J=3.5'])
    plt.show()
    return

def CL_CD(V,J, filename):
    df_cor = specific_cor_file(filename)

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
    #range = np.linspace(x_range_array[0] - adjustment, x_range_array[-1] + adjustment, 100)
    # a, b, c = np.polyfit(CL_old, CD_old, deg=2)
    #
    # plot_inverse_second_degree_polynomial(a, b, c, x_range_array)
    # plt.scatter(CD_old,CL_cor)
    range = np.linspace(-0.5, 1.5, 100)
    old = np.vstack((CL_old, CD_old)).tolist()
    cor = np.vstack((CL_cor, CD_cor)).tolist()
    #PlotData('CL', 'CD', range, [CL_old, CD_old, CL_cor, CD_cor], 'curvefit', ['Uncorrected', 'Corrected'])
    return range, old, cor

def CL_CD_plot(filename):
    J = [1.8, 3.5]
    old_lst = []
    cor_lst = []
    for j in J:
        range, old, cor = CL_CD(40, j, filename)
        old_lst.append(old)
        cor_lst.append(cor)
    PlotData('CL', 'CD', range, [old_lst[0][0], old_lst[0][1], cor_lst[0][0], cor_lst[0][1], old_lst[1][0], old_lst[1][1],  cor_lst[1][0], cor_lst[1][1]], 'curvefit', [ 'Uncorrected J=1.8', 'Corrected J=1.8', 'Uncorrected J=3.5',  'Corrected J=3.5'])
    plt.show()
    return

def J_CT(V,AoA, filename):
    df_cor = specific_cor_file(filename)

    df_old = df_cor.loc[(df_cor['rounded_v'] == V) & (df_cor['rounded_AoA'] == AoA)]
    J_old = df_old['rounded_J'].values
    CT_old = df_old['Thrust coefficient'].values

    V_low = V - 1
    V_high = V + 1

    df_cor = df_cor .loc[(df_cor['V cor'] >= V_low) & (df_cor['V cor'] <= V_high) & (df_cor['rounded_AoA'] == AoA)]
    J_cor = df_cor['rounded_J'].values
    CT_cor = df_cor['CT cor'].values

    # Adjust the range
    # range = [x_range_array[0] - adjustment] + [x + adjustment / (len(x_range_array) - 2) for x in x_range_array[1:-1]] + [x_range_array[-1] + adjustment]
    # range = np.linspace(x_range_array[0] - adjustment, x_range_array[-1] + adjustment, 100)
    # a, b, c = np.polyfit(CL_old, CD_old, deg=2)
    #
    # plot_inverse_second_degree_polynomial(a, b, c, x_range_array)
    # plt.scatter(CD_old,CL_cor)
    range = np.linspace(1.5, 3.6, 100)
    old = np.vstack((J_old, CT_old)).tolist()
    cor = np.vstack((J_cor, CT_cor)).tolist()
    #PlotData('J', 'CT', range, [J_old, CT_old, J_cor, CT_cor], 'lists', ['Uncorrected', 'Corrected'])
    return range, old, cor

def J_CT_plot(filename):
    aoa = [7, 12]
    old_lst = []
    cor_lst = []
    for angle in aoa:
        range, old, cor = J_CT(40, angle, filename)
        old_lst.append(old)
        cor_lst.append(cor)
    PlotData('J', 'CT', range, [old_lst[0][0], old_lst[0][1], cor_lst[0][0], cor_lst[0][1], old_lst[1][0], old_lst[1][1],  cor_lst[1][0], cor_lst[1][1]], 'lists', [ 'Uncorrected J=1.8', 'Corrected J=1.8', 'Uncorrected J=3.5',  'Corrected J=3.5'])
    plt.show()
    return

J_CT_plot(2)