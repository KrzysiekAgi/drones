import math as m

def azimuth(lat_an, lon_an, lat_dr, lon_dr):
	Earth_radius = 6371000
	a_rad = m.radians(90-lat_dr)
	c_rad = m.radians(90-lat_an)
	B = m.radians(lon_dr - lon_an)
	b_rad = m.acos(m.cos(a_rad)*m.cos(c_rad) + m.sin(a_rad)*m.sin(c_rad)*m.cos(B))
	A = m.asin(m.sin(a_rad)*(m.sin(B)/m.sin(b_rad)))
	az = m.degrees(A)
	if az >= 0:
		return az
	else: 
		return az + 360

#def azimuth(lat_an, lon_an, lat_dr, lon_dr):
	#lat_an_rad = m.radians(lat_an)
	#lon_an_rad = m.radians(lon_an)
	#lat_dr_rad = m.radians(lat_dr)
	#lon_dr_rad = m.radians(lon_dr)
	#f = 1/298.257223563
	#e_sq = f*(2-f)
	#b = (1-f)**2    # 1-e**2
	#fi_1 = b*(m.tan(lat_dr_rad)/m.tan(lat_an_rad))
	#fi_2 = e_sq*m.sqrt((1+b*(m.tan(lat_dr_rad)**2))/(1+b*(m.tan(lat_an_rad))**2))
	#fi = fi_1 + fi_2
	#az = m.atan2(m.sin(lon_dr_rad),(fi-m.cos(lon_dr_rad)*m.sin(lat_an_rad)))
	#return az