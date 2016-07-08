import math as m

def azimuth(lat_an, lon_an, lat_dr, lon_dr):
    '''lat_an being X1 and lat_dr being X2'''
    azimuth = m.degrees(m.atan2(m.radians(lat_dr - lat_an),m.radians(lon_dr - lon_an)))
    if azimuth > 0 or azimuth ==0:
        return azimuth
    else:
        return azimuth + 360

print azimuth(0, 0, 0, 1)
