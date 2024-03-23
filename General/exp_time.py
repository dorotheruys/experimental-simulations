#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 16:08:35 2024

@author: jackcheng
"""
#na= number of aoa setting
#n_p= number of prop speed setting underscore to not be confused with numpy as np


na=4  #na= number of aoa setting
n_p=3  #n_p= number of prop speed setting
nv=3   #nv= number of tunnel velocity setting
n_e=3  #n_e= number of elevator setting


def wind_on(na,n_p,nv,n_e):
    
    prop_onoff=15*60
    c_ele=15*60
    c_tunnel_v= 2*60
    c_alpha=25
    t_samp=7 #sampling time per point
    c_prop_set=30
    set1=na*c_alpha*n_p+n_p*c_prop_set  
    set2=set1 *nv + nv*c_tunnel_v
    set3=set2*n_e+ n_e*c_ele
    sampling_time=na*n_p*nv*n_e*t_samp
    return (set3+sampling_time)/60    #return time in minutes
    
    
    
def wind_off(na):
    
    prop_onoff=15*60
    c_ele=15*60
    c_tunnel_v= 2*60
    c_alpha=na*2+20
    t_samp=10
    prop_set=30
    
    return (na*(c_alpha-1)+prop_onoff)/60    #return time in minutes


#15+5 for tunnel prep, 10 for trimming
total_time=wind_on(na,n_p,nv,n_e)+ wind_off(na)+15+5+10
print('total time=',total_time,'minutes')


# Copies of old, redundant files from testmatrix.py
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