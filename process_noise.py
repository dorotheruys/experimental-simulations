#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 18:43:44 2024

@author: jackcheng
"""
import scipy as sp
import numpy as np
import pandas as pd
import matlab.engine
import math
import matplotlib.pyplot as plt
import os

#%%
current_dir = os.path.dirname(os.path.abspath(__file__))

#some file path thing I guess
avg_file1=os.path.join(current_dir, 'Noisedata_from_matlab/AVGdata_neg15_2.mat')
avg_file2=os.path.join(current_dir, 'Noisedata_from_matlab/AVGdata_0.mat')
avg_file3=os.path.join(current_dir, 'Noisedata_from_matlab/AVGdata_plus15.mat')

#mic data with calibration
micCal_file1=os.path.join(current_dir, 'Noisedata_from_matlab/micCal_neg15_2.mat')
micCal_file2=os.path.join(current_dir, 'Noisedata_from_matlab/micCal_0.mat')
micCal_file3=os.path.join(current_dir, 'Noisedata_from_matlab/micCal_plus15.mat')

#corresponding operating conditions
opp_file1=os.path.join(current_dir, 'Noisedata_from_matlab/opp_neg15_2.mat')
opp_file2=os.path.join(current_dir, 'Noisedata_from_matlab/opp_0.mat')
opp_file3=os.path.join(current_dir, 'Noisedata_from_matlab/opp_plus15.mat')

#spectral analysis data
w_file1=os.path.join(current_dir, 'Noisedata_from_matlab/w_neg15_2.mat')
w_file2=os.path.join(current_dir, 'Noisedata_from_matlab/w_0.mat')
w_file3=os.path.join(current_dir, 'Noisedata_from_matlab/w_plus15.mat')

#load data with matlab engine
eng = matlab.engine.start_matlab()
s = eng.load(micCal_file1)
# s2=eng.load(file_p)

#%%







