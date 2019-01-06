import numpy as np
from astropy.io import fits

#***************************************
#Setting parameters to shift the model
#***************************************

path_data = './data/'
dist = 5410. #pc

def get_name(freq):
    if freq is None: img_data = path_data + 'W51e2w_ALMAB3_cutout.fits' 
    elif '45' in freq: img_data = path_data + 'W51e2w_VLA_Q_cutout.fits'
    elif '95' in freq: img_data = path_data + 'W51e2w_ALMAB3_cutout.fits'
    return img_data

def get_shift(freq):
    if freq is None:
        img_data = get_name(freq)
        cy, cx = 127, 41 #real paraboloid centre in pxls
        posang = 225.
        #Adjusting centres:
        cy -= 7
        cx -= 3

    elif '45' in freq: 
        img_data = get_name(freq)
        cy, cx = 62, 23 #real paraboloid centre in pxls
        posang = 225.
        #Adjusting centres:
        cy -= 4
        #cx -= 6

    elif '95' in freq: 
        img_data = get_name(freq)
        cy, cx = 127, 41 #real paraboloid centre in pxls
        posang = 225.
        #Adjusting centres:
        cy -= 7
        cx -= 3
        
    datah = fits.getheader(img_data)
    pixres = abs(datah['CDELT1']) * 3600 #pixel resolution of the data, in arcsecs
    iy, ix = np.array([datah['NAXIS2'], datah['NAXIS1']]) / 2 #image centre in pxls
    dx = pixres * (cx - ix) * dist #x-shift in au
    dy = pixres * (cy - iy) * dist #y-shift in au
    
    return dx,dy,posang

def get_size(freq):
    img_data = get_name(freq)
    datah = fits.getheader(img_data)
    pxls = (datah['NAXIS1'], datah['NAXIS2'])
    pxls_max = np.max(pxls) #number of pxls of the greater dimension in the image
    pixres = abs(datah['CDELT1']) * 3600 #pixel resolution of the data, in arcsecs
    size = pixres * pxls_max * dist #size of the greater dimension in the image, in au

    return pxls_max, size
