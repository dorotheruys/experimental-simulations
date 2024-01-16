#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:57:23 2024

@author: jackcheng
"""

import numpy as np
import itertools
import pandas as pd


na=[-5,7,12,14]
ne=[1,2,3]
nv=[10,20,40]
n_prop=[0,1,2]

def get_test_matrix():

    dummy=[ne,nv,n_prop,na]
    comb=list(itertools.product(*dummy))
    mat=np.zeros((len(comb),4))
    for i in range(4):
        for j in range(len(comb)):
            mat[j,i]=comb[j][i]
    mat=pd.DataFrame(mat,columns=['Elevator','Tunnel velocity','propeller setting','AoA'])
    return mat



#calculates time for wind on 
def wind_on(na,n_p,nv,n_e):
    a=len(na)
    b=len(n_p)
    c=len(nv)
    d=len(n_e)
    prop_onoff=15*60
    c_ele=15*60
    c_tunnel_v= 2*60
    c_alpha=25
    t_samp=7 #sampling time per point
    c_prop_set=30
    set1=a*c_alpha*b+b*c_prop_set  
    set2=set1 *c + c*c_tunnel_v
    set3=set2*d+ d*c_ele
    sampling_time=a*b*c*d*t_samp
    return (set3+sampling_time)/60    #return time in minutes
    
    
    
def wind_off(na):
    a=len(na)
    prop_onoff=15*60
    c_ele=15*60
    c_tunnel_v= 2*60
    c_alpha=a*2+20
    t_samp=10
    prop_set=30
    
    return (a*(c_alpha-1)+prop_onoff)/60    #return time in minutes


#15+5 for tunnel prep, 10 for trimming
total_time=wind_on(na,n_prop,nv,ne)+ wind_off(na)+15+5+10
print('total time=',total_time,'minutes')