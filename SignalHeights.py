#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 19:00:33 2019

@author: margarita
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import glob

#note: will need to include also height for standard...
#this is the file where everything gets written into
ofile=open("signalheights.csv","w+")
ofile.write('File name, standard pp-height b.n. [au], standard peak width b.n.[G], signal pp-height [au], signal peak width [G], normalized signal pp-height [au], normalized signal peak width [G]\n')
ofile.write('name, Mpph, MppwG, Spph, SppwG, NSpph, NSppwG\n')

standard = 'yes' #was a standard used in the measurements?
############# STANDARD DATA ####################
#set the values between which the magnetic field corresponding to the standard peak
# is expected
high =  3542.
low = 3510.
gstand = 1.9800 #gfactor of the standard
gstandB = 3540. #Bfield corresponding to the g-factor in Gauss
#TODO: find the correct value

#set the values between which the magnetic field is expected to be for the signal
s_high = 3501. 
s_low = 3497.8

color1 = '#720000'
color2 = '#214f21'

for file in glob.glob("*.asc"):
    #use to look at only one file
    #if file != "ZMC_16.asc":
     #  continue
    if standard == 'yes':
    ##################DEAL WITH THE STANDARD FIRST#########################
    #find the maximum between Magnetic field values of high and low
    #those are the spectra files
        data = pd.read_csv(file, skiprows=2, sep='\t')
        #find the index of the bounds
        indlow = data[data['X [G]'].gt(low)].index[0] 
        indhigh = data[data['X [G]'].gt(high)].index[0] 
        #crop dataset to the bounds
        crdata = data[indlow:indhigh]
        
        #find max of the intensity value
        maxI= crdata['Intensity'].max()
        #find the corresponding magnetic field value
        maxB = crdata.loc[crdata['Intensity'].idxmax(),'X [G]']
    
        #find min of the intensity value
        minI= crdata['Intensity'].min()
        #find the corresponding magnetic field value
        minB = crdata.loc[crdata['Intensity'].idxmin(),'X [G]']
        #print(minI)
        #print(minB)
    
        #calculate the pp signal height
        pph = abs(maxI-minI)
        #calculate the pp signal width in Gauss and mT
        ppwG = minB-maxB
        ppwmT = 0.1*(ppwG)
        #calculate the location of the signal in Gauss
        #TODO
        
        #finding the center of the standard
        standC=(maxB+minB)/2
        #shifting everything to the standard g-value
        shift = standC - gstandB
        data_transp = pd.DataFrame()
        data_transp['X [G]'] = data['X [G]'] - shift
        data_transp['Intensity'] = data['Intensity']
        
        #define the hight of the standard to be 1 and scale everything based on this
        data_scaled = pd.DataFrame()
        data_scaled['X [G]'] = data_transp['X [G]']
        data_scaled['Intensity'] = data_transp['Intensity']*(1/pph)*1000000
        #print(data_scaled[data['Intensity']==maxI])
        #print(data_scaled[data['Intensity']==minI])
        
        
        plt.plot(data['X [G]'],data['Intensity'], 'k')
        #plt.vlines([minB,maxB,high,low],-1500000,1000000)
        plt.plot(data_transp['X [G]'],data_transp['Intensity'],color=color1)
        
        plt.plot(data_scaled['X [G]'],data_scaled['Intensity'],color=color2)
        #plt.vlines([s_high,s_low],-1500000,1000000)
        #plt.show()
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        #plt.title(filename)
        plt.savefig(file[:-4]+'-scaling.svg')
        plt.show()
        
        
        workingdata = data_scaled        
        
    elif standard == 'no':
        print('We will continue without a standard')
        workingdata = pd.read_csv(file, skiprows=2, sep='\t')
    
    ####################### SIGNAL ANALYSIS ##############################
        
    #now find the index of the location of the peaks with and without normalization
    def peakHeights(dataframe):
        
        s_indlow = dataframe[dataframe['X [G]'].gt(s_low)].index[0] 
        s_indhigh = dataframe[dataframe['X [G]'].gt(s_high)].index[0] 
        #print(dataframe)
        #crop dataset to the bounds
        crdataframe = dataframe[s_indlow:s_indhigh]
        s_maxI= crdataframe['Intensity'].max()
        #find max of the intensity value
        #find the corresponding magnetic field value
        s_maxB = crdataframe.loc[crdataframe['Intensity'].idxmax(),'X [G]']
        #find min of the intensity value
        s_minI= crdataframe['Intensity'].min()
        #find the corresponding magnetic field value
        s_minB = crdataframe.loc[crdataframe['Intensity'].idxmin(),'X [G]']
        #print(s_minI,s_maxI)
        #print(s_minB,s_maxB)
        #plt.plot(crdataframe['X [G]'],crdataframe['Intensity'])
        #plt.vlines([s_minB,s_maxB],-1500000,1000000)
        
        #calculate the pp signal height
        s_pph = abs(s_maxI-s_minI)
        #calculate the pp signal width in Gauss and mT
        s_ppwG = s_minB-s_maxB
        s_ppwmT = 0.1*(ppwG)
        return s_pph,s_ppwG,s_ppwmT
    
    s_pphN,s_ppwGN,s_ppwmTN=peakHeights(workingdata)
    s_pph,s_ppwG,s_ppwmT=peakHeights(data_transp)
    
    ofile.write('{:},{:},{:},{:},{:},{:},{:}\n'.format(file,pph,ppwG,s_pph,s_ppwG,s_pphN,s_ppwGN))
    
    print(file,pph,ppwG)

ofile.close()




