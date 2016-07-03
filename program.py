import math as m


def azimuth(lat_an, lat_dr, lon_an, lon_dr):
    numerator = m.sin(lon_dr)
    denominator = m.cos(lat_an) * m.tan(lat_dr) - m.sin(lat_an) * m.cos(lon_dr)
    azimuth_in_radians = m.atan(numerator / denominator)
    azimuth_in_degrees = m.degrees(azimuth_in_radians)
    return azimuth_in_degrees


def elevation(lat_an, lat_dr, h_drone, lon_an, lon_dr):
    '''source: https://en.wikipedia.org/wiki/Azimuth
    https://pl.wikipedia.org/wiki/Ortodroma
    fi1 - site's latitude, fi2 - drone's latitude,
    L2 - dron's longitude,
    L1 - site's longitude being equal to 0 (?), H - drone's hight in km'''
    some_radians = m.acos(m.sin(lat_an) * m.sin(lat_dr) + m.cos(lat_an) * m.cos(lat_dr) * m.cos(lon_dr - lon_an))
    arch_len = 111.195 * m.degrees(some_radians)  # in km
    alfa = (360 * arch_len) / (2 * m.pi * 6378.41)
    r = 6378.41
    r_pow = r ** 2
    leng = m.sqrt(r_pow * 2 - 2 * r_pow * m.cos(alfa))  # in km
    elev = m.asin(h_drone / leng)
    return elev

