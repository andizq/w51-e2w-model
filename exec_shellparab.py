from sf3dmodels.create_parabola import *
from sf3dmodels.Utils import *
from sf3dmodels.Model import Make_Datatab
from argparse import ArgumentParser
from utils_paraboloid import get_shift
import os

parser = ArgumentParser(prog='Paraboloids', description='Modelling paraboloid HII regions')
parser.add_argument('-freq', '--freq', help='frequency of the fits file to be convolved')
args = parser.parse_args()

#***************************************
#Getting parameters to shift the model
#***************************************
dx, dy, posang = get_shift(args.freq)
print("Outer shell shift in au", dx, dy)

#***************************************
#MODELLING
#***************************************
tag = 'shell0.dat'

z_min = 1*AU
z_max = 400*AU
"""
drBIGGRID = sqrt(dx**2+dy**2+dz**2) or smaller 
 --> the smaller the more points to be generated
"""
drBIGGRID = 20*AU

#rho = lambda R: dens0
#T = lambda R: 10000.

T0 = 10000.
qT = 0.
temp = [T0, qT]

dens0 = 2.6e13
qn = -0.4 #-2
dens = [dens0, qn]

a = 1.8*np.sqrt(300*AU) #10*AU
b = 1.8*np.sqrt(300*AU) #10*AU
GRID, props = make_paraboloid(z_min, z_max, drBIGGRID, a, b, dens, T0, width = 20*AU)
shift = Model.ChangeGeometry(GRID, center = np.array([0, dy-20, dx+20])*AU,
                             rot_dict = { 'angles': [-np.pi/180*(posang+90 + 8),
                                                      -np.pi/12], 
                                          'axis': ['x','y'] })
GRID.XYZ = shift.newXYZ
Make_Datatab(props, GRID).submodel(tag = tag)

