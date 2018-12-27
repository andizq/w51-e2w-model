import runpy
import os
import shutil

os.system('radmc3d image lambda 3157.9 incl 0 phi -30 npix 172') #95 GHz 
#True image: 172, 164
os.system('python2.7 plot_fits_image.py -f image_95ghz.fits')
shutil.move('image.out','image_95ghz.out')

os.system('radmc3d image lambda 6666.7 incl 0 phi -30 npix 86') #45 GHz
#True image: 86, 83
os.system('python2.7 plot_fits_image.py -f image_45ghz.fits')
shutil.move('image.out','image_45ghz.out')
