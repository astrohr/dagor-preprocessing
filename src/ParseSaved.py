def raDeg2H(ra_str):
    """ Convert string representation of decimal right ascention to sexagesimal right ascention string. """

    ra_deg = float(ra_str)

    ra_h = int(ra_deg/15)
    ra_m = int((ra_deg - 15*ra_h)*4)
    ra_s = (4*ra_deg - 60*ra_h - ra_m)*60

    return ' '.join(list(map(str, [ra_h, ra_m, ra_s])))


def decDec2Sim(dec_str):
    """ Convert string representation of decimal declination to sexagesimal declination string. """

    dec_deg = float(dec_str)

    if dec_deg > 0:
        init = '+'
    else:
        init = '-'

    dec_degs = int(dec_deg)
    dec_min = (dec_deg - dec_degs) * 60
    dec_mins = int(dec_min)
    dec_secs = int(dec_min - dec_mins)

    return init + ' '.join(list(map(str, [dec_degs, dec_mins, dec_secs])))


if __name__ == '__main__':

    print(raDeg2H(107.50161))
    print(decDec2Sim(23.748603))