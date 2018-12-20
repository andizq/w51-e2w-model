import sf3dmodels.BuildGlobalGrid as BGG
from sf3dmodels import Model, Plot_model as Pm, Utils as U
import numpy as np

sizex = 1700 * U.AU
sizey = sizez = sizex
Nx = 60 
Ny = Nz = Nx
GRID = Model.grid([sizex, sizey, sizez], [Nx, Ny, Nz], radmc3d = True)
#list_sub = ['datatab_Main.dat', 'datatab_Burger.dat']
global_prop = BGG.overlap(GRID, all = True, radmc3d = True)

from astropy import units as u
alpha_b = 2.6e-13*u.cm**3 * u.s**-1
print(((global_prop.GRID.step*u.m)**3 * (global_prop.density*u.m**-3)**2 * alpha_b).sum().decompose())

#--------
#PLOTTING
#--------
"""
GRID = global_prop.GRID 
density = global_prop.density / 1e6 #1e6 to convert from m^-3 to cm^-3
temperature = global_prop.temperature

weight = 1 * np.mean(density)

#-----------------
#Plot for DENSITY
#-----------------

Pm.scatter3D(GRID, density, weight, NRand = 3000, axisunit = U.AU, colorscale = 'log', palette = 'cool',
                  colorlabel = r'${\rm log}_{10}(\rho [cm^{-3}])$', output = 'global_grid_dens.png', vmin = 5.5)

#--------------------
#Plot for TEMPERATURE
#--------------------
Pm.scatter3D(GRID, density, weight, colordim = temperature, NRand = 3000, axisunit = U.AU, colorscale = 'log',
             palette = 'brg', colorlabel = r'${\rm log}_{10}(T$ $[K])$', output = 'global_grid_temp.png', vmin = 2)
"""
