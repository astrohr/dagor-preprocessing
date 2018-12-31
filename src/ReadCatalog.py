import os
import numpy as np

def loadGaiaCatalog(dir_path, file_name, lim_mag=None, ra_min=None, ra_max=None, dec_min=None, dec_max=None):
    """ Read star data from the GAIA catalog in the .npy format. 
    
    Arguments:
        dir_path: [str] Path to the directory where the catalog file is located.
        file_name: [str] Name of the catalog file.
    Keyword arguments:
        lim_mag: [float] Faintest magnitude to return. None by default, which will return all stars.
        ra_min: [float] Minimum right ascention to return. If None, returns all stars. 
        ra_max: [float] Maximum right ascention to return. If None, returns all stars. 
        dec_min: [float] Minimum declination to return. If None, returns all stars. 
        dec_max: [float] Maximum declination to return. If None, returns all stars. 
    Return:
        results: [2d ndarray] Rows of (ra, dec, mag), angular values are in degrees.
    """

    file_path = os.path.join(dir_path, file_name)

    # Read the catalog
    results = np.load(file_path, allow_pickle=False)


    # Filter by limiting magnitude
    if lim_mag is not None:

        results = results[results[:, 2] < lim_mag]

    # Filter by right ascention and declination
    if None not in [ra_min, ra_max, dec_min, dec_max]:
        
        results = results[(results[:, 0] > ra_min) & (results[:, 0] < ra_max) & \
            (results[:, 1] > dec_min) & (results[:, 1] < dec_max)]


    # Sort stars by descending declination
    results = results[results[:,1].argsort()[::-1]]

    return results

    