import math as m

def azimuth(lat_an, lon_an, lat_dr, lon_dr):
	Earth_radius = 6371000
	a_rad = m.radians(90-lat_dr)
	c_rad = m.radians(90-lat_an)
	B = m.radians(lon_dr - lon_an)
	b_rad = m.acos(m.cos(a_rad)*m.cos(c_rad) + m.sin(a_rad)*m.sin(c_rad)*m.cos(B))
	A = m.asin(m.sin(a_rad)*(m.sin(B)/m.sin(b_rad)))
	az = m.degrees(A)
	return az
    