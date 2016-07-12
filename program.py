import math as m


def azimuth(lat_an, lon_an, lat_dr, lon_dr):
    numerator = m.sin(m.radians(lon_dr))
    denominator = m.cos(m.radians(lat_an)) * m.tan(m.radians(lat_dr)) - m.sin(m.radians(lat_an)) * m.cos(m.radians(lon_dr))
    azimuth_in_radians = m.atan2(denominator, numerator)
    azimuth_in_degrees = m.degrees(azimuth_in_radians)
    if azimuth_in_degrees >= 0: 
        return azimuth_in_degrees
    else:
        return azimuth_in_degrees + 360


def elevation(lat_an, lon_an, h_an, lat_dr, lon_dr, h_drone):
    '''source: https://en.wikipedia.org/wiki/Azimuth
    https://pl.wikipedia.org/wiki/Ortodroma'''
    some_radians = m.acos(m.sin(m.radians(lat_an)) * m.sin(m.radians(lat_dr)) + m.cos(m.radians(lat_an)) * m.cos(m.radians(lat_dr)) * m.cos(m.radians(lon_dr - lon_an)))
    arch_len = 111.195 * m.degrees(some_radians)  # in km
    alfa = (360 * arch_len) / (2 * m.pi * 6378.41)
    r = 6378.41
    r_pow = r ** 2
    leng = m.sqrt(r_pow * 2 - 2 * r_pow * m.cos(alfa))  # in km
    elev = m.asin(h_drone / leng)
    return elev