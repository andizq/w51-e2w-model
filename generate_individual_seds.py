import runpy
import os
import shutil

runpy.run_path('exec_paraboloid.py')
runpy.run_path('exec_shellparab.py')

import sf3dmodels.BuildGlobalGrid as BGG
from sf3dmodels import Model, Plot_model as Pm, Utils as U
import numpy as np

sizex = 1700 * U.AU
sizey = sizez = 1700 * U.AU 
Nx = 60 
Ny = Nz = 60
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

os.system('radmc3d sed dpc 5410')
shutil.move('spectrum.out','spectrum_shell+parab.out')

runpy.run_path('plot_sed_data.py')
runpy.run_path('generate_fits.py')

os.system('mkdir radmc3d_inp')
os.system('mv *.inp radmc3d_inp')
os.system('mkdir radmc3d_out')
os.system('mv *.out radmc3d_out')
