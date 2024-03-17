#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 17:49:32 2024

@author: jackcheng
"""

import scipy as sp
import numpy as np
import pandas as pd

import math
import matplotlib.pyplot as plt




bal_soted1=pd.read_csv('Sort_data/bal_sorted1.csv')
bal_soted2=pd.read_csv('Sort_data/bal_sorted2.csv')
bal_soted3=pd.read_csv('Sort_data/bal_sorted3.csv')

colors=['b','g','c','r','k','m','tab:orange','grey']

def get_set(data, vel,prop):
    if prop=='off':
        prop=17
        group1=data.groupby('rounded_J')
        layer1=group1.get_group(prop)    
        
        group2=layer1.groupby('rounded_v')
        layer2=group2.get_group(vel)
    else:

        group1=data.groupby('rounded_v')
        layer1=group1.get_group(vel)
        
        group2=layer1.groupby('rounded_J')
        layer2=group2.get_group(prop)    
        
    return layer2.sort_values(by='AoA')


inp_lst=[(40,1.6),(40,1.8),(40,3.5),(20,1.6),(10,1.6),(40,17),(20,17),(10,17)]
def CL_plot(data):
    fig,ax=plt.subplots()
    #this is linspace for curve fitting
    alpha=np.linspace(-5,25,26)
    for i in range(len(inp_lst)):
        dat=get_set(data,inp_lst[i][0],inp_lst[i][1])
        #polynomial data fit ## order 2
        curve_fit=np.poly1d(np.polyfit(dat['AoA'],dat['CL'],2))
        lab='V='+str(round(np.mean(dat['V']))) +'  , J=' +str(round(np.mean(dat['J_M1']),1))
        #ax.plot(dat['AoA'],dat['CL'],label=lab,color=colors[i])
        ax.plot(alpha,curve_fit(alpha),'-.',color=colors[i],label=lab)
        ax.scatter(dat['AoA'],dat['CL'],color=colors[i])
        ax.legend()
    ax.grid()
    ax.set_ylabel('CL')
    ax.set_xlabel('AoA')
   
def CLCD_plot(data):
    fig,ax=plt.subplots()
    cl=np.linspace(-1,1.7,50)
    for i in range(len(inp_lst)):
        dat=get_set(data,inp_lst[i][0],inp_lst[i][1])
        #polynomial data fit ## order 2
        curve_fit=np.poly1d(np.polyfit(dat['CL'],dat['CD'],2))
        lab='V='+str(round(np.mean(dat['V']))) +'  , J=' +str(round(np.mean(dat['J_M1']),1))
        #ax.plot(dat['CD'],dat['CL'],label=lab,color=colors[i])
        ax.plot(curve_fit(cl),cl,'-.',color=colors[i],label=lab)
        ax.scatter(dat['CD'],dat['CL'],color=colors[i])
        ax.legend()
    ax.grid()
    ax.set_ylabel('CL')
    ax.set_xlabel('CD')  
    
def CM_plot(data):
    fig,ax=plt.subplots()
    alpha=np.linspace(-5,20,26)
    for i in range(len(inp_lst)):
        dat=get_set(data,inp_lst[i][0],inp_lst[i][1])
        #polynomial data fit ##order 1
        curve_fit=np.poly1d(np.polyfit(dat['AoA'],dat['CMpitch'],1))
        lab='V='+str(round(np.mean(dat['V']))) +'  , J=' +str(round(np.mean(dat['J_M1']),1))
        #ax.plot(dat['AoA'],dat['CMpitch'],label=lab,color=colors[i])
        ax.plot(alpha,curve_fit(alpha),'-.',color=colors[i],label=lab)
        ax.scatter(dat['AoA'],dat['CMpitch'],color=colors[i])
        ax.legend()
    ax.grid()
    ax.set_ylabel('CM')
    ax.set_xlabel('AoA')
     
CL_plot(bal_sorted3)
CM_plot(bal_sorted3)
CLCD_plot(bal_sorted3)