import pyfits
import numpy as np
import math as m
import sys
import matplotlib.pyplot as plt
import pdb

#Get list of table files
fluxlist = sys.argv[1]

#Make the figure
fig = plt.figure()
plt.grid(True)
plt.xlabel('Time')
plt.ylabel('Relative Flux')
plt.title('Lightcurve of Reference Stars')

ctr = 0

for tablefile in open(fluxlist):
    ctr += 1
    fig.clf()

    #Open file
    tablefile = tablefile.rstrip('\n')
    data = np.loadtxt(tablefile)
    
    #Get the information
    fluxdata = data[:,1]                    #fluxdata holds all raw data
    fluxerrordata = data[:,2]
    time = data[:,0]

    #Normalize flux and ignore outliers
    flux = fluxdata[np.where(fluxdata!=0)]  #flux used for average 
    flux = flux[287:]                       #flux ignores beginning exposures (no outliers)
    fluxerror = fluxerrordata[287:]         #fluxerror ignores beginning images 
    average = np.mean(flux)    #average ignores beginning exposures
    n = flux.shape[0]
    sigma = m.sqrt( np.sum((flux-average)**2) / (n-1))
    normfluxdata = fluxdata/average          #normfluxdata normalizes ALL exposures
    normfluxerrordata = fluxerrordata/average #normfluxerrordata normalizes ALL exposures
    
    #Plot data
    plt.errorbar(time, normfluxdata, yerr = normfluxerrordata, fmt = 'r.')
    fig.savefig('exo_curves' + str(ctr) + '.pdf', bbox_inches='tight', dpi=fig.dpi)
    
    #Make files containing time, flux, and error
    #For the science target, we won't normalize to average
    if (ctr == 11):
        #Scrap non-zero outliers more that 2 sigma away for non-beginning exposures
        tempflux = fluxdata[287:]                 #no beginning exposures, HAS outliers
        tempflux[np.where(tempflux < (average - 4*(sigma)))] = 0.0
        tempflux[np.where(tempflux > (average + 4*(sigma)))] = 0.0
        fluxerror[np.where(tempflux < (average - 4*(sigma)))] = 0.0
        fluxerror[np.where(tempflux > (average + 4*(sigma)))] = 0.0
    
        #Write average fluxes to file
        filename = ('exo_fluxdata' + str(ctr) + '.txt')
        finalflux = np.concatenate((fluxdata[:287], tempflux), axis = 0) #flux with beginning
        finalfluxerror = np.concatenate((fluxerrordata[:287], fluxerror), axis=0)        
        np.savetxt(filename, np.column_stack((time, finalflux, finalfluxerror)), fmt='%f') 
    #For the others, we will normalize to average
    else:
        #Scrap non-zero outliers more that 2 sigma away for non-beginning exposures
        tempflux = normfluxdata[287:]            #ignores first exposures
        tempfluxerror = normfluxerrordata[287:]   #ignores first exposures
        tempflux[np.where( tempflux < ((average - 4*sigma)/average) )] = 0.0
        tempflux[np.where( tempflux > ((average + 4*sigma)/average) )] = 0.0
        tempfluxerror[np.where( tempflux < ((average - 4*sigma)/average) )] = 0.0
        tempfluxerror[np.where( tempflux > ((average + 4*sigma)/average) )] = 0.0
        
        #Write average fluxes to file
        filename = ('exo_fluxdata' + str(ctr) + '.txt')
        normflux = np.concatenate((normfluxdata[:287], tempflux), axis = 0)
        normfluxerror = np.concatenate((normfluxerrordata[:287], tempfluxerror), axis = 0)
        np.savetxt(filename, np.column_stack((time, normflux, normfluxerror)), fmt='%f')









