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
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

file1 = os.path.join(current_dir, 'bal_sorted1.csv')
file2 = os.path.join(current_dir, 'bal_sorted2.csv')
file3 = os.path.join(current_dir, 'bal_sorted3.csv')


bal_sorted1=pd.read_csv(file1)
bal_sorted2=pd.read_csv(file2)
bal_sorted3=pd.read_csv(file3)

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

#%%

#inp_lst=[(40,1.6),(40,1.8),(40,3.5),(20,1.6),(10,1.6),(40,17),(20,17),(10,17)]
def CL_plot(data,inp_lst):
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
#%%
def CLCD_plot(data,inp_lst):
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
#%%  
def CM_plot(data,inp_lst):
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
#%%
def CM_delta(dat1,dat2,dat3,inp_lst,AoA):
    cmd1=[]
    cmd2=[]
    cmd3=[]
    delta=np.array([-15,0,15])
   
    lab=[]
    for i in range(len(inp_lst)):
        dummy1=get_set(dat1,inp_lst[i][0],inp_lst[i][1])
        group1=dummy1.groupby('rounded_AoA')
        dummy2=get_set(dat2,inp_lst[i][0],inp_lst[i][1])
        group2=dummy2.groupby('rounded_AoA')
        dummy3=get_set(dat3,inp_lst[i][0],inp_lst[i][1])
        group3=dummy3.groupby('rounded_AoA')
      
        
        cmd1.append(float(group1.get_group(AoA)['CMpitch']))
        cmd2.append(float(group2.get_group(AoA)['CMpitch']))
        cmd3.append(float(group3.get_group(AoA)['CMpitch']))
        # lab.append('V=' +str(round(inp_lst[i][0],1))+ '  J= '+str(round(inp_lst[i][1],1))\
        #             +'    AoA='+str(AoA))
        lab.append('J= '+str(round(inp_lst[i][1],1)))
               
            
    stack=np.stack((np.array(cmd1),np.array(cmd2),np.array(cmd3)))
    
    delta_fit=np.linspace(-20,20,100)
    fig,ax=plt.subplots()
    for i in range(len(lab)):
        curve_fit=np.poly1d(np.polyfit(delta,stack[:,i],1))
        ax.scatter(delta,stack[:,i])
        ax.plot(delta_fit,curve_fit(delta_fit),'-.',label=lab[i])
        ax.legend()
    ax.grid()
    ax.set_ylabel(r'$C_{M} $')
    ax.set_xlabel(r'$\delta [deg]$')  
    ax.set_title('V= '+str( inp_lst[0][0] )+' m/s,  ' + r'$\alpha = $' + str(AoA)+'[deg]')
    return stack

    
#%%
CL_plot(bal_sorted2,[(40,1.6),(40,1.8),(40,3.5),(40,17)])

CLCD_plot(bal_sorted2,[(40,1.6),(40,1.8),(40,3.5),(40,17)])

CM_plot(bal_sorted2,[(40,1.6),(40,1.8),(40,3.5),(40,17)])

CM_delta(bal_sorted1,bal_sorted2,bal_sorted3,[(40,1.6),(40,1.8),(40,3.5),(40,17)],7)
   



# #plots for delta=-15
# CL_plot(bal_sorted1)
# CM_plot(bal_sorted1)
# CLCD_plot(bal_sorted1)

# #plots for delta=0
# CL_plot(bal_sorted2)
# CM_plot(bal_sorted2)
# CLCD_plot(bal_sorted2)    
    
# #plots for delta=15
# CL_plot(bal_sorted3)
# CM_plot(bal_sorted3)
# CLCD_plot(bal_sorted3)