import runpy
import os
import shutil
from utils_paraboloid import get_size

pxls, size = get_size('45')
os.system('radmc3d image lambda 6666.7 incl 0 phi 0 npix %d sizeau %f'%(pxls,size)) #45 GHz
#True image: 86, 83
os.system('python2.7 plot_fits_image.py -f image_45ghz.fits')
shutil.move('image.out','image_45ghz.out')

pxls, size = get_size('95')
os.system('radmc3d image lambda 3157.9 incl 0 phi 0 npix %d sizeau %f'%(pxls,size)) #95 GHz 
#True image: 172, 164
os.system('python2.7 plot_fits_image.py -f image_95ghz.fits')
shutil.move('image.out','image_95ghz.out')
