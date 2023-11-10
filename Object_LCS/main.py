from ParticleAdvector import AdvectionBarentsEPS, Advection
from LCS import FTLE
import xarray as xr
import numpy as np
#from joblib import Parallel, delayed
import os
from datetime import datetime, timedelta
from postproc import postproc #plot_single_day

def _mkdir(member):
    """
        Creates a directory "store_file/member{member}"
        store_file is specified in the __name__=='__main__' part of the script.
    Args:
        member  [int]   :   the ensemble member
    """
    if not os.path.exists(store_file):
        os.mkdir(store_file)
    if not os.path.exists(f'{store_file}/member{member}'):
        os.mkdir(f'{store_file}/member{member}')

def CreateLCSField(lons, lats, ts, sep, dur, date, member, output, at_time=0):
    """
        Advects particles using ParticleAdvector.py, which creates an output file.
        Uses this output file to compute LCSs. 
    Args:
        lons    [list]      :   A list [lon1, lon2], where lon1 is bottom left corner of domain and lon2 is top right corner of domain. 
        lats    [list]      :   A list [lat1, lat2], where lat1 is bottom left corner of domain and lat2 is top right corner of domain.
        ts      [float]     :   Time step for integration, given in seconds
        sep     [int]       :   Initial separation between particles, given in meters.
        dur     [int]       :   Duration of integration, given in hours
        date    [str]       :   A string of the date, in format 'ymd', no spacings.
        member  [int]       :   Number of ensemble member, between 0-23.
        output  [str]       :   Name of output file. Particle positions are saved to output.nc, LCS are saved to output_LCS.nc
        at_time [int]       :   Which hour of the day LCSs are computed for
    """
    _mkdir(member)
#    advector = AdvectionBarentsEPS(lons, lats, ts, sep, dur, date, at_time)
#    outfile = advector.displace_one_member(member, output)
#    print('date',date)
#    start = datetime.strptime(date,'%Y%m%d')
    start = timedelta(hours=at_time)
#    print('start',start)
    file = 'https://thredds.met.no/thredds/dodsC/fou-hi/norkyst800m-1h/NorKyst-800m_ZDEPTHS_his.an.{}00.nc'.format(date)
#    file = '/lustre/storeB/project/fou/hi/new_norkyst/his/ocean_his.an.{}.nc'.format(date)
    advector = Advection(file, lons, lats, ts, sep, dur, start=start)
    try:
        ftle = advector.run(output)
    except Exception:
        print('## Warning: Skipping file: \n', file)
        return
#    LCS = xr.open_dataset(FTLE(f'{output}.nc', f'{output}_LCS'))
    LCS = FTLE(ftle, f'{output}_LCS',example_model_file=file)
    os.remove(f'{output}.nc')

def Run(i, date, at_time=24):
    """
        Runs the particle and LCS simulation
    Args:
        i       [int]   :   The ensemble member for which LCSs should be computed
        date    [str]   :   A string of the date, in format 'ymd', no spacings.
        at_time [int]   :   Which hour of the day LCSs are computed for
    """
    output=f'{store_file}/member{i}/{date}_h{at_time}-{dur}'
#    CreateLCSField(lons=[4.5,23], lats=[67,69.9], ts=-3600, sep=1000, dur=24, date=date, member=i, output=output, at_time=at_time)
    #CreateLCSField(lons=[23.5, 26.4], lats=[69.6, 72.6], ts=-3600, sep=sep, dur=dur, date=date, member=i, output=output, at_time=at_time)
    

    if member==0:
        # Finnmark domain
        CreateLCSField(lons=[28.0, 27.], lats=[68.2, 73.], ts=-3600, sep=sep, dur=dur, date=date, member=i, output=output, at_time=at_time)
    elif member==1:
        # Troms domain
        CreateLCSField(lons=[19.2, 19.0], lats=[68.3, 72.0], ts=-3600, sep=sep, dur=dur, date=date, member=i, output=output, at_time=at_time)
    elif member==2:
        # Nordland domain
        CreateLCSField(lons=[13.4, 12.5], lats=[65.7, 69.9], ts=-3600, sep=sep, dur=dur, date=date, member=i, output=output, at_time=at_time)


if __name__ == '__main__':
    """
    """
    import sys
    from glob import glob
    import os.path


    # Folder to store nc files
    store_file = '../data/ncfiles'
 
    # Parameters    
    at_time = 23   # time when the LCS field is valid
    dur = 12        # delta t for LCS computation
    sep = 600

    member = 0 # Finnmark
    #member = 1 # Troms
    #member = 2 # Nordland



    # List of dates in string format ['YYYYMMDD']
#    dates = [f'202303{d:02d}' for d in range(20,31)]
    #dates = ['20230628']
    d0 = datetime(2023,3,1)
    dates = [(d0 + timedelta(days=i)).strftime('%Y%m%d') for i in range(0,30)]
    print('***\n Processing dates: \n',dates,'\n****')

    # Run the LCS analysis
    #for curr_date in dates:
    #    Run(member, curr_date, at_time)



    
    


    # POST PROCESSING

    tag = f'h{at_time}-{dur}'

    files = np.array([f'{store_file}/member{member}/{item}_{tag}_LCS.nc' for item in dates])
    files = files[ np.where([os.path.exists(item) for item in files])[0] ]

    if len(files)==0:
        print('no files available... ')
        exit()

    tag+='_{:02d}'.format(member)
    outdir = '../data/plots'
    postproc(files, outdir, tag=tag, single=False, average=True)


