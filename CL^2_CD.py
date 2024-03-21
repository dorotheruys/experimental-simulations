import pandas as pd
from Data_sorting import *
from Thrust_calculation import Thrust_estimation
import matplotlib.pyplot as plt

def graph(J,V):
    thrust_lst = []
    for aoa in aoa_lst:
        thrust_lst.append(Thrust_estimation(J,V, aoa))
    prop_setting = df['rounded_J'] == J
    tunnel_velocity = df['rounded_v'] == V
    filtered_df = df.loc[(prop_setting) & (tunnel_velocity)].copy()
    filtered_df['CL_squared'] = filtered_df['CL'] ** 2
    CL_squared_array = filtered_df['CL_squared'].values
    CD_array = filtered_df['CD'].values+thrust_lst

    plt.scatter(CL_squared_array, CD_array)
    plt.xlabel('CL^2')
    plt.ylabel('CD')

    # Show the plot
    plt.show()
    return

graph(1.6,40)