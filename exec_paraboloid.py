from __future__ import print_function
import os
import numpy as np

from sf3dmodels import Model
from sf3dmodels.create_parabola import make_paraboloid
import sf3dmodels.utils.units as u
import sf3dmodels.rt as rt
from argparse import ArgumentParser
from utils_paraboloid import get_shift


parser = ArgumentParser(prog='Paraboloids', description='Modelling paraboloid HII-regions')
parser.add_argument('-freq', '--freq', default=95, help='Frequency in GHz of the reference fits file to shift paraboloid vertex')
args = parser.parse_args()

#***************************************
#Getting parameters to shift the model
#***************************************
dx, dy, posang = get_shift(args.freq)
print("Paraboloid shift in au", dx, dy)

#***************************************
#MODELLING
#***************************************
tag = 'paraboloid0.dat'

z_min = 1*u.au
z_max = 1800*u.au
"""
dx_grid --> the smaller the more grid points to be generated
"""
dx_grid = 40*u.au 

#rho = lambda R: dens0
#T = lambda R: 10000.

T0 = 10000.
qT = 0.
temp = [T0, qT]

dens0 = 0.24*2.6e14 
qn = -0.7 #-0.9
dens = [dens0, qn]

a = 2.0*np.sqrt(300*u.au) 
b = 2.0*np.sqrt(300*u.au)
GRID, props  = make_paraboloid(z_min, z_max, dx_grid, a, b, dens, T0)
shift = Model.ChangeGeometry(GRID, center = np.array([dx, dy, 0])*u.au,
                             rot_dict = { 'angles': [-np.pi/2,
                                                     1*np.pi/180*(posang+90 + 8),
                                                     -np.pi/12], 
                                          'axis': ['y','z','y'] })
GRID.XYZ = shift.newXYZ

prop_dict = {'dens_e': props[0],
             'dens_ion': props[0],
             'temp_gas': props[1]}
parab = rt.Radmc3d(GRID)
parab.submodel(prop_dict, output=tag)

print ('Columns written into file:', parab.columns)
