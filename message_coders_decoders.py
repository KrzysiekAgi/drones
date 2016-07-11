
class rmc_position():
    def __init__(self, latitude, longitude, azimuth, azimuth_variation):
        self.latitude = latitude
        self.longitude = longitude
        self.azimuth = azimuth
        self.azimuth_variation = azimuth_variation

def rotate_to_position_msg(device_address_in_hex, position_in_steps):
    return "ble"

def move_up_down_msg(device_address_in_hex, position_in_steps):
    return "ble"

def reference_point_msg(device_address_in_hex):
    return "ble"

def get_position_msg(device_address_in_hex):
    return "ble"

def sleep_msg(device_address_in_hex):
    return "ble"

def enable_device_msg(device_address_in_hex):
    return "ble"

def decode_tilt_msg(msg):
    return -23432

def decode_gprmc_msg(msg):
    rmc_position(1, 1, 1, 1)