# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
import pickle
from numpy import linalg as LA

#os.chdir('Desktop/covid/heatmap')

f = open('VarRefs/sev_discrete_to_real.pickle','rb')
sevdic=pickle.load(f)
f.close()


f = open('VarRefs/long_discrete_to_real.pickle','rb')
longdic=pickle.load(f)
f.close()

def pnummap(df,var1,var2):
    data = df[[var1,var2]]
    xd = np.array(data)
    bar1 = list(np.unique(df[var1]))
    bar2 = list(np.unique(df[var2]))
    if -999 in bar1:
        bar1.remove(-999)
    if -999 in bar2:
        bar2.remove(-999)
    
    pdata = np.zeros((len(bar1),len(bar2))).astype('int')
    

    for i in range(len(xd)):
        r = xd[i,:]
        if (r[1] != -999) and (r[0] != -999):
            pdata[list(bar1).index(r[0]),list(bar2).index(r[1])] += 1
    
    
#     label1 = []
#     for i in range(len(bar1)):
#         if np.min(bar1)==1:
#             value = bar1[i]-1
#         else:
#             value = bar1[i]
#         if var2 == 'Long Covid':
#             label1.append(longdic[var1][value])
#         elif var2 == 'Severity':
#             label1.append(sevdic[var1][value])
    
#     if var2 == 'Long Covid':
#         label2 = ['Non Long COVID','Long COVID']
#     if var2 == 'Severity':
#         label2 = ['Uninfected','Mild','Moderate','Severe','Dead']
#         pdata = pdata[:,[4,3,0,1,2]]
        
#     label1 = pd.Index(label1)
#     label2 = pd.Index(label2)
#     label1.name = var1
#     label2.name = var2
    
    #pdata = pdata.T/pdata.sum(axis=1).T
    pdata=pdata
    
    return pdata


var1 ='Albumin (LOWEST value)' 

longlist=[
'Runny nose (Rhinorrhea) ?',
#'Dialysis ?',
'Shortness of breath (Dyspnea) ?',
'Chest pain ?',
#'Severity of COPD:',
'Joint pain (Arthralgia) ?' ,
'Diabetes ?',
'Electronic cigarettes?',
'Age']



sevlist=[
'Joint pain (Arthralgia) ? (follow up)',
'Joint pain (Arthralgia) ?',
'Leg swelling (Edema) (follow up)',
'Leg swelling (Edema) ?',
'BMI:',
'C-reactive protein (CRP) (HIGHEST value)',
'Acute Respiratory Distress Syndrome (ARDS)?',
'Albumin (LOWEST value)' ,
'Electronic cigarettes?',
'Age']

'''
severity:
relevant: ['Acute Respiratory Distress Syndrome (ARDS)?','Albumin (LOWEST value)' ,'C-reactive protein (CRP) (HIGHEST value)','Age','BMI:']  
irrelevant: ['Joint pain (Arthralgia) ?']
'''


'''
long-covid:
relevant: ['Shortness of breath (Dyspnea) ?','Joint pain (Arthralgia) ?' , 'Runny nose (Rhinorrhea) ?','Age', 'Chest pain ?']
irrelevant: ['Diabetes ?']
'''



#pnummap(sevdf,'ALT:','Severity')#'Long Covid')


#pnummap(longdf,'Chronic kidney disease ?','Long Covid')

