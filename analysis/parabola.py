from __future__ import print_function
import os
from astropy.io import fits
from astropy import wcs
from astropy import units as u
import regions
import numpy as np
import pylab as pl
import sys

print (sys.argv)
path_data = '/Users/andrespipecar42/w51/data/'
if not os.path.exists(path_data+'W51e2w_ALMAB3_cutout.fits'):
    fh = fits.open('/Users/adam/work/w51/alma/FITS/longbaseline/w51e2_sci.spw0_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17_18_19.mfs.I.manual.image.tt0.pbcor.fits')
    ww = wcs.WCS(fh[0].header).celestial
    pr0 = regions.read_ds9('/Users/adam/work/w51/vla_q/regions/e2w_ellipse.reg')[0].to_pixel(ww)
    pr0.width *= 2.5
    pr0.height *= 2.5
    msk = pr0.to_mask()
    img_95ghz = msk.multiply(fh[0].data.squeeze())

    header = fh[0].header
    ww_cutout = ww[msk.bbox.slices]
    header.update(ww_cutout.to_header())
    fits.PrimaryHDU(data=img_95ghz, header=header).writeto('W51e2w_ALMAB3_cutout.fits', overwrite=True)
else:
    img_95ghz = fits.getdata(path_data+'W51e2w_ALMAB3_cutout.fits')

if not os.path.exists(path_data+'W51e2w_VLA_Q_cutout.fits'):
    fh = fits.open('/Users/adam/work/w51/vla_q/FITS/W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal9.image.tt0.pbcor.fits')
    ww = wcs.WCS(fh[0].header).celestial
    pr0 = regions.read_ds9('/Users/adam/work/w51/vla_q/regions/e2w_ellipse.reg')[0].to_pixel(ww)
    pr0.width *= 2.5
    pr0.height *= 2.5
    msk = pr0.to_mask()
    img_45ghz = msk.multiply(fh[0].data.squeeze())

    header = fh[0].header
    ww_cutout = ww[msk.bbox.slices]
    header.update(ww_cutout.to_header())
    fits.PrimaryHDU(data=img_45ghz, header=header).writeto('W51e2w_VLA_Q_cutout.fits', overwrite=True)
else:
    img_45ghz = fits.getdata(path_data+'W51e2w_VLA_Q_cutout.fits')


#******************
#ANALYSIS 45 GHz
#******************
angle = (180+315) * u.deg
cy,cx = np.where(img_45ghz == np.max(img_45ghz))
cy += 3; cx += 2 #Small adjustments
print ('Image 45 GHz --> center cy,cx: ({}, {})'.format(cy,cx) 
       + ', position angle:', (90 + angle.value%360)*u.deg)

xx = np.linspace(0,25,1000)
yy = xx**2 / 17

xx_, yy_ = np.dot([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]], [xx,yy])
xx2_, yy2_ = np.dot([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]], [-xx,yy])

fig, ax = pl.subplots(ncols = 2, figsize=(10,4))
ax[0].set_title('Data - 45 GHz')
ax[0].imshow(img_45ghz, origin='lower', interpolation='none')
ax[0].plot(xx_+cx,yy_+cy, linewidth=0.5, color='w', linestyle='--')
ax[0].plot(xx2_+cx,yy2_+cy, linewidth=0.5, color='w', linestyle='--')

data_on_path = img_45ghz[(yy_+cy).astype('int'), (xx_+cx).astype('int')]
data_on_path2 = img_45ghz[(yy2_+cy).astype('int'), (xx2_+cx).astype('int')]
prj_dist = (xx**2+yy**2)**0.5

ax[1].plot(prj_dist, data_on_path, label='left arm')
ax[1].plot(prj_dist, data_on_path2, label='right arm')
core = data_on_path[:10].mean()

"""
profile = (core*(prj_dist/prj_dist[250])**-0.1 * (prj_dist >= prj_dist[250])/10.
           + core * (1-(prj_dist/prj_dist[580])**2) * (prj_dist<=prj_dist[580])
           )
"""
profile = core * (1-(prj_dist/prj_dist[580])**2) * (prj_dist<=prj_dist[580])
ax[1].plot(prj_dist, profile)
ax[1].legend()


#******************
#ANALYSIS 95 GHz
#******************
cy,cx = np.where(img_95ghz == img_95ghz.max()) #127,41
cy += 2; cx += 1 #Small adjustments
print ('Image 95 GHz --> center cy,cx: ({}, {})'.format(cy,cx) 
       + ', position angle:', (90 + angle.value%360)*u.deg)

xx = np.linspace(0,50,1000)
yy = xx**2 / 28

xx_, yy_ = np.dot([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]], [xx,yy]) #rotation clockwise
xx2_, yy2_ = np.dot([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]], [-xx,yy])

fig, ax = pl.subplots(ncols = 2, figsize=(10,4))
ax[0].set_title('Data - 95 GHz')
ax[0].imshow(img_95ghz, origin='lower', interpolation='none')
ax[0].plot(xx_+cx,yy_+cy, linewidth=0.5, color='w', linestyle='--')
ax[0].plot(xx2_+cx,yy2_+cy, linewidth=0.5, color='w', linestyle='--')

data_on_path = img_95ghz[(yy_+cy).astype('int'), (xx_+cx).astype('int')]
data_on_path2 = img_95ghz[(yy2_+cy).astype('int'), (xx2_+cx).astype('int')]
prj_dist = (xx**2+yy**2)**0.5

ax[1].plot(prj_dist, data_on_path, label='left arm')
ax[1].plot(prj_dist, data_on_path2, label='right arm')

core = data_on_path[:10].mean()
profile = core * (1-(prj_dist/prj_dist[580])**2) * (prj_dist<=prj_dist[580])
ax[1].plot(prj_dist, profile)
ax[1].legend()
