import math as m

def cart2pol3d(x, y, z, xx, yy, zz): #xx etc. being anthen
	r = sqrt((x-xx)**2+(y-yy)**2+(z-zz)**2)
	az = m.degrees(m.atan2(y-yy, x-xx)) #flat
	elev = m.degrees(m.acos((z-zz)/r) #height
	return (az, elev)

print cart2pol3d(4, 6, 10, -1, -2, 5)

