import matplotlib.pyplot as plt
from Lift_interference import *

def plot_aoa_lift(df):
    return plt.scatter(df["AoA"], df["CL"])


def plot_lift_drag(df):
    return plt.scatter(df["CD"], df["CL"])


def plot_aoa_drag(df):
    return plt.scatter(df["AoA"], df["CD"])


df_V20 = df_velocity_filter(20)
df_V40 = df_velocity_filter(40)
df_V40_cor = average_40(df_V40)

plot_aoa_lift(df_V20)
plot_aoa_lift(df_V40)
plot_aoa_lift(df_V40_cor)
plt.xlabel('AoA')
plt.ylabel("CL")
plt.grid(True)
plt.show()

plot_aoa_drag(df_V20)
plot_aoa_drag(df_V40)
plot_aoa_drag(df_V40_cor)
plt.xlabel('AoA')
plt.ylabel("CD")
plt.grid(True)
plt.show()

plot_lift_drag(df_V20)
plot_lift_drag(df_V40)
plot_lift_drag(df_V40_cor)
plt.xlabel('CD')
plt.ylabel("CL")
plt.grid(True)
plt.show()