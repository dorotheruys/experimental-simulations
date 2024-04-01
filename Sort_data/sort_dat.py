#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 09:46:42 2024

@author: jackcheng
"""

import scipy as sp
import numpy as np
import pandas as pd
import matlab.engine
import math
import matplotlib.pyplot as plt

# %%
# key names for windon in BAL
names = ['run', 'hr', 'min', 'sec', 'AoA', 'AoS', 'dPb', 'pBar', 'temp', 'B', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', \
         'rpmWT', 'rho', 'q', 'V', 'Re', 'rpsM1', 'rpsM2', 'iM1', 'iM2', 'dPtQ', 'pInf', 'nu', 'J_M1', 'J_M2', \
         'B16zeroed', 'FX', 'FY', 'FZ', 'MX', 'MY', 'MZ', 'CFX', 'CFY', 'CFZ', 'CMX', 'CMY', 'CMZ', \
         'CN', 'CT', 'CL', 'CD', 'CYaw', 'CMroll', 'CMpitch', 'CMpitch25c', 'CMyaw', 'b', 'c', 'S']

# key names for windoff in BAL
names_z = ['run', 'hr', 'min', 'sec', 'AoA', 'AoS', 'pBar', 'temp', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']

# key names in PRS
names_p = ['run', 'hr', 'min', 'sec', 'AoA', 'AoS', 'dPb', 'pBar', 'temp', 'rpmWT', 'rho', 'q', 'V', 'Re', 'pTfs', \
           'pSfs', 'pTaps', 'CpTaps', 'rpsM1']

# %%
# load data with matlab engine
file = 'Sort_data/BAL_05neg15.mat'
file_p = 'Sort_data/PRS_dat.mat'

eng = matlab.engine.start_matlab()
s = eng.load(file)
s2 = eng.load(file_p)

# %%
# windon measurements of BAL
set1 = s['BAL']['windOn']['group19delta_neg15_2']
set2 = s['BAL']['windOn']['group19delta_0']
set3 = s['BAL']['windOn']['group19delta_15']
# wind off measurements of BAL
set1_z = s['BAL']['windOff']['group19delta_neg15_2']
set2_z = s['BAL']['windOff']['group19delta_0']
set3_z = s['BAL']['windOff']['group19delta_15']

# data in PRS
set1_p = s2['PRS']['group19delta_neg15_2']
set2_p = s2['PRS']['group19delta_0']
set3_p = s2['PRS']['group19delta_plus15']

# %%
# initialize empty dictionary
delta_neg15 = {}
delta_0 = {}
delta_15 = {}

delta_neg15_z = {}
delta_0_z = {}
delta_15_z = {}

delta_neg15_p = {}
delta_0_p = {}
delta_15_p = {}

# write everything into dict
for i in range(len(names)):
    delta_neg15[names[i]] = np.array(set1[names[i]])
    delta_0[names[i]] = np.array(set2[names[i]])
    delta_15[names[i]] = np.array(set3[names[i]])
for i in range(len(names_z)):
    delta_neg15_z[names_z[i]] = np.array(set1_z[names_z[i]]).flatten()
    delta_0_z[names_z[i]] = np.array(set2_z[names_z[i]]).flatten()
    delta_15_z[names_z[i]] = np.array(set3_z[names_z[i]]).flatten()

for i in range(len(names_p)):
    delta_neg15_p[names_p[i]] = np.array(set1_p[names_p[i]])
    delta_0_p[names_p[i]] = np.array(set2_p[names_p[i]])
    delta_15_p[names_p[i]] = np.array(set3_p[names_p[i]])

delta_neg15_z = pd.DataFrame.from_dict(delta_neg15_z)
delta_0_z = pd.DataFrame.from_dict(delta_neg15_z)
delta_15_z = pd.DataFrame.from_dict(delta_neg15_z)


# %%
def sort1(data):
    # remove stuff
    dummy = data.copy()

    pop_lst = ['B', 'B16zeroed', 'b', 'c', 'S']
    for i in pop_lst:
        dummy.pop(i)
    k = list(dummy.keys())

    for i in range(len(dummy)):
        a = dummy[k[i]]
        dummy[k[i]] = a.flatten()
    df = pd.DataFrame.from_dict(dummy, orient='columns')

    # round velocity to nearest 10,20 or 40
    rnd_v = np.array([40, 20, 10])
    rnd_J = np.array([1.6, 3.5, 1.8, 17])
    rnd_alpha = np.array([7, 14, -5, 12])

    V_round = []
    J_round = []
    alpha_round = []
    prop_io = []
    for i in range(len(df['V'])):
        diff1 = abs(np.ones(3) * df['V'][i] - rnd_v)
        V_round.append(rnd_v[np.argmin(diff1)])

        diff2 = abs(np.ones(4) * df['J_M1'][i] - rnd_J)
        J_round.append(rnd_J[np.argmin(diff2)])

        # diff3=abs(np.ones(4)*df['AoA'][i]-rnd_alpha)
        alpha_round.append(round(df['AoA'][i]))

    df.insert(19, 'rounded_v', V_round)
    df.insert(28, 'rounded_J', J_round)
    df.insert(5, 'rounded_AoA', alpha_round)
    return df


# enter advance ratio or "off" for off setting
# input for vel and prop must be exactly equal to the values in the array below
# rnd_v=np.array([40,20,10])
# rnd_J=np.array([1.6,3.5,1.8,17])
def get_set(data, vel, prop):
    if prop == 'off':
        prop = 17
        group1 = data.groupby('rounded_J')
        layer1 = group1.get_group(prop)

        group2 = layer1.groupby('rounded_v')
        layer2 = group2.get_group(vel)
    else:

        group1 = data.groupby('rounded_v')
        layer1 = group1.get_group(vel)

        group2 = layer1.groupby('rounded_J')
        layer2 = group2.get_group(prop)

    return layer2.sort_values(by='AoA')


inp_lst = [(40, 1.6), (40, 1.8), (40, 3.5), (20, 1.6), (10, 1.6), (40, 17), (20, 17), (10, 17)]


def final_sort(data):
    dat = []
    for i in range(len(inp_lst)):
        dat.append(get_set(data, inp_lst[i][0], inp_lst[i][1]))
    return pd.concat(dat)


bal_sorted1 = final_sort(sort1(delta_neg15))
bal_sorted2 = final_sort(sort1(delta_0))
bal_sorted3 = final_sort(sort1(delta_15))
