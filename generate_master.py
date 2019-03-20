from __future__ import print_function
import runpy
import os, sys
import shutil
import time
import numpy as np

from sf3dmodels import (Model, Plot_model as Pm)
from sf3dmodels.grid import Overlap
import sf3dmodels.utils.units as u
import sf3dmodels.rt as rt


t0 = time.time()
runpy.run_path('exec_paraboloid.py')
runpy.run_path('exec_shellparab.py')
columns = ['id', 'x', 'y', 'z', 'dens_ion', 'dens_e', 'temp_gas'] #columns in submodel files

#Plotting 3-D grid points?
plot_3d = True 

#**********************************
#SETTING DEFAULTS FOR RADMC-3D
#**********************************
nthreads = 4 
files_ff = lambda R, prop: R.freefree(prop, 
                                      kwargs_control = {'setthreads': nthreads},
                                      kwargs_wavelength = {'lam': [5e2,2e4,4e4,3e5], 
                                                           'nxx': [20,20,20]})  
""" 
About the lambda function files_ff
- R is an instance of the class rt.Radmc3dDefaults
- prop is a dictionary with the physical properties needed for free-free calculations. 
- in kwargs_wavelength:
  lam: wavelength intervals in microns, 
  nxx: num of partitions in each interval
"""
#*************************************
#COMMON GRID TO MERGE THE SUBMODELS IN
#*************************************
sizex = 3000 * u.au
sizey = sizez = sizex
Nx = 125 
Ny = Nz = Nx
GRID = Model.grid([sizex, sizey, sizez], [Nx, Ny, Nz], rt_code='radmc3d')

#**********************************
#MERGING PARABOLOID ONLY + SED
#**********************************
globalA = Overlap(GRID)
prop_globalA = globalA.fromfiles(columns, 
                                 submodels=['paraboloid0.dat'],
                                 rt_code = 'radmc3d')
A = rt.Radmc3dDefaults(GRID)
files_ff(A, prop_globalA)

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_parab.out')
print ('-------------------------------------------------\n-------------------------------------------------')

#**********************************
#MERGING SHELL ONLY + SED
#**********************************
globalB = Overlap(GRID)
prop_globalB = globalB.fromfiles(columns, 
                                 submodels=['shell0.dat'],
                                 rt_code = 'radmc3d')
B = rt.Radmc3dDefaults(GRID)
files_ff(B, prop_globalB)

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_shell.out')
print ('-------------------------------------------------\n-------------------------------------------------')

#**********************************
#MERGING PARABOLOID+SHELL + SED
#**********************************
globalC = Overlap(GRID)
prop_globalC = globalC.fromfiles(columns, 
                                 submodels=['shell0.dat', 'paraboloid0.dat'],
                                 rt_code = 'radmc3d')
C = rt.Radmc3dDefaults(GRID)
files_ff(C, prop_globalC)

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_shell+parab.out')

#**********************************
#GRID POINTS 3-D PLOTTING
#**********************************
if plot_3d:
    tags = iter(['A','B','C'])
    npoints = iter([3000,2000,4000])
    for density in [prop_globalA['dens_e'], prop_globalB['dens_e'], prop_globalC['dens_e']]:
        dens2plot = density/1e6
        weight = 10*np.mean(dens2plot)
        Pm.scatter3D(GRID, dens2plot, weight, 
                     NRand = next(npoints), axisunit = u.au, 
                     colorscale = 'log', 
                     cmap = 'cool',
                     colorlabel = r'${\rm log}_{10}(n_{e^-} [cm^{-3}])$', 
                     output = 'global_grid%s.png'%next(tags), 
                     vmin = 5.5,
                     azim = 10,
                     elev = 30,
                     show = False)

#**********************************
#PLOTTING SEDS + FITS + CONVOLUTION
#**********************************
runpy.run_path('plot_sed_data.py')
runpy.run_path('generate_fits.py')
print ('-------------------------------------------------\n-------------------------------------------------')
print("Creating folder radmc3d_inp/")
os.system('mkdir radmc3d_inp')
print("Moving *.inp files into radmc3d_inp/")
os.system('mv *.inp radmc3d_inp')

print("Creating folder radmc3d_out/")
os.system('mkdir radmc3d_out')
print("Moving *.out files into radmc3d_out/")
os.system('mv *.out radmc3d_out')

print("\n*** Using python3 (astropy2) for the convolution ***\n")
os.system('python3 convolve_fits.py -freq 45') 
os.system('python3 convolve_fits.py -freq 95') 

print("Moving *.fits files into data/")
os.system('mv *.fits data')

from astropy import units as un
alpha_b = 2.6e-13*un.cm**3*un.s**-1 #Notes-on-Photoionized-Regions, Caltech, 2011
Q = ((alpha_b * (GRID.step*un.m)**3 * (prop_globalC['dens_ion']*un.m**-3)**2).sum()).decompose() #Eq. 13 Vacca+1996
print('log10 of the ionizing luminosity Q [photons s^-1]:', np.log10(Q.value))

print("Ellapsed time from master: %.2f s"%(time.time()-t0))
print ('-------------------------------------------------\n-------------------------------------------------')
