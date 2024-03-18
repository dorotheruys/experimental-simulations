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

#this is in array format
avg1=np.array(eng.load(avg_file1)['AVGdata'][0])
avg2=np.array(eng.load(avg_file2)['AVGdata'][0])
avg3=np.array(eng.load(avg_file3)['AVGdata'][0])


#these are dicts
a1=eng.load(micCal_file1)
micCal1_d={}
micCal1_d['F_mics']=np.array(a1['micCal']['F_mics'])
micCal1_d['f_oct']=np.array(a1['micCal']['f_oct'])

a2=eng.load(micCal_file2)
micCal2_d={}
micCal2_d['F_mics']=np.array(a2['micCal']['F_mics'])
micCal2_d['f_oct']=np.array(a2['micCal']['f_oct'])

a3=eng.load(micCal_file3)
micCal3_d={}
micCal3_d['F_mics']=np.array(a3['micCal']['F_mics'])
micCal3_d['f_oct']=np.array(a3['micCal']['f_oct'])

mic_cols=['mic1','mic2','mic3','mic4','mic5','mic6','oct']
def pack_mic(data):
    dummy=data.copy()
    arr=dummy['F_mics']
    arr=arr.transpose()
    arr=np.append(arr,np.reshape(dummy['f_oct'],(len(arr),1)),axis=1)
    df=pd.DataFrame(arr,columns=mic_cols)
    return df   

micCal1=pack_mic(micCal1_d)    
micCal2=pack_mic(micCal1_d)    
micCal3=pack_mic(micCal1_d)       
    


b1=eng.load(opp_file1)['opp'][0]
b2=eng.load(opp_file2)['opp'][0]
b3=eng.load(opp_file3)['opp'][0]
keys=list(b1.keys())
opp1_d={}
opp2_d={}
opp3_d={}
for i in range(len(keys)):
    opp1_d[keys[i]]=np.array(b1[keys[i]]).flatten()
    opp2_d[keys[i]]=np.array(b2[keys[i]]).flatten()
    opp3_d[keys[i]]=np.array(b3[keys[i]]).flatten()

#pack dict into dataframe
def pack_opp(data):
    dummy=data.copy()
    df=pd.DataFrame.from_dict(dummy)
    return df
opp1=pack_opp(opp1_d)
opp2=pack_opp(opp2_d)
opp3=pack_opp(opp3_d)

#these are arrays  
w1=np.array(eng.load(w_file1)['w'])
w2=np.array(eng.load(w_file2)['w'])
w3=np.array(eng.load(w_file3)['w'])
    



    
    
    
#df1=pd.DataFrame.from_dict(opp1,dtype=float)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    