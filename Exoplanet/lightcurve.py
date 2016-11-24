import pdb
import numpy as np
import math as m
import sys
import matplotlib.pyplot as plt

#Calculate average and its error for a given data set
def Average(values, error= None):
    #No error in the values
    if (error is None):
        #Calculate the average
        mu = np.sum(values)/values.shape[0]
        
        #Calculate the error
        s = np.sum((values - mu)**2)/(values.shape[0] - 1)
        sigma = m.sqrt(s/values.shape[0])
    
    #Error in the values
    else:
        #Initialize stuff
        num = 0
        denom = 0
        
        #Caluclations
        for n in range(0, values.shape[0]):
            if values[n] == 0:  #ignore outliers
                continue
            num += values[n]/(error[n]**2)
            denom += 1.0/(error[n]**2)
        
        #Mu and Sigma 
        if (num == 0) and (denom == 0):    #in case series of outliers
            mu = 0
            sigma = 0
        elif denom == 0:                   #in case no error
            mu = num/denom
            sigma == 0                
        else:                              #if normal
            mu = num/denom
            sigma = m.sqrt(1.0/denom)
    
    return (mu, sigma)

#Gives limits (indices) of exposures used for baseline flux
def getLim(images, lowexp, upexp):
    l = np.array(np.where(images > lowexp))
    u = np.array(np.where(images < upexp))
    
    lowlim = l[0, 1]
    uplim  = u[0, -1]

    return (lowlim, uplim)
 
#Extract data from input
tablefile = sys.argv[1]
mastertable = np.loadtxt(tablefile)
exposures = mastertable[:,0]
sci_flux = mastertable[:, 1]
sci_error = mastertable[:, 2]
ratio = mastertable[:, 4]
ratio_error = mastertable[:, 5]

#Get times for exposures
ignore = np.where(sci_flux == 0)          #locations of outliers
exposures = np.delete(exposures, ignore)  #ignore outliers

#Get exposure indicies for the range of fluxes from which to calculate baseline flux
lowlimit, uplimit = getLim(exposures, 4000, 6000) #picture number for lower limit of fluxes used for baseline

#Ignore outliers and caluclate the baseline flux
sci_flux = np.delete(sci_flux, ignore)    #ignore outliers
sci_error = np.delete(sci_error, ignore)  #ignore outliers
baseline, baseline_error = Average(sci_flux[(lowlimit-1) : (uplimit+1)], sci_error[(lowlimit-1) : (uplimit+1)])

#Get ratios
ratio = np.delete(ratio, ignore)  #ignore outliers
ratio_error = np.delete(ratio_error, ignore)  #ignore outliers

#Normalize the ratio by baseline flux
flux = ratio/baseline
flux_error = np.zeros(flux.shape[0])
for i in range(0,flux.shape[0]):
    if ratio[i] == 0:
        continue
    flux_error[i] = flux[i] * np.sqrt((baseline_error/baseline)**2 + (ratio_error[i]/ratio[i])**2)

#Set up for binning
binsize = 12
times = np.zeros(((exposures.shape[0]/binsize) + 1))
times_error = np.zeros(times.shape[0])
sciencecurve = np.zeros(((flux.shape[0]/binsize) + 1))
sciencecurve_error = np.zeros(sciencecurve.shape[0])
ctr = 0             #counter for index of times array
rmLastBin = False

#Bin times and fluxes
for n in range(0, exposures.shape[0], binsize):
    #Times
    if (n + binsize)>= exposures.shape[0]:         #last exopsure has smaller bin size
        #binflux, binflux_error = Average(exposures[n:exposures.shape[0]])
        #Uncomment above line if you want the last bin
        #The line below is if you want to ignore it 
        rmLastBin = True
        continue
    else:                                          #rest of exposures have normal bin sizes
        bintime, bintime_error = Average(exposures[n:n+binsize])
    times[ctr] = bintime
    times_error[ctr] = bintime_error
   
    #Fluxes
    binflux, binflux_error = Average(flux[n:n+binsize], flux_error[n:n+binsize])
    sciencecurve[ctr] = binflux
    sciencecurve_error[ctr] = binflux_error
    
    
    ctr += 1

#Remove last bin if needed
if rmLastBin:
    times = times[:-1]
    times_error = times_error[:-1]
    sciencecurve = sciencecurve[:-1]
    sciencecurve_error = sciencecurve_error[:-1]

#Plot our light curve
fig = plt.figure()
plt.grid(True)
plt.xlabel('Time (s)')
plt.ylabel('Relative flux')
plt.title('Lightcurve for HD 209458')
plt.errorbar(x = times, y = sciencecurve, xerr = times_error, yerr = sciencecurve_error, fmt = 'k.')
plt.show()
fig.savefig('exo_lightcurve.pdf', bbox_inches='tight', dpi=fig.dpi)
