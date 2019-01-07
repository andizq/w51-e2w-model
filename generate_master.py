from __future__ import print_function
import runpy
import os, sys
import shutil
import time
import numpy as np

import sf3dmodels.BuildGlobalGrid as BGG
from sf3dmodels import Model, Plot_model as Pm, Utils as U

t0 = time.time()
runpy.run_path('exec_paraboloid.py')
runpy.run_path('exec_shellparab.py')

#Plotting 3-D grid points?
plot_3d = True 

#**********************************
#SETTING DEFAULTS FOR RADMC-3D
#**********************************
nthreads = 4 
"""
in kwargs_wavelength:
lam: wavelength intervals in microns, nxx: num of partitions in each interval 
"""
files_ff = lambda R: R.freefree(kwargs_control = {'setthreads': nthreads},
                                kwargs_wavelength = {'lam': [5e2,2e4,4e4,3e5], 
                                                     'nxx': [20,20,20]}) 
dict_from_global = lambda G: {'dens_elect': G.density, 
                              'dens_ion': G.density,
                              'tgas': G.temperature} 
 
#**********************************
#COMMON GRID TO MERGE MODELS IN
#**********************************
sizex = 3000 * U.AU
sizey = sizez = sizex
Nx = 125 
Ny = Nz = Nx
GRID = Model.grid([sizex, sizey, sizez], [Nx, Ny, Nz], radmc3d = True)

#**********************************
#MERGING PARABOLOID ONLY + SED
#**********************************
globalA = BGG.overlap(GRID, all = False, radmc3d = True,
                      submodels=['paraboloid0.dat'])
prop_dict = dict_from_global(globalA)

A = Model.Radmc3d(prop_dict, GRID)
files_ff(A)

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_parab.out')
print ('-------------------------------------------------\n-------------------------------------------------')

#**********************************
#MERGING SHELL ONLY + SED
#**********************************
globalB = BGG.overlap(GRID, all = False, radmc3d = True,
                      submodels=['shell0.dat'])
prop_dict = dict_from_global(globalB)

B = Model.Radmc3d(prop_dict, GRID)
files_ff(B)

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_shell.out')
print ('-------------------------------------------------\n-------------------------------------------------')

#**********************************
#MERGING PARABOLOID+SHELL + SED
#**********************************
globalC = BGG.overlap(GRID, all = False, radmc3d = True,
                      submodels=['shell0.dat', 'paraboloid0.dat'])
prop_dict = dict_from_global(globalC)

C = Model.Radmc3d(prop_dict, GRID)
files_ff(C)

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_shell+parab.out')

#**********************************
#GRID POINTS 3-D PLOTTING
#**********************************
if plot_3d:
    tags = iter(['A','B','C'])
    npoints = iter([2000,3000,2000])
    for density in [globalA.density, globalB.density, globalC.density]:
        dens2plot = density/1e6
        weight = 10*np.mean(dens2plot)
        Pm.scatter3D(GRID, dens2plot, weight, 
                     NRand = next(npoints), axisunit = U.AU, 
                     colorscale = 'log', 
                     cmap = 'cool',
                     colorlabel = r'${\rm log}_{10}(\rho [cm^{-3}])$', 
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
print("Moving *.inp files to radmc3d_inp/")
os.system('mv *.inp radmc3d_inp')

print("Creating folder radmc3d_out/")
os.system('mkdir radmc3d_out')
print("Moving *.out files to radmc3d_out/")
os.system('mv *.out radmc3d_out')

print("\n*** Using python3 (astropy2) for the convolution ***\n")
os.system('python3 convolve_fits.py -freq 45') 
os.system('python3 convolve_fits.py -freq 95') 

print("Moving *.fits files to data/")
os.system('mv *.fits data')

from astropy import units as u
alpha_b = 2.6e-13*u.cm**3 * u.s**-1
Q = ((alpha_b * (GRID.step*u.m)**3 * (globalC.density*u.m**-3)**2).sum()).decompose()
print('log10 of the ionizing luminosity Q [photons s^-1]:', np.log10(Q.value))

print("Ellapsed time from master: %.2f s"%(time.time()-t0))
print ('-------------------------------------------------\n-------------------------------------------------')
