import pandas as pd
from Data_sorting import df
import matplotlib.pyplot as plt

def graph(J,V):
    prop_setting = df['rounded_J'] == J
    tunnel_velocity = df['rounded_v'] == V
    filtered_df = df.loc[(prop_setting) & (tunnel_velocity)].copy()
    filtered_df['CL_squared'] = filtered_df['CL'] ** 2
    x_column = 'CL_squared'
    y_column = 'CD'

    filtered_df.plot(x=x_column, y=y_column, kind='scatter')

    # Add title and labels
    plt.title('Plot of {} vs {}'.format(y_column, x_column))
    plt.xlabel(x_column)
    plt.ylabel(y_column)

    # Show the plot
    plt.show()
    return

graph(1.6,40)