import math as m

def az_elev2(fi1, fi2, L1, L2, H):
    '''source: https://en.wikipedia.org/wiki/Azimuth
    https://pl.wikipedia.org/wiki/Ortodroma
    fi1 - site's latitude, fi2 - drone's latitude, L2 - dron's longitude, L1 - site's longitude being equal to 0 (?), H - drone's hight in km'''
    az = m.degrees(m.atan(m.sin(L2)/(m.cos(fi1)*m.tan(fi2)-m.sin(fi1)*m.cos(L2) ) ) )
    arch_len = 111.195*m.degrees(m.acos(m.sin(fi1)*m.sin(fi2)+m.cos(fi1)*m.cos(fi2)*m.cos(L2-L1))) #in km
    alfa = (360*arch_len)/(2*m.pi*6378.41)
    #leng = arch length on flat
    leng = m.sqrt(6378.41**2 + 6378.41**2 -2*6378.41*6378.41*m.cos(alfa) ) #in km
    elev = m.asin(H/leng)
    return az, elev


def az_elev(S, N, L): 
    '''S - drone's longitude, N - site's longitude, L - site's latitude
    source: http://tiij.org/issues/issues/3_2/3_2e.html 
    I think it works only for geostationary satelite'''	
    G = S - N
    elev = m.degrees(m.atan((m.cos(G)*m.cos(L) - 0.1512)/(m.sqrt(1-m.cos(G)*m.cos(G)*m.cos(L)*m.cos(L)))))
    az = m.degrees(180+m.atan(m.tan(G)/m.sin(L)))
    return elev, az


print az_elev2(15, 30, 0, 20, 2)
