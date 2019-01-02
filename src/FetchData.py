import os
import time
import numpy as np
from requests import get, post
from bs4 import BeautifulSoup
from astropy.time import Time


def fetchData(mpc_str, obs_code='L01', start='', eph_num=4, eph_int=2, eph_unit='h', eph_pos='d', \
    mot_disp='d', mot_mode='t'):
    """
    Arguments:
        mpc_str: [string]  Normal format MPC measurements. 
        obs_code: [string] Observatory code. 
        start: [string] Starting date. 
        eph_num: [int] Number of ephemeris positions to output.
        eph_int: [int] Ephemeris interval. 
        eph_unit: [string] Ephemeris units ("d" for days, "h" for hours). 
        eph_pos: [string] Ephemeris position format ("h" for truncated sexagesimal, "a" for
            full sexagesimal, "d" for decimal)
        mot_disp: [string] How the miotion is displayed. "s" for "/sec, "m" for "/min, "h" for "/h, 
            "d" for deg/day 
        mot_mode: [string] Motion display mode ("t" for total motion and direction, "s" for
            separate. )
    Returns:
        ret_str: [string] Return string (pure text extracted from the website). 
    """

    # Init post dictionary
    params = {
        "TextArea": mpc_str,
        "o": obs_code, 
        "d": start,
        "l": str(eph_num), 
        "i": str(eph_int),
        "u": eph_unit, 
        "raty": eph_pos, 
        "m1": mot_disp, 
        "m2": mot_mode 
    }

    # The url from which the data is gathered
    url = "https://cgi.minorplanetcenter.net/cgi-bin/newobjephems.cgi"
    
    # Request data
    req = post(url, data=params)
    
    # Create soup
    soup = BeautifulSoup(req.text, "html5lib")

    # Get start of measurements
    lines = soup.get_text().splitlines()

    for i, line in enumerate(lines):
        if line.startswith('Object'):
            line_ind = i
            break
    

    # Check if there is a warning string
    lines = lines[line_ind:-7]

    if lines[1].startswith('This'):
        for i in range(2):
            del lines[1]

    # Form return string
    ret_str = '\n'.join(lines)

    print(ret_str)
    
    return ret_str

def saveData(ret_str, save_dir, save_name):
    """ Writes a string to a file. """

    filename = os.path.join(save_dir, save_name)

    with open(filename, 'w+') as file:
        file.write(ret_str.encode('utf-8'))


def loadData(data_dir, data_name):
    """ Loads all data from a file to a string. """

    filename = os.path.join(data_dir, data_name)

    with open(filename, 'r') as file:
        lines = file.readlines()

    return ''.join(lines)

def sData2Query(data_dir, data_name, save_dir, save_name):

    print("Loading MPC data...")
    mpc_str = loadData(data_dir, data_name)
    
    print("Fetching ephemeris query from IAU MPC...")
    ret_str = fetchData(mpc_str)

    print("Saving query results...")
    saveData(ret_str, save_dir, save_name)

def getUrl(object_i):

    cur_time = time.time()
    astro_time = Time(cur_time, format='unix')
    jd = astro_time.jd

    url = 'https://cgi.minorplanetcenter.net/cgi-bin/uncertaintymap.cgi?Obj=' + \
        object_i + '&JD=' + str(jd) + '&Form=Y&Ext=VAR&OC=000&META=apm00'

    return url


def getUncertainties(object_i):

    url = getUrl(object_i)

    req = get(url)

    soup = BeautifulSoup(req.text, 'html5lib')

    out_arr = []

    for line in soup.get_text().splitlines()[8:-4]:

        line_spl = line.split()

        ra_off = int(str(line_spl[0]))
        dec_off = int(str(line_spl[1]))

        sign = str(line_spl[-1])

        ra_off, dec_off = map(lambda x: float(x)/3600, [ra_off, dec_off])

        out_arr.append([ra_off, dec_off, sign])

    # Convert to numpy array
    out_arr = np.asarray(out_arr)

    return out_arr

if __name__ == '__main__':


    data_dir, data_name = '../data/', 'mpc_data.txt'
    save_dir, save_name = '../data/', 'query_results.txt'

    # sData2Query(data_dir, data_name, save_dir, save_name)

    uncertainties = getUncertainties('ZTF025s')

    print(uncertainties)