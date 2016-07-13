import math as m

class Point:
    def __init__(self, latitude, longitude, height):
        #lat & lon in degrees, h in meters
        self.lat = latitude
        self.lon = longitude
        self.elev = height

A = Point(0.0, 0.0, 0.0)
B = Point(0.1, 0.1, 100)

def EarthRadiusMeters(latitudeRadians): #latitude is geodetic, i.e. that reported by GPS
    '''http://en.wikipedia.org/wiki/Earth_radius'''
    a = 6378137.0 #equatorial radius in meters
    b = 6356752.3 #polar meters in meters
    cos = m.cos(latitudeRadians)
    sin = m.sin(latitudeRadians)
    t1 = a**2 * cos
    t2 = b**2 * sin
    t3 = a * cos
    t4 = b * sin
    return m.sqrt ((t1**2 + t2**2) / (t3**2 + t4**2))

def GeocentricLatitude(lat):
    '''Convert geodetic latitude 'lat' to a geocentric latitude 'clat'.
    Geodetic latitude is the latitude as given by GPS.
    Geocentric latitude is the angle measured from center of Earth between a point and the equator.
    https://en.wikipedia.org/wiki/Latitude#Geocentric_latitude'''
    e2 = 0.00669437999014
    clat = m.atan((1.0-e2) * m.tan(lat))
    return clat

def LocationToPoint(c):
    '''Convert (lat, lon, elv) to (x, y, z).'''
    lat = c.lat
    lon = c.lon
    radius = EarthRadiusMeters(lat)
    clat = GeocentricLatitude(lat)

    cosLon = m.cos(lon)
    sinLon = m.sin(lon)
    cosLat = m.cos(clat)
    sinLat = m.sin(clat)
    x = radius * cosLon * cosLat
    y = radius * sinLon * cosLat
    z = radius * sinLat

    cosGLat = m.cos(lat)
    sinGLat = m.sin(lat)

    # We used geocentric latitude to calculate (x,y,z) on the Earth's ellipsoid.
    # Now we use geodetic latitude to calculate normal vector from the surface, to correct for elevation.
    nx = cosGLat * cosLon
    ny = cosGLat * sinLon
    nz = sinGLat

    x = x + c.elev * nx
    y = y + c.elev * ny
    z = z + c.elev * nz
    return {'x':x, 'y':y, 'z':z, 'radius':radius, 'nx':nx, 'ny':ny, 'nz':nz}

def Distance(ap, bp):
    dx = ap.x - bp.x
    dy = ap.y - bp.y
    dz = ap.z - bp.z
    return m.sqrt(dx**2 + dy**2 + dz**2)

def NormalizeVectorDiff(b, a):
    '''Calculate norm b-a, where norm divides a vector by its length to produce a unit vector'''
    dx = b.x - a.x
    dy = b.y - a.y
    dz = b.z - a.z
    dist2 = dx**2 + dy**2 + dz**2
    if dist2==0:
        return None
    dist = m.sqrt(dist2)
    return { 'x':(dx/dist), 'y':(dy/dist), 'z':(dz/dist), 'radius':1.0 }

def Calculate(a, b):
    ap = LocationToPoint(a)
    bp = LocationToPoint(b)
    distKm = 0.001 * Distance(ap, bp)

    bma = NormalizeVectorDiff(bp, ap)
    if bma!=None:
        #Calculate altitude, which is the angle above the horizon of B as seen from A.
        #Almost always, B will actually be below the horizon, so the altitude will be negative.
        #The dot product of bma and norm = cos(zenith_angle), and zenith_angle = (90 deg) - altitude.
        #So altitude = 90 - acos(dotprod).
        altitude = 90.0 - m.degrees(m.acos(bma.x*ap.nx + bma.y*ap.ny + bma.z*ap.nz))
        return altitude
    else:
        return "error"

Calculate(A, B)