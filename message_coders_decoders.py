import re


class gprmc_position():
    def __init__(self, latitude, longitude, azimuth, azimuth_variation, gps_status):
        self.latitude = latitude
        self.longitude = longitude
        self.azimuth = azimuth
        self.azimuth_variation = azimuth_variation
        self.gps_status = gps_status

    def __eq__(self, other):
        a = abs(self.latitude - other.latitude) < 0.01
        b = abs(self.longitude - other.longitude) < 0.01
        c = abs(self.azimuth - other.azimuth) < 0.01
        d = abs(self.azimuth_variation - other.azimuth_variation) < 0.01
        e = self.gps_status == other.gps_status
        return a and b and c and d


def raise_if_device_address_is_wrong(address):
    # Type error should not be raised in this case, read and convert
    # Refractor this ugly if statement
    r = "[0-9A-Fa-f]{2}"
    result = re.search(r, address)
    if result and len(address) == 2:
        pass
    else:
        raise TypeError("wrong_device_address")


def raise_if_number_is_to_long_for_msg(num):
    # Type error should not be raised in this case, read and convert
    if num < 32001 and num > -32001:
        pass
    else:
        raise TypeError("position_out_of_range")


def rotate_to_position_msg(device_address_in_hex, position_in_steps):
    raise_if_device_address_is_wrong(device_address_in_hex)
    raise_if_number_is_to_long_for_msg(position_in_steps)
    if position_in_steps > 0:
        sign = "+"
    else:
        sign = ""
    return "$O" + device_address_in_hex + "W" + sign + str(position_in_steps) + "\n"


def move_up_down_msg(device_address_in_hex, position_in_steps):
    raise_if_device_address_is_wrong(device_address_in_hex)
    raise_if_number_is_to_long_for_msg(position_in_steps)
    header = "$O" + device_address_in_hex
    if (position_in_steps > 0):
        result = header + "U" + str(position_in_steps) + "\n"
    else:
        result = header + "D" + str(-position_in_steps) + "\n"

    return result


def reference_point_msg(device_address_in_hex):
    raise_if_device_address_is_wrong(device_address_in_hex)
    return "$O" + device_address_in_hex + "Z" + "\n"


def get_position_msg(device_address_in_hex):
    raise_if_device_address_is_wrong(device_address_in_hex)
    return "$O" + device_address_in_hex + "R" + "\n"


def sleep_msg(device_address_in_hex):
    raise_if_device_address_is_wrong(device_address_in_hex)
    return "$O" + device_address_in_hex + "S" + "\n"


def enable_device_msg(device_address_in_hex):
    raise_if_device_address_is_wrong(device_address_in_hex)
    return "$O" + device_address_in_hex + "E" + "\n"

def gprmc_position_request():
    return "$OGPRMC\n"

def decode_tilt_msg(msg):
    # add validation later
    # r = "\$O[0-9, a-f, A-F]{2}[+, -]{1}[0-9]{4}"
    # result = re.search(r, msg)
    # print "\n"
    # print "msg " + msg
    # print result.group(0)
    # print "\n"
    # if result and result.group(0) == msg:
    #     pass
    # else:
    #     raise TypeError("wrong string")
    return int(msg[5:])


def decode_gprmc_msg(msg):
    # add proper validation
    tokens = msg.split(",")
    gps_status = tokens[2]
    latitude_string = tokens[3]
    latitude_direction = tokens[4]
    longitude_string = tokens[5]
    longitude_direction = tokens[6]
    azimuth = tokens[8]
    azimuth_var = tokens[10]

    if azimuth_var == '':
        azimuth_var = "0"

    if latitude_string == '' or latitude_direction == '':
        latitude = 0
    else:
        latitude = nmea_latitude_to_degrees(latitude_string,
                                            latitude_direction)

    if longitude_direction == '' or longitude_string == '':
        longitude = 0
    else:
        longitude = nmea_longitude_to_degrees(longitude_string,
                                              longitude_direction)

    return gprmc_position(latitude, longitude,
                          float(azimuth), float(azimuth_var), gps_status)


def nmea_longitude_to_degrees(number, direction):
    r = "([0-9]{3})([0-9]{2})\.([0-9]{4})"
    result = re.search(r, number)
    if result and result.group(0) == number and ( direction == "W" or direction == "E"):
        pass
    else:
        raise TypeError("wrong string")

    degrees = float(result.group(1))
    minutes = float(result.group(2))
    minutes_tenth_of_thousand = float(result.group(3))
    result = degrees + (minutes + minutes_tenth_of_thousand / 10000) / 60 

    if direction == "W":
        result = result * -1

    return result


def nmea_latitude_to_degrees(number, direction):

    r = "([0-9]{2})([0-9]{2})\.([0-9]{4})"
    result = re.search(r, number)
    if result and result.group(0) == number and ( direction == "N" or direction == "S"):
        pass
    else:
        print direction
        raise TypeError("wrong string")

    degrees = float(result.group(1))
    minutes = float(result.group(2))
    minutes_tenth_of_thousand = float(result.group(3))
    result = degrees + (minutes + minutes_tenth_of_thousand / 10000) / 60 

    if direction == "S":
        result = result * -1

    return result
