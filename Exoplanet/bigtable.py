import pdb
import numpy as np
import math as m
import sys

#Read in the tables for each star
referencestarfile2 = sys.argv[1]
referencestarfile3 = sys.argv[2]
referencestarfile4 = sys.argv[3]
referencestarfile5 = sys.argv[4]
referencestarfile6 = sys.argv[5]
referencestarfile7 = sys.argv[6]
referencestarfile8 = sys.argv[7]
referencestarfile11 = sys.argv[8]

#Import the data into arrays.
#We will only work with the first 3 columns
#These are the times, fluxes, and flux errors
data2 = np.loadtxt(referencestarfile2)
data3 = np.loadtxt(referencestarfile3)
data4 = np.loadtxt(referencestarfile4)
data5 = np.loadtxt(referencestarfile5)
data6 = np.loadtxt(referencestarfile6)
data7 = np.loadtxt(referencestarfile7)
data8 = np.loadtxt(referencestarfile8)
data11 = np.loadtxt(referencestarfile11)

#The following is storing the relevent data into arrays
#--------------------------------------
fluxdata2 = data2[:,1]
fluxerrordata2 = data2[:,2]
time2 = data2[:,0]
#-------------------------------------
fluxdata3 = data3[:,1]
fluxerrordata3 = data3[:,2]
time3 = data3[:,0]
#-------------------------------------
fluxdata4 = data4[:,1]
fluxerrordata4 = data4[:,2]
time4 = data4[:,0]
#-------------------------------------
fluxdata5 = data5[:,1]
fluxerrordata5 = data5[:,2]
time5 = data5[:,0]
#--------------------------------------
fluxdata6 = data6[:,1]
fluxerrordata6 = data6[:,2]
time6 = data6[:,0]
#--------------------------------------
fluxdata7 = data7[:,1]
fluxerrordata7 = data7[:,2]
time7 = data7[:,0]
#---------------------------------------
fluxdata8 = data8[:,1]
fluxerrordata8 = data8[:,2]
time8 = data8[:,0]
#-------------------------------------
fluxdata11 = data11[:,1]
fluxerrordata11 = data11[:,2]
time11 = data11[:,0]
#------------------------------------

#Concatanate all of the fluxes and their errors
fluxdata = np.column_stack([fluxdata2, fluxdata3, fluxdata4, fluxdata5, fluxdata6, fluxdata7, fluxdata8])
fluxerrordata = np.column_stack([fluxerrordata2, fluxerrordata3, fluxerrordata4, fluxerrordata5, fluxerrordata6, fluxerrordata7, fluxerrordata8])

#Initialize some variables
mu_ref = np.zeros(fluxdata.shape[0])
sigma_ref = np.zeros(fluxdata.shape[0])
ratio = np.zeros(fluxdata.shape[0])
sigma_ratio = np.zeros(fluxdata.shape[0])

#Calculate average reference star flux for each exposure and its error
for i in range(0, fluxerrordata.shape[0]):     #i = image index
    denominator = 0
    numerator = 0
    for n in range(0, fluxerrordata.shape[1]): #n = star index
        #Ignore certain exposures from each reference star
        if fluxerrordata[i, n] == 0:
            continue
        
        #Calculate parts of average and sigma
        numerator += fluxdata[i,n]/(fluxerrordata[i,n]**2)
        denominator += (1.0/(fluxerrordata[i, n]**2))
    
    #Actual average and error for each image
    if (numerator == 0) and (denominator == 0):     #ignore the beginning exposures
        continue
    mu_ref[i] = numerator/denominator
    sigma_ref[i] = m.sqrt(1.0/denominator)

#Get ratio between science flux and average ref star flux
#and its error
for k in range(0, mu_ref.shape[0]):
    #Ignore certain exposures from each reference star
    if (fluxdata11[k] == 0) or (mu_ref[k] == 0):
        continue
    ratio[k] = (fluxdata11[k])/(mu_ref[k])
    sigma_ratio[k] = ratio[k]*m.sqrt((fluxerrordata11[k]/fluxdata11[k])**2+(sigma_ref[k]/mu_ref[k])**2)

#Write everything to a text file
with open('exo_masterrecord.txt', 'w+') as outfile:
    for i in range(0,ratio.shape[0]):
        #pdb.set_trace()
        outfile.write(str(time11[i]) + ' ' + str(fluxdata11[i]) + ' ' + str(fluxerrordata11[0]) + ' ' + str(mu_ref[i]) + ' ' + str(ratio[i]) + ' ' + str(sigma_ratio[i]) + '\n') 
