import os
from astropy.coordinates import ICRS
from astropy import units

def decimalToTele(ra_str, dec_str):
    """ Convert a decimal string representation of equatorial coordinates to truncated sexagesimal. """

    ra_deg = float(ra_str)
    dec_deg = float(dec_str)

    coord = ICRS(ra_deg*units.degree, dec_deg*units.degree)

    ra_tele = str(coord.ra.to_string(units.hour, sep=' ', precision=1))
    dec_tele = str(coord.dec.to_string(units.degree, sep=' ', alwayssign=True, precision=0))

    return ra_tele, dec_tele

def parseRaw(raw_dir, raw_name, final_dir, final_name):
    """ Parse the raw file containing the saved imaging coordinates. """

    raw_fname = os.path.join(raw_dir, raw_name)
    final_fname = os.path.join(final_dir, final_name)

    with open(raw_fname, 'r') as raw, open(final_fname, 'w+') as final:

        for raw_line in raw:
            name_str, ra_str, dec_str = raw_line.lstrip().split(" ")
            ra_tele, dec_tele = decimalToTele(ra_str, dec_str)
            final.write('* ' + name_str + '\n')
            final.write('2018 12 30 2130   ' + ra_tele + ' ' + dec_tele + '\n')


if __name__ == '__main__':

    print(decimalToTele('107.50161', '23.748603'))

    raw_dir, raw_name = '../data/', 'saved_coordinates.txt'
    final_dir, final_name = '../data/', 'saved_coord_telescope.txt'

    parseRaw(raw_dir, raw_name, final_dir, final_name)