#astropy2->py36
import numpy as np
from astropy.convolution import Gaussian2DKernel, convolve, convolve_fft
from astropy.io import fits
from argparse import ArgumentParser

parser = ArgumentParser(prog='Paraboloids', description='Free free emission from paraboloids')
parser.add_argument('-freq', '--freq', help='frequency of the fits file to be convolved')
args = parser.parse_args()

path_data = '/Users/andrespipecar42/w51/data/'

assert args.freq != None, "Did not provide any frequency via: python convolve_fits.py -freq 95"

if '45' in args.freq: 
    img_data = path_data + 'W51e2w_VLA_Q_cutout.fits'
    img_sf3d = 'image_45ghz.fits'
    img_conv = 'image_45ghz-conv.fits'
elif '95' in args.freq: 
    img_data = path_data + 'W51e2w_ALMAB3_cutout.fits'
    img_sf3d = 'image_95ghz.fits'
    img_conv = 'image_95ghz-conv.fits'

#FWHM->stddev: FWHM=2*sqrt(2*log(2))*stddev ~= 2.35482*stddev
datah = fits.getheader(img_data)
sf3d = fits.open(img_sf3d)[0]

pixres = abs(datah['CDELT1'])

a_pix = datah['BMAJ'] / pixres
b_pix = datah['BMIN'] / pixres
posang = datah['BPA']

print ('Pixel resolution', pixres)
print ('Image centers in pxls x,y:', datah['NAXIS1']/2, datah['NAXIS2']/2)

x_stddev = a_pix / 2.35482 # = x_fwhm / 2.35482
y_stddev = b_pix / 2.35482 # = y_fwhm / 2.35482

r_gauss = hwhm = 0.5 * np.sqrt(a_pix * b_pix) 
areaBeamPix=1.442*np.pi*hwhm**2

#2*np.log(2)=1.386 for Gaussian func.
#1.442 for Bessel func.

#----------------------
#CONVOLUTION and HEADER
#----------------------
print ("Convolving free-free continuum image...")
print ('r_gauss:', r_gauss)

kernel = Gaussian2DKernel(x_stddev = x_stddev,
                          y_stddev = y_stddev,
                          theta = posang * np.pi/180 + np.pi/2)
nx = datah['NAXIS1']
ny = datah['NAXIS2']
result = areaBeamPix * convolve(sf3d.data.squeeze()[0:ny][0:nx], kernel)

sf3d.header['BUNIT'] = datah['BUNIT']
sf3d.header['BMAJ'] = datah['BMAJ']
sf3d.header['BMIN'] = datah['BMIN']
sf3d.header['BPA'] = posang 
sf3d.header['CRVAL1'] = datah['CRVAL1']
sf3d.header['CRPIX1'] = datah['CRPIX1']
sf3d.header['CDELT1'] = datah['CDELT1']
sf3d.header['CRVAL2'] = datah['CRVAL2']
sf3d.header['CDELT2'] = datah['CDELT2']
sf3d.header['CRPIX2'] = datah['CRPIX2']
sf3d.header['RADESYS'] = datah['RADESYS']

print ("Writing in '%s'"%img_conv)
fits.writeto(img_conv,result,sf3d.header,overwrite=True) 
