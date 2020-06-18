#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:18:51 2019

@author: margarita
"""
'''
what will this code do?
file 0 is the background
file 3 is the measurement
1) import both files
2) use the normalized ppheight
3) subtract ppheight 0 from ppheight 3
4) assign a dose to each filename 1-6:0.2, etc up to 37-42:5Gy
5) output: name,dose,ppheightdiff
6) plot dose-ppheigt, dose-pp-heightdiff
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import glob
import os
from scipy.optimize import curve_fit

ofile=open("cnlanalysis.csv","w+")
ofile.write('Sample name, Dose [Gy], p-p heught [a.u], Signal height Difference [a.u.]\n')
#ofile.write('name, Mpph, MppwG, Spph, SppwG, NSpph, NSppwG\n')
ofold = "graphs"
if not os.path.isdir(ofold):
    os.mkdir(ofold)

#which file is the background and where is the data located?
background = "Outfiles/signalheights_0.csv"
file1 = "Outfiles/signalheights_1.csv"
file2 = "Outfiles/signalheights_2.csv"
file3 = "Outfiles/signalheights_3.csv"
file4 = "Outfiles/signalheights_4.csv"
file5 = "Outfiles/signalheights_5.csv"
densityfile = "density.csv"

allfiles=[background,file1,file2,file3,file4,file5]
#datafiles = ["signalheights_3.csv","signalheights_4.csv"]
#measdata = []
df_density = pd.read_csv(densityfile, sep=',',index_col='samplenr')
#in mg/mm^3
df_density.sort_index(inplace=True)
densitycols = df_density.columns
#df_background = pd.read_csv(backgroundfile, skiprows=1, sep=',')

#df_irradiated = pd.read_csv(datafile3, skiprows=1, sep=',')
#set the error for the intensity measurements, will have to be independently estimated
#deltaI = 0.01
deltaI=0.0
df_master=pd.DataFrame()
#in Gy
dose= [0.2,0.2,0.2,0.2,0.2,0.2,0.5,0.5,0.5,0.5,0.5,0.5,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,2.0,2.0,2.0,2.0,2.0,2.0,3.0,3.0,3.0,3.0,3.0,3.0,5.0,5.0,5.0,5.0,5.0,5.0]
df_master['Dose'] = dose
df_master.index=df_master.index+1

alldf=[]
colcount=1
f=len(allfiles)-len(allfiles)
print(f) #counter for the filenames in the masterfile
for file in allfiles:
    df_data = pd.read_csv(file, skiprows=1, sep=',')
    Samplecolumn=[]
    for name in df_data['name']:
        #print(name)
        ind = name.find("ZMC_")
        #print(name[ind+4], name[ind+5])
        if name[ind+5]=='_':
            samplenr = int(float(name[ind+4]))
        else:
            samplenr = int(float(name[ind+4]+name[ind+5]))
        #print(samplenr)
        Samplecolumn.append(samplenr)
    #print(Samplecolumn)
    df_data['sample']=Samplecolumn
    df_data.set_index('sample',inplace=True)
    df_data.sort_index(inplace=True)
    i=df_data.shape[0]+1 #set index to row after last filled 
    while df_data.shape[0] < 42:
        df_data.loc[i] = [None,None,None,None,None,None,None]
        i=i+1
    
    #print(df_density[densitycols[colcount]])
    #print(df_data[' NSpph'])
    df_data['I_dn']=df_data[' NSpph']/df_density[densitycols[colcount]]
    df_data['deltaI_dn']=np.sqrt((deltaI/df_data[' NSpph'])**2 + (df_density[densitycols[colcount+1]]/df_density[densitycols[colcount]])**2)*df_data['I_dn']
    
    #put all dataframes in a list
    #alldf.append(pd.DataFrame(df_data))
    
    df_master['I_dn'+str(f)]=df_data['I_dn']
    df_master['deltaI_dn'+str(f)]=df_data['deltaI_dn']
    if f==0:
       f=f+1
       
    else:
        df_master['I_dn-backg'+str(f)]=df_master['I_dn'+str(f)]-df_master['I_dn0']
        df_master['deltaI_dn-backg'+str(f)]=df_master['deltaI_dn'+str(f)]+df_master['deltaI_dn0']
        f=f+1

    colcount=colcount+2
    
    #print(df_data.shape,df_data.size)
df_master['nIaverage'] = df_master[['I_dn-backg{:}'.format(i) for i in range(1,6,1)]].mean(skipna=True, axis=1)
df_master['nIstd'] = df_master[['I_dn-backg{:}'.format(i) for i in range(1,6,1)]].std(skipna=True, axis=1)

#dump everything into an output file
df_master.to_csv(r'G3results.csv', index = False)

'''
#uncomment to do plots on the fly
#Onwards to the plotting
plt.figure(figsize=(5,4))
plt.errorbar(df_master['Dose'],df_master['I_dn-backg2'],yerr=df_master['deltaI_dn-backg2'],ls=' ',marker='o',ms=0.1,capsize=4.)
plt.xlabel('Dose [Gy]')
plt.ylabel('normalized pp-height [a.u.]')
plt.ticklabel_format(style='sci', axis='y', scilimits=(6,6))
plt.title('Normalized peak-to-peak height difference \n (Measurement 2)')
plt.xlim(0.18,1.2)
plt.ylim(-1,1000000)
plt.savefig('meas2allerrors.png',dpi=600)
plt.show()

plt.plot(df_master['Dose'],df_master['I_dn-backg1'],'o')
plt.plot(df_master['Dose'],df_master['I_dn-backg2'],'o')
plt.plot(df_master['Dose'],df_master['I_dn-backg3'],'o')
plt.plot(df_master['Dose'],df_master['I_dn-backg4'],'o')
plt.plot(df_master['Dose'],df_master['I_dn-backg5'],'o')
plt.xlabel('Dose [Gy]')
plt.ylabel('normalized pp-height difference [a.u.]')
plt.title('Normalized peak-to-peak height \n all samples, all measurment runs')
plt.ticklabel_format(style='sci', axis='y', scilimits=(6,6))
plt.savefig('allmeas.png',dpi=600)
plt.show()
'''
'''
plt.errorbar(df_master['Dose'],df_master['nIaverage'],yerr=df_master['nIstd'],ls=' ',marker='o',ms=0.1,capsize=4.)
plt.xlabel('Dose [Gy]')
plt.ylabel('normalized pp-height [a.u.]')
plt.title('Normalized peak-to-peak height \n averages of all samples')
plt.ticklabel_format(style='sci', axis='y', scilimits=(6,6))
plt.xlim(0.18,1.2)
plt.ylim(-1,1000000)
plt.savefig('allavgs.png',dpi=600)
plt.show()
'''
'''
def linear(x,m,t):
    return x*m+t

popt, pcov = curve_fit(linear,df_master.loc[[2,8,14,20,26,32,38],'Dose'],df_master.loc[[3,9,15,21,27,33,39],'nIaverage'])

plt.errorbar(df_master.loc[[2,8,14,20,26,32,38],'Dose'],df_master.loc[[3,9,15,21,27,33,39],'nIaverage'],yerr=df_master.loc[[3,9,15,21,27,33,39],'nIstd'],ls=' ',marker='o',ms=0.1,capsize=4.)
plt.xlabel('Dose [Gy]')
plt.ylabel('normalized pp-height difference [a.u.]')
plt.plot(df_master.loc[[2,8,14,20,26,32,38],'Dose'], linear(df_master.loc[[2,8,14,20,26,32,38],'Dose'],popt[0],popt[1]),'-')
plt.title('Normalized peak-to-peak height averages of all runs \n (one sample for each dose))')
plt.ticklabel_format(style='sci', axis='y', scilimits=(6,6))
#plt.xlim(0.18,1.2)
#plt.ylim(-1,1000000)
plt.savefig('sample2.png',dpi=600)
plt.show()
'''
##################################################
dosegroups=df_master.groupby('Dose')
averages=[]
doses=[]
stdevs=[]
df_analysis=pd.DataFrame()

for d in np.unique(df_master['Dose']):
    doses.append(d)
    av = (dosegroups.get_group(d)['I_dn-backg3'].mean())
    std = (dosegroups.get_group(d)['I_dn-backg3'].std())
    averages.append(av)
    stdevs.append(std)
    
df_analysis['Dose']=doses
df_analysis['Average']=averages
df_analysis['STDEV']=stdevs  
#df_analysis.to_csv(r'G3analysis.csv', index = False) 

averages=np.array(averages)
doses=np.array(doses)
stdevs=np.array(stdevs)
''''
popt, pcov = curve_fit(linear,doses,averages)
plt.errorbar(doses,averages,yerr=stdevs,ls=' ',marker='o',ms=0.1,capsize=4.)
plt.xlabel('Dose [Gy]')
plt.ylabel('normalized pp-height difference [a.u.]')
plt.plot(doses, linear(doses,popt[0],popt[1]),'-')
plt.title('Normalized peak-to-peak height averages one runs \n all samples (run 3)')
plt.ticklabel_format(style='sci', axis='y', scilimits=(6,6))
#plt.xlim(0.18,1.2)
#plt.ylim(-1,1000000)
plt.savefig('run3avgs.png',dpi=600)
plt.show()
'''
