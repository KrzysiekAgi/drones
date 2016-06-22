import math as m

def cart2pol3d(x, y, z, xx, yy, zz): #xx etc. being anthen
	fi = m.degrees(m.atan2(y-yy, x-xx)) #flat
	elev = m.degrees(m.atan2(z-zz, m.sqrt((x-xx)**2+(y-yy)**2))) #height
	return fi, elev

print cart2pol3d(4, 6, 10, 1, 2, 5)