#data2 = np.loadtxt(referencestarfile2)
#data3 = np.loadtxt(referencestarfile3)
#data4 = np.loadtxt(referencestarfile4)
#data5 = np.loadtxt(referencestarfile5)
#data6 = np.loadtxt(referencestarfile6)
#data7 = np.loadtxt(referencestarfile7)
#data8 = np.loadtxt(referencestarfile8)
#data9 = np.loadtxt(referencestarfile9)
#data10 = np.loadtxt(referencestarfile10)
#data11 = np.loadtxt(referencestarfile11)
#
##--------------------------------------
#fluxdata1 = data1[:,1]
#fluxerrordata1 = data1[:,2]
#time1 = data1[:,0]
#
#fluxdata1 = fluxdata1/np.mean(fluxdata1)
#
#fluxerrordata1 = fluxerrordata1/np.mean(fluxerrordata1)
##--------------------------------------
#fluxdata2 = data2[:,1]
#fluxerrordata2 = data2[:,2]
#time2 = data2[:,0]
#
#fluxdata2 = fluxdata2/np.mean(fluxdata2)
#fluxerrordata2 = fluxerrordata2/np.mean(fluxerrordata2)
#
##-------------------------------------
#fluxdata3 = data3[:,1]
#fluxerrordata3 = data3[:,2]
#time3 = data3[:,0]
#
#fluxdata3 = fluxdata3/np.mean(fluxdata3)
#fluxerrordata3 = fluxerrordata3/np.mean(fluxerrordata3)
##-------------------------------------
#fluxdata4 = data4[:,1]
#fluxerrordata4 = data4[:,2]
#time4 = data4[:,0]
#
#fluxdata4 = fluxdata4/np.mean(fluxdata4)
#fluxerrordata4 = fluxerrordata4/np.mean(fluxerrordata4)
##-------------------------------------
#fluxdata5 = data5[:,1]
#fluxerrordata5 = data5[:,2]
#time5 = data5[:,0]
#
#fluxdata5 = fluxdata5/np.mean(fluxdata5)
#fluxerrordata5 = fluxerrordata5/np.mean(fluxerrordata5)
##--------------------------------------
#fluxdata6 = data6[:,1]
#fluxerrordata6 = data6[:,2]
#time6 = data6[:,0]
#
#fluxdata6 = fluxdata6/np.mean(fluxdata6)
#fluxerrordata6 = fluxerrordata6/np.mean(fluxerrordata6)
##--------------------------------------
#fluxdata7 = data7[:,1]
#fluxerrordata7 = data7[:,2]
#time7 = data7[:,0]
#
#fluxdata7 = fluxdata7/np.mean(fluxdata7)
#fluxerrordata7 = fluxerrordata7/np.mean(fluxdata7)
##---------------------------------------
#fluxdata8 = data8[:,1]
#fluxerrordata8 = data8[:,2]
#time8 = data8[:,0]
#
#fluxdata8 = fluxdata8/np.mean(fluxdata8)
#fluxerrordata8 = fluxerrordata8/np.mean(fluxerrordata8)
##---------------------------------------
#fluxdata9 = data9[:,1]
#fluxerrordata9 = data9[:,2]
#time9 = data9[:,0]
#
#fluxdata9 = fluxdata9/np.mean(fluxdata9)
#fluxerrordata9 = fluxerrordata9/np.mean(fluxerrordata9)
##--------------------------------------
#fluxdata10 = data10[:,1]
#fluxerrordata10 = data10[:,2]
#time10 = data10[:,0]
#
#fluxdata10 = fluxdata10/np.mean(fluxdata10)
#fluxerrordata10 = fluxerrordata10/np.mean(fluxerrordata10)
##-------------------------------------
#plt.plot(time2, fluxdata2, 'ro')
#plt.plot(time3, fluxdata3, 'ro')
#plt.plot(time4, fluxdata4, 'ro')
#plt.plot(time5, fluxdata5, 'ro')
#plt.plot(time6, fluxdata6, 'ro')
#plt.plot(time7, fluxdata7, 'ro')
#plt.plot(time8, fluxdata8, 'ro')
#plt.plot(time9, fluxdata9, 'ro')
#plt.plot(time10, fluxdata10, 'ro')
#plt.plot(time11, fluxdata11, 'ro')
#
##plt.errorbar(fluxerrordata1)
