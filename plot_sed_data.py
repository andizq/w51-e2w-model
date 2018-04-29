from radmc3dPy.analyze import *
import matplotlib.pyplot as plt

tag = 'all'

data = {13.5: 0.15587470697361785,
 25.0: 0.34918392701200385,
 27.0: 0.33573671861347437,
 29.0: 0.2565478972380418,
 33.0: 0.3629123405746117,
 36.0: 0.2649481591519583,
 42.5: 0.5145262038367601,
 43.5: 0.5239466039409053,
 44.5: 0.5244943648836852,
 45.5: 0.5141563275079916,
 46.5: 0.5811386102964936,
 47.5: 0.6159157052591661,
 95.0: 0.5967870400672453}


s = readSpectrum(fname = 'spectrum_shell+parab.out') #column 0: wavelength in microns; column 1: Flux in cgs.
s2 = readSpectrum(fname = 'spectrum_parab.out')
s3 = readSpectrum(fname = 'spectrum_shell.out') 
distance = 5410. #in pc. The spectrum.out file is still normalized to a distance of 1 pc (see radmc3d docs)
F_nu = s[:,1] * distance**-2 * 1e23 #to Jy at the set distance
F_nu2 = s2[:,1] * distance**-2 * 1e23
F_nu3 = s3[:,1] * distance**-2 * 1e23
nu = 3e8 * s[:,0]**-1 * 1e6 * 1e-9 #microns to GHz
plt.plot(nu, F_nu, label = "shell+parab")
plt.plot(nu, F_nu2, label = "parab") 
plt.plot(nu, F_nu3, label = "shell") 
plt.plot(data.keys(), data.values(), 'o')
plt.title('%s - distance: %d pc'%(tag,distance))
plt.xlabel('Frequency [GHz]'); plt.ylabel('Flux [Jy]')
plt.xscale('log'); plt.yscale('log')
plt.legend()
plt.savefig('sed_'+tag+'.png', dpi=300)
plt.show()
