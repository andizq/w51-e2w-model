import BuildGlobalGrid as BGG
import Model
import Plot_model as Pm
import Utils as U
import numpy as np

sizex = 1700 * U.AU
sizey = sizez = 1700 * U.AU 
Nx = 60 
Ny = Nz = 60
GRID = Model.grid([sizex, sizey, sizez], [Nx, Ny, Nz], radmc3d = True)
#list_sub = ['datatab_Main.dat', 'datatab_Burger.dat']
global_prop = BGG.overlap(GRID, all = True, radmc3d = True)

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
