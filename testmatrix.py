import numpy as np
import itertools
import pandas as pd
import datetime

def get_test_matrix():
    dummy = [n_elevator, n_windspeed, n_prop, n_angles]
    comb = list(itertools.product(*dummy))
    mat = np.zeros((len(comb), 4))
    for i in range(4):
        for j in range(len(comb)):
            mat[j, i] = comb[j][i]
    mat = pd.DataFrame(mat, columns=['Elevator', 'Tunnel velocity', 'propeller setting', 'AoA'])
    return mat


# calculates time for wind on
def wind_on(na, n_p, nv, n_e):
    a = len(na)
    b = len(n_p)
    c = len(nv)
    d = len(n_e)
    prop_onoff = 15 * 60
    c_ele = 15 * 60
    c_tunnel_v = 2 * 60
    c_alpha = 25
    t_samp = 7  # sampling time per point
    c_prop_set = 30
    set1 = a * c_alpha * b + b * c_prop_set
    set2 = set1 * c + c * c_tunnel_v
    set3 = set2 * d + d * c_ele
    sampling_time = a * b * c * d * t_samp
    return (set3 + sampling_time) / 60  # return time in minutes

def wind_off(na):
    a = len(na)
    prop_onoff = 15 * 60
    c_ele = 15 * 60
    c_tunnel_v = 2 * 60
    c_alpha = a * 2 + 20
    t_samp = 10
    prop_set = 30

    return (a * (c_alpha - 1) + prop_onoff) / 60  # return time in minutes

def time_estimate(df):
    # Calculate differences
    AoA_diff = df["AoA"].diff().abs()
    elevator_diff = df["Elevator"].diff().abs()
    velocity_diff = df["Tunnel velocity"].diff().abs()
    propset_diff = df["propeller setting"].diff().abs()

    # Calculate point_time and total_time
    point_time = AoA_diff * 2 + 15
    point_time += (velocity_diff != 0) * 60
    point_time += (elevator_diff != 0) * (12.5 * 60 + 3 * 60)
    point_time += (propset_diff != 0) * 30
    total_time = point_time.cumsum()

    # Manually set the values for the first item
    point_time.iloc[0] = 0  # or any value you want
    total_time.iloc[0] = 0  # or any value you want

    def convert_to_hms(series):
        return series.apply(lambda x: pd.to_timedelta(x, unit='s').components).apply(
            lambda x: '{:02}:{:02}:{:02}'.format(x.hours, x.minutes, x.seconds))

    df["setpoint time"] = convert_to_hms(point_time)
    df["total time"] = convert_to_hms(total_time)

    return df




n_angles = [-5, 7, 12, 14]  # [deg]
n_elevator = [-15, 0, 15]  # [deg]
n_windspeed = [10, 20, 40]  # [m/s]
n_prop = [0, 1, 2]  # [rpm]

# n_angles = [-5, 7, 12, 14]  # [deg]
# n_elevator = [0,15]  # [deg]
# n_windspeed = [40]  # [m/s]
# n_prop = [2]  # [rpm]

# 15+5 for tunnel prep, 10 for trimming
total_time = wind_on(n_angles, n_prop, n_windspeed, n_elevator) + wind_off(n_angles) + 15 + 5 + 10
print('total time=', total_time, 'minutes')

testmatrix = get_test_matrix()

print(time_estimate(testmatrix))
print(f"3 hours = {3*60*60} seconds")