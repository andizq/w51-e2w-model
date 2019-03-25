import runpy
import os
import subprocess
import shutil
from utils_paraboloid import get_size

pxls, size = get_size('45')
subprocess.check_call('radmc3d image lambda 6666.7 incl 0 phi 0 npix %d sizeau %f'%(pxls,size), shell=True) #45 GHz
#Real image: 86, 83
subprocess.call('python3 plot_fits_image.py -f image_45ghz.fits', shell=True)
shutil.move('image.out','image_45ghz.out')

pxls, size = get_size('95')
subprocess.check_call('radmc3d image lambda 3157.9 incl 0 phi 0 npix %d sizeau %f'%(pxls,size), shell=True) #95 GHz 
#Real image: 172, 164
subprocess.call('python3 plot_fits_image.py -f image_95ghz.fits', shell=True)
shutil.move('image.out','image_95ghz.out')
