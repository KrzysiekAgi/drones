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


def circle_dist(lat_a, lon_a, lat_b, lon_b):
    '''https://en.wikipedia.org/wiki/Great-circle_distance#Computational_formulas
    korzystam z tego bardziej skomplikowanego wzoru, ale dokadnego dla wszystkich odleglosci'''
    lat_an_rad = m.radians(lat_a)
    lat_dr_rad = m.radians(lat_b)
    lon_diff_rad = m.radians(lon_b - lon_a)
    num_part_1 = (m.cos(lat_dr_rad) * m.sin(lon_diff_rad))**2
    num_part_21 = m.cos(lat_an_rad) * m.sin(lat_dr_rad)
    num_part_22 = m.sin(lat_an_rad) * m.cos(lat_dr_rad) * m.cos(lon_diff_rad)
    num_part_2sq = (num_part_21 - num_part_22)**2
    numerator = m.sqrt(num_part_1 + num_part_2sq)
    denom_1 = m.sin(lat_an_rad) * m.sin(lat_dr_rad)
    denom_2 = m.cos(lat_an_rad) * m.cos(lat_dr_rad) * m.cos(lon_diff_rad)
    denominator = denom_1 + denom_2
    D = m.atan2(numerator, denominator)
    return D


def elevation(lat_an, lon_an, h_an, lat_dr, lon_dr, h_dr):
    D = circle_dist(lat_an, lon_an, lat_dr, lon_dr)
    R_dr = 6378137.0 + h_dr
    R_an = 6378137.0 + h_an
    distance_sq = (R_an) ** 2 + (R_dr) ** 2 - 2 * R_an * R_dr * m.cos(D)
    distance = m.sqrt(distance_sq)
    cos_beta = (R_dr ** 2 - R_an ** 2 - distance_sq)/(2 * R_an * distance)
    return 90 - m.degrees(m.acos(cos_beta)) 
