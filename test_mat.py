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


dummy=[ne,nv,n_prop,na]

# layer_1=list(itertools.product(na,ne))
# layer_2=list(nv,layer_1)
comb=list(itertools.product(*dummy))
mat=np.zeros((len(comb),4))
for i in range(4):
    for j in range(len(comb)):
        mat[j,i]=comb[j][i]
mat=pd.DataFrame(mat,columns=['Elevator','Tunnel velocity','propeller setting','AoA'])