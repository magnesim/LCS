"""
Read a number of data files
Do some analysis, averaging
Plot results

"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from glob import glob
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime

import cmocean


cmap=cmocean.cm.turbid
#cmap=cmocean.cm.tempo
cmap=cmocean.cm.amp
cmap='gist_heat_r'

vmin = -0.01 ; vmax = 0.3
#vmin = 0.04; vmax = 0.2
vmin2 = 0.05 ; vmax2 = 0.2


proj_pp = ccrs.PlateCarree()


datadir = '/home/magnes/git/LCS/ALCS_jun/member0'
#files = '2023????_h0_norkyst_LCS.nc'
files = '2023040?_h0_norkyst_LCS.nc'


ff = glob(datadir+'/'+files)
ff = np.sort(ff)

#ff=ff[:4]

ntimes = len(ff)

alcst = []
times = []

times = np.array([item.split('/')[-1][:8] for item in ff])
times = np.array([datetime.strptime(item,'%Y%m%d') for item in times])
print(times)


for fi in ff:
    print('Read and plot file:',fi)

    d = xr.open_dataset(fi)
    
    alcs =  np.array(d.ALCS)
    lats =  np.array(d.lat)
    lons =  np.array(d.lon)

    alcst.append(alcs)

alcst=np.array(alcst)

print(alcst.shape)



for ii in range(ntimes):
    fig = plt.figure(figsize=[11,11])
    ax=plt.subplot(projection=ccrs.Orthographic(10,67))
    #ax.stock_img()
    ax.coastlines(lw=.4)
#    ax.add_feature(cfeature.LAND,facecolor='silver')

    m1=ax.pcolormesh(lons,lats,alcst[ii,:,:], cmap=cmap, vmin=vmin, vmax=vmax, transform=proj_pp)
    plt.colorbar(m1)
    title = times[ii].strftime('%Y %m %d')
    ax.set_title(title)
    plt.savefig('plots/alcs_'+title.replace(' ','')+'.png',dpi=190, bbox_inches='tight' )
    plt.close()




# Plot mean and std

time_average = np.mean(alcst,axis=0)
time_std     = np.std(alcst,axis=0)

fig = plt.figure(figsize=[11,8])
ax=plt.subplot(1,2,1, projection=ccrs.Orthographic(10,67))
    #ax.stock_img()
ax.coastlines(lw=.4)
#ax.add_feature(cfeature.LAND,facecolor='silver')

m2 = ax.pcolormesh(lons,lats,time_average, cmap=cmap, vmin=vmin2, vmax=vmax2, transform=proj_pp)
plt.colorbar(m2,location='bottom')
#title = 'Average {} - {}'.format(times[0].strftime('%Y %m %d'), times[-1].strftime('%Y %m %d'))
title = 'Average'
ax.set_title(title)



ax2=plt.subplot(1,2,2, projection=ccrs.Orthographic(10,67))
ax2.coastlines(lw=.4)
m2 = ax2.pcolormesh(lons,lats,time_std, cmap=cmap, vmin=vmin2, vmax=vmax2, transform=proj_pp)
plt.colorbar(m2,location='bottom')
#title2 = 'Std {} - {}'.format(times[0].strftime('%Y %m %d'), times[-1].strftime('%Y %m %d'))
title2 = 'Std'
ax2.set_title(title2)

title = '{} - {}'.format(times[0].strftime('%Y %m %d'), times[-1].strftime('%Y %m %d'))
plt.suptitle(title)


plt.savefig('plots/avgstd_'+title.replace(' ','')+'.png',dpi=190, bbox_inches='tight')



#plt.show()
