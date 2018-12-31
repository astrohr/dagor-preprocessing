from requests import post
from bs4 import BeautifulSoup

def fetchData(mpc_str, obs_code='L01', start='', eph_num=4, eph_int=2, eph_unit='h', eph_pos='h', \
    mot_disp='m', mot_mode='t'):
    """
    Arguments:
        mpc_str: [string]  Normal format MPC measurements. 
        obs_code: [string] Observatory code. 
        start: [string] Starting date. 
        eph_num: [int] Number of ephemeris positions to output.
        eph_int: [int] Ephemeris interval. 
        eph_unit: [string] Ephemeris units ("d" for days, "h" for hours). 
        mot_disp: [string] Ephemeris position format ("h" for truncated sexagesimal, "a" for
            full sexagesimal, "d" for decimal)ž
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
    
    # Form return string
    ret_str = '\n'.join(soup.get_text().splitlines[11:-7])
    
    return ret_str

if __name__ == '__main__':

    mpc = """
         VXt0001 IC2018 12 29.84223807 13 13.25 +23 57 49.3          19.5 G      L01
         VXt0001*KC2018 12 29.86135807 13 11.30 +23 57 25.9          19.4 G      L01
         VXt0001 KC2018 12 29.86408107 13 11.04 +23 57 22.8          19.3 G      L01
    """
    soup = fetchData(mpc)
    print(soup)