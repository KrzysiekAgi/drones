import math as m


def azimuth(fi1, fi2, L1, L2, H):
    numerator = m.sin(L2)
    denominator = m.cos(fi1) * m.tan(fi2) - m.sin(fi1) * m.cos(L2)
    azimuth_in_radians = m.atan(numerator / denominator)
    azimuth_in_degrees = m.degrees(azimuth_in_radians)
    return azimuth_in_degrees


def elevation(fi1, fi2, L1, L2, H):
    '''source: https://en.wikipedia.org/wiki/Azimuth
    https://pl.wikipedia.org/wiki/Ortodroma
    fi1 - site's latitude, fi2 - drone's latitude,
    L2 - dron's longitude,
    L1 - site's longitude being equal to 0 (?), H - drone's hight in km'''
    some_radians = m.acos(m.sin(fi1) * m.sin(fi2) + m.cos(fi1) * m.cos(fi2) * m.cos(L2 - L1))
    arch_len = 111.195 * m.degrees(some_radians)  # in km
    alfa = (360 * arch_len) / (2 * m.pi * 6378.41)
    r = 6378.41
    r_pow = r ** 2
    leng = m.sqrt(r_pow * 2 - 2 * r_pow * m.cos(alfa))  # in km
    elev = m.asin(H / leng)
    return elev


def az_elev(S, N, L): 
    '''S - drone's longitude, N - site's longitude, L - site's latitude
    source: http://tiij.org/issues/issues/3_2/3_2e.html 
    I think it works only for geostationary satelite'''	
    G = S - N
    elev = m.degrees(m.atan((m.cos(G)*m.cos(L) - 0.1512)/(m.sqrt(1-m.cos(G)*m.cos(G)*m.cos(L)*m.cos(L)))))
    az = m.degrees(180+m.atan(m.tan(G)/m.sin(L)))
    return elev, az


print elevation(15, 30, 0, 20, 2)
print azimuth(15, 30, 0, 20, 2)
