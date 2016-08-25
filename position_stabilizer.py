import numpy
import statistics

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
        lon_dev = numpy.std(self.longitude_measurments)
        lat_dev = numpy.std(self.latitude_measurments)
        if len(self.longitude_measurments) > self.min_measur_num:
            return True
        else:
            return False
