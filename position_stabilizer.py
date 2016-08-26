import numpy
import geography

class position_stabilizer():
    def __init__(self, accuracy_in_meters, min_measur_num):
        self.accuracy = accuracy_in_meters
        self.min_measur_num = min_measur_num
        self.longitude_measurments = []
        self.latitude_measurments = []

    def get_position(self):
        lon = numpy.mean(self.longitude_measurments)
        lat = numpy.mean(self.latitude_measurments)
        return {"lat": lat, "lon": lon}

    def add_measurment(self, lat, lon):
        self.longitude_measurments.append(lon)
        self.latitude_measurments.append(lat)

    def is_ready(self):
        enough_measurments = len(self.longitude_measurments) > self.min_measur_num
        if not enough_measurments:
            return False

        lon_dev = numpy.std(self.longitude_measurments)
        lat_dev = numpy.std(self.latitude_measurments)
        lon = numpy.mean(self.longitude_measurments)
        lat = numpy.mean(self.latitude_measurments)
        lat_2 = lat + lat_dev
        lon_2 = lon + lon_dev
        error_rad = geography.circle_dist(lat, lon, lat_2, lon_2)
        error_met = error_rad * 6371 * 1000

        is_accurate = self.accuracy > error_met
        if is_accurate:
            return True
        else:
            return False
