import radmc3dPy.image as image
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser(prog='Burgers', description='Self-obscuration')
parser.add_argument('-f', '--file', help='fits file to write')
args = parser.parse_args()

if args.file: file = args.file
else: file = 'image.fits'
    
dist = 5410.
im = image.readImage()

#image.plotImage(im, au=True, log=True, maxlog=10, saturate=1e-5, cmap=plt.cm.gist_heat)
"""
image.plotImage(im, dpc=140, arcsec=True, log=True, maxlog=10, saturate=1e-5, cmap=plt.cm.gist_heat)
image.plotImage(im, dpc=dist, arcsec=True, log=True, maxlog=10, saturate=1e-5, cmap=plt.cm.gist_heat)
cim = im.imConv(fwhm=[1.0, 0.6], pa=120., dpc=dist)
image.plotImage(cim, arcsec=True, dpc=dist, log=True, maxlog=10, bunit='snu', cmap=plt.cm.gist_heat)
"""
im.writeFits(file, dpc=dist)#, coord='03h10m05s -10d05m30s')


#Mirar lo de inputs desde terminal
