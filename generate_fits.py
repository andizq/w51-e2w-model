import runpy
import os
import shutil

os.system('radmc3d image lambda 3157.9 npixx 172 npixy 172') #95 GHz 
#True image: 164, 172
os.system('python2.7 plot_fits_image.py -f image_95ghz.fits')
shutil.move('image.out','image_95ghz.out')

os.system('radmc3d image lambda 6666.7 incl 0 phi 0 npixx 86 npixy 86') #45 GHz
#True image: 83, 86
os.system('python2.7 plot_fits_image.py -f image_45ghz.fits')
shutil.move('image.out','image_45ghz.out')
