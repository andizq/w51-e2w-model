from sf3dmodels.create_parabola import *
from sf3dmodels.Utils import *
import os

os.system('mkdir Subgrids')
folder='./Subgrids/'
tag = folder+'paraboloid0.dat'

pos_c = np.array([0, 0, 0])
dir = np.array([0, 0, 1])
pos_f = pos_c + dir #[300*AU, 0, 1000*AU]
r_min = 1*AU
r_max = 1500*AU
drBIGGRID = 80*AU

#rho = lambda R: dens0
#T = lambda R: 10000.

T0 = 10000.
qT = 0.
temp = [T0, qT]

dens0 = 2e14 * 5 / 2.5 / 1.1
qn = -1. #-2
#dens0 = 2e14 * 5 / 2.5 / 50
#qn = -0.5 #-2
dens = [dens0, qn]

a = np.sqrt(2*300*AU) #10*AU
b = np.sqrt(4*150*AU) #10*AU
make_paraboloid(pos_c, pos_f, r_min, drBIGGRID, a, b, dens, T0, r_max = r_max, name = tag)


