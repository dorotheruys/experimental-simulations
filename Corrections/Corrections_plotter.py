from Plotting.plotter import PlotData
from General.Data_sorting import specific_old_file, specific_cor_file
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

    range = [min(aoa_old)-max(aoa_old)*0.1, max(aoa_old)+max(aoa_old)*0.1]

    PlotData('AoA', 'CL', aoa_old, [CL_old, CL_cor], 'lists', ['Uncorrected', 'Corrected'])
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

    range = [min(aoa_old) - max(aoa_old) * 0.1, max(aoa_old) + max(aoa_old) * 0.1]

    PlotData('AoA', 'CD', aoa_old, [CD_old, CD_cor], 'lists', ['Uncorrected', 'Corrected'])
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

    range = [min(CD_old) - max(CD_old) * 0.1, max(CD_old) + max(CD_old) * 0.1]

    PlotData('CD', 'CL', CD_old, [CL_old, CL_cor], 'lists', ['Uncorrected', 'Corrected'])
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

    range = [min(aoa_old)-max(aoa_old)*0.1, max(aoa_old)+max(aoa_old)*0.1]

    PlotData('AoA', 'CM', aoa_old, [CM_old, CM_cor], 'lists', ['Uncorrected', 'Corrected'])

    return
J = [1.6, 1.8, 3.5]
for j in J:
    CD_CL(40, j)
plt.show()