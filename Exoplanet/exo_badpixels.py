#Creates bad pixel mask

import astropy.io.fits as fits
import numpy as np
import sys

#Get fits file for pixel map (ratio of exposure times)
pixelfilename = sys.argv[1]
pixelfile = fits.open(pixelfilename)

#Extracts data into 2D numpy array
image = np.array([pixelfile[0].data])

#Upon inspecting the image with ds9, we determined that
#anthing pixel with a value less than 2.8 was bad
badpixels = np.array(np.where(image <= 2.8))

#Making bad pixel mask
mask = np.ones(image.shape)
for i in range(0, badpixels.shape[1])
    y = badpixels[i,1]
    x = badpixels[i,2]
    mask[y,x] = 0

pixelfile.close()
