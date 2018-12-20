import runpy
import os
import shutil

runpy.run_path('exec_paraboloid.py')
runpy.run_path('exec_shellparab.py')

import sf3dmodels.BuildGlobalGrid as BGG
from sf3dmodels import Model, Plot_model as Pm, Utils as U
import numpy as np

sizex = 1700 * U.AU
sizey = sizez = sizex
Nx = 60 
Ny = Nz = Nx
GRID = Model.grid([sizex, sizey, sizez], [Nx, Ny, Nz], radmc3d = True)
global_prop = BGG.overlap(GRID, all = False, radmc3d = True,
                          submodels=['paraboloid0.dat'])

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_parab.out')

global_prop = BGG.overlap(GRID, all = False, radmc3d = True,
                          submodels=['shell0.dat'])

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_shell.out')

global_prop = BGG.overlap(GRID, all = False, radmc3d = True,
                          submodels=['shell0.dat', 'paraboloid0.dat'])

from astropy import units as u
alpha_b = 2.6e-13*u.cm**3 * u.s**-1
Q = ((alpha_b * (global_prop.GRID.step*u.m)**3 * (global_prop.density*u.m**-3)**2).sum()).decompose()
print('log10 of the ionizing luminosity Q [photons s^-1]', np.log10(Q.value))

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_shell+parab.out')

runpy.run_path('plot_sed_data.py')
runpy.run_path('generate_fits.py')

os.system('mkdir radmc3d_inp')
os.system('mv *.inp radmc3d_inp')
os.system('mkdir radmc3d_out')
os.system('mv *.out radmc3d_out')
