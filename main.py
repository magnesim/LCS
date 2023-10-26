from ParticleAdvector import Advection
from LCS import FTLE
import xarray as xr
import numpy as np
#from joblib import Parallel, delayed

def _mkdir(member):
    """
        Creates a directory "store_file/member{member}"
        store_file is specified in the __name__=='__main__' part of the script.
    Args:
        member  [int]   :   the ensemble member
    """
    import os
    if not os.path.exists(store_file):
        os.mkdir(store_file)
    if not os.path.exists(f'{store_file}/member{member}'):
        os.mkdir(f'{store_file}/member{member}')

def CreateLCSField(lons, lats, ts, sep, dur, date, member, output, at_time=0, model=None):
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
    advector = Advection(lons, lats, ts, sep, dur, date, at_time, model=model)
    outfile = advector.displace_one_member(member, output)
    LCS = xr.open_dataset(FTLE(f'{output}.nc', f'{output}_LCS'))
    

def Run(i, date, at_time=0, model=None):
    """
        Runs the particle and LCS simulation
    Args:
        i       [int]   :   The ensemble member for which LCSs should be computed
        date    [str]   :   A string of the date, in format 'ymd', no spacings.
        at_time [int]   :   Which hour of the day LCSs are computed for
    """
    output=f'{store_file}/member{i}/{date}_h{at_time}_{model}'
#    CreateLCSField(lons=[4.5,23], lats=[67,69.9], ts=-3600, sep=1000, dur=24, date=date, member=i, output=output, at_time=at_time)
    if model=='norkyst' or model=='barents':
        CreateLCSField(lons=[7.8, 20.5], lats=[66.7,69.9], ts=-3600, sep=1000, dur=6, date=date, member=i, output=output, at_time=at_time, model=model)
    else:
        CreateLCSField(lons=[12.9, 12.8], lats=[66.1,69.0], ts=-3600, sep=1000, dur=6, date=date, member=i, output=output, at_time=at_time)

if __name__ == '__main__':
    """
    import os
    for i in range(24):
        os.mkdir(f'logs/ALCS_files_2h_april/member{i}')
    """
    store_file = 'ALCS_jun'
    import sys
    sel = int(sys.argv[1])
    #sel = 1
    dates = [f'202306{d:02d}' for d in range(1,10)]
#    dates = ['20230627']
    model = 'norkyst'
#    model = 'barents' 

#
#     curr_date = dates[sel-1]
    
    for curr_date in dates:
        Run(0, curr_date, model=model)
    
    #for i in range(6):
    #    Run(i, curr_date)
    
    
    #Run(0, '20221210')
    """
    for t in times:
        for i in range(24):
            Run(i, int(t), curr_date)
    """