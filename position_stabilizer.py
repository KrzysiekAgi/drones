import numpy
import geography


def clac_error_and_pos(measur_list):
    lon_list, lat_list = get_lon_lat_list(measur_list)
    # this function will not work near poles
    lon_dev = numpy.std(lon_list)
    lat_dev = numpy.std(lat_list)
    lon = numpy.mean(lon_list)
    lat = numpy.mean(lat_list)
    lat_2 = lat + lat_dev
    lon_2 = lon + lon_dev
    error_rad = geography.circle_dist(lat, lon, lat_2, lon_2)
    error_met = error_rad * 6371 * 1000
    return {"lon": lon, "lat": lat, "err": error_met}


def remove_big_errors(measur_list):
    result = []
    p_and_e = clac_error_and_pos(measur_list)
    print p_and_e["err"]
    for m in measur_list:
        lat_1 = p_and_e["lat"]
        lon_1 = p_and_e["lon"]
        lat_2 = m["lat"]
        lon_2 = m["lon"]
        c_dist = geography.circle_dist(lat_1, lon_1, lat_2, lon_2)
        m_dist = c_dist * 6371 * 1000
        print str(m_dist) + "\t" + str(p_and_e["err"])
        err = max(p_and_e["err"], 0.1)
        if m_dist <= err:
            result.append(m)

    return result


def get_lon_lat_list(measur_list):
    lon_list = [x["lon"] for x in measur_list]
    lat_list = [x["lat"] for x in measur_list]
    return lon_list, lat_list


class position_stabilizer():
    def __init__(self, accuracy_in_meters, min_measur_num):
        self.accuracy = accuracy_in_meters
        self.min_measur_num = min_measur_num
        self.measur_list = []

    def get_position(self):
        lon_list, lat_list = get_lon_lat_list(self.measur_list)
        lon = numpy.mean(lon_list)
        lat = numpy.mean(lat_list)
        return {"lat": lat, "lon": lon}

    def add_measurment(self, lat, lon):
        self.measur_list.append({"lat": lat, "lon": lon})

    def is_ready(self):
        enough_measurments = len(self.measur_list) > self.min_measur_num
        if not enough_measurments:
            return False

        self.measur_list = remove_big_errors(self.measur_list)
        p_and_e = clac_error_and_pos(self.measur_list)

        is_accurate = self.accuracy > p_and_e["err"]
        if is_accurate:
            return True
        else:
            return False
