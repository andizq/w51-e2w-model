from sf3dmodels.create_parabola import *
from sf3dmodels.Utils import *
from sf3dmodels.Model import Make_Datatab
from astropy.io import fits
from argparse import ArgumentParser
import os

parser = ArgumentParser(prog='Paraboloids', description='Modelling paraboloid HII regions')
parser.add_argument('-freq', '--freq', help='frequency of the fits file to be convolved')
args = parser.parse_args()
path_data = '/Users/andrespipecar42/w51/data/'
dist = 5410. #pc

#***************************************
#Getting real centres to shift the model
#***************************************
if args.freq is None:
    img_data = path_data + 'W51e2w_ALMAB3_cutout.fits'
    cy, cx = 127, 41 #real paraboloid center in pxls
    posang = 225.

elif '45' in args.freq: 
    img_data = path_data + 'W51e2w_VLA_Q_cutout.fits'
    cy, cx = 62, 23 #real paraboloid center in pxls
    posang = 225.

elif '95' in args.freq: 
    img_data = path_data + 'W51e2w_ALMAB3_cutout.fits'
    cy, cx = 127, 41 #real paraboloid center in pxls
    posang = 225.

datah = fits.getheader(img_data)
pixres = abs(datah['CDELT1']) * 3600 #pixel resolution of the data in arcsecs
iy, ix = np.array([datah['NAXIS2'], datah['NAXIS1']]) / 2 #image centre in pxls
dx = pixres * (cx - ix) * dist #x-shift in au
dy = pixres * (cy - iy) * dist #y-shift in au
print("Shell shift in au", dx, dy)

#***************************************
#MODELLING
#***************************************
tag = 'shell0.dat'

z_min = 1*AU
z_max = 1500*AU
drBIGGRID = 80*AU

#rho = lambda R: dens0
#T = lambda R: 10000.

T0 = 10000.
qT = 0.
temp = [T0, qT]

dens0 = 1*3.e14 / 15. * 2. * 1.1
qn = -0.5 #-2
dens = [dens0, qn]

a = 1.3*np.sqrt(300*AU) #10*AU
b = 3.2*np.sqrt(150*AU) #10*AU
GRID, props = make_paraboloid(z_min, z_max, drBIGGRID, a, b, dens, T0, width = 40*AU)
shift = Model.ChangeGeometry(GRID, center = np.array([0, dy, dx])*AU,
                             rot_dict = { 'angles': [-np.pi/180*(posang+90 + 2)], 'axis': ['x'] })
GRID.XYZ = shift.newXYZ
Make_Datatab(props, GRID).submodel(tag = tag)

