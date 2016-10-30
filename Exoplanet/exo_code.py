##########################################################################################
#                                                                                        #
#   This program takes 5 arguments:                                                      #
#   1) A final name for a file containing a list of dark exposure file names             #
#   2) A final name for a file containing a list of the long exposure flats file names   #
#   3) A final name for a file containing a list of the short exposure flats file names  #
#   4) A final name for a file containing a list of science exposure file names          #
#   5) A basename that all files written by this program will start with                 #
#                                                                                        #
#   There are four functions defined below:                                              #
#   1) PixelMask(longfiles, shortfiles), whice creates and returns an image of the ratio #
#      of the non-normalized master flat images for the long and short exposures         #
#   2) AverageDark(darkfiles), which creates and returns the master dark image           #
#   3) AverageFlat(flatfiles,masterdark) which creats and returns the master dark        #
#      subtracted flat image                                                             #
#   4) ScienceExposure(rawscidata,masterdark,masterflat), which applied the master       #
#      dark and flat images to a raw science image                                       #
#                                                                                        #
#   Below these functions is the main body of the program, which applies the master      #
#   dark and master flat to all of the science images and writes that clean science      #
#   images to files                                                                      #
#                                                                                        #
#   This code was adapted from code written by the TAs of the Physics 100 course at      #
#   Stanford University (Anna Ogorzalek et al.).                                         #
#   Modified for PHY 517 / AST 443 at Stony Brook University by Drew Jamieson and        #
#   Anja von der Linden                                                                  #
#   Modified for specific lab group in AST 443 at Stony Brook University by Yogesh Mehta # 
#   and Joseph Monroy                                                                    #
#                                                                                        #
##########################################################################################

# This is the incomplete version of the calibration script that you will be
# using to process all of your observatory data. You will need to finish 
# this script to complete the data reduction. Remember at any point
# during development you can try running the script on a real data and see
# if the output products make sense.

# Here are the libraries we need. Note that wherever you see np, that
# stands for Numpy. 'import' loads an external library.

import pyfits
import numpy as np
import sys,os
import pdb

# Python is an interpreted programming language, so we have to put all of our functions BEFORE
# the main body of the code!

#This function maps the bad pixels
def PixelMask(longfiles, shortfiles):
    #Open the long exposure files and store in 2D numpy array containing doubles
    longflats = np.array([pyfits.open(i.rstrip('\n'))[0].data for i in open(longfiles)])
    longflats = longflats.astype(float)

    #Open the short exposure files and store in 2D numpy array containing doubles
    shortflats = np.array([pyfits.open(i.rstrip('\n'))[0].data for i in open(shortfiles)])
    shortflats = shortflats.astype(float)

    masterlong=np.median(longflats,axis=0) # Median combines long flat images
    mastershort=np.median(shortflats,axis=0) # Median combines short flat images
    
    pixelimage = masterlong/mastershort #These pixels should all be 3 (ratio of our exposure times)
    
    return pixelimage

# This function does the combining of dark currents
def AverageDark(darkfiles):

    # opens each dark image file and stores the 2d images in a numpy array
    darkdata=np.array([pyfits.open(i.rstrip('\n'))[0].data for i in open(darkfiles)])
    
    # make the master dark file (uses median)
    masterdark = np.median(darkdata, axis = 0)
  
    return masterdark
    

# This function creates a combined flat field image
def AverageFlat(flatfiles):
     
    # opens each flat image file and stores the 2d images in a numpy array
    flatdata=np.array([pyfits.open(i.rstrip('\n'))[0].data for i in open(flatfiles)])
    flatdata = flatdata.astype(float)
    
    # normalizes each image by its median (useful especially if the flats have very different count level):
    for i in range(0,flatdata.shape[0]):
        flatdata[i] = flatdata[i]/np.median(flatdata[i])
    masterflat=np.median(flatdata,axis=0) # Median combines flat images
    masterflat = masterflat/np.mean(masterflat) # Normalizes to the mean of the flats
    return masterflat


# This function creates the processed science image after combined dark, and flat images have been created.  
def ScienceExposure(rawscidata,masterdark,masterflat):
    
    rawimage=rawscidata.data #Gets the data from the header of the science image file
    rawimage = rawimage.astype(float)
    
    scienceimage= (rawimage - masterdark)/masterflat   #creates final science image
    
    return scienceimage


# This is the end of the functions. The main body of the code begins below.

# Each of these is an argument that needs to be on the calling of the script. 
# Make sure you run with all arguments provided or you will run into errors!

darkfilelist=sys.argv[1]    # First argument is a text file that lists the names of all dark current image file names
longflatfilelist=sys.argv[2]    # Second argument is a text file that lists the names of all of the long exposure flat field images
shortflatfilelist = sys.argv[3] # Third argument is a text file that lists the names of all of the short exposure flat field images
sciencefilelist=sys.argv[4] # Fourth argument is a text file that lists the names of all the science images
basename=sys.argv[5]        # All of the output files will start with the string value of basename. 

finaldark=AverageDark(darkfilelist) # Find function aboved

finalflat=AverageFlat(longflatfilelist) # Find function aboved

#finalpixel = PixelMask(longflatfilelist, shortflatfilelist)

for sciencefile in open(sciencefilelist): # Loops though all science files to apply finaldark and finalflat corrections

    sciencefile = sciencefile.rstrip(' \n')
    
    rawdata=pyfits.open(sciencefile+'.FIT')[0] # This gets the 1st extension (starts with 0!), this is an example of 
                                        # using pyfits.open, this is a FITS file object
    finalimage=ScienceExposure(rawdata,finaldark,finalflat) # Find function above
    sciheader=rawdata.header # This grabs the header object from the FITS object rawdata
    newscience=basename+'_'+sciencefile+'_clean.fits'  # Appending filenames onto the base
    sciencehdu=pyfits.PrimaryHDU(finalimage,header=sciheader)  # This converts a numpy array into a FITS object with a 
                                                               # data block (finalimage) and a header (sciheader)
    sciencehdu.writeto(newscience, clobber=True) # This writes the fits object to the file name newscience, which is 
                                                 # defined above The clobber means to overwrite the file if it already exists.
    
newdark=basename+'_Master_Dark.fits'
newflat=basename+'_Master_Flat.fits'
newpixel = basename + '_Pixel_Map.fits'

darkhdu=pyfits.PrimaryHDU(finaldark)
darkhdu.writeto(newdark, clobber=True)

flathdu = pyfits.PrimaryHDU(finalflat)
flathdu.writeto(newflat, clobber = True)

pixelhdu = pyfits.PrimaryHDU(finalpixel)
pixelhdu.writeto(newpixel, clobber = True)
###################################### End of Program ##########################################
