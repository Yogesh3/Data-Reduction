# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 00:26:51 2016

@author: Yogesh
"""

import astropy.io.fits as pyfits
import numpy as np
import sys

def PixelMask(longfiles, shortfiles):
    #Open the long exposure files and store in 2D numpy array containing doubles
    longflats = np.array([pyfits.open(i.rstrip('\n'))[0].data for i in open(longfiles)])
    longflats = longflats.astype(float)

    #Open the short exposure files and store in 2D numpy array containing doubles
    shortflats = np.array([pyfits.open(i.rstrip('\n'))[0].data for i in open(shortfiles)])
    shortflats = shortflats.astype(float)

    masterlong=np.median(longflats,axis=0) # Median combines long flat images
    mastershort=np.median(shortflats,axis=0) # Median combines short flat images
    
    pixelimage = masterlong/mastershort #These pixels should all be 3, which is the ratio of our exposure times
    
    return pixelimage

longflatfilelist=sys.argv[1]    # Second argument is a text file that lists the names of all of the long exposure flat field images
shortflatfilelist = sys.argv[2] # Third argument is a text file that lists the names of all of the short exposure flat field images
basename = sys.argv[3]

finalpixel = PixelMask(longflatfilelist, shortflatfilelist)
newpixel = basename + '_Pixel_Map.fits'

pixelhdu = pyfits.PrimaryHDU(finalpixel)
pixelhdu.writeto(newpixel, clobber = True)
