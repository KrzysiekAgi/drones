import serial
import io
import subprocess
from message_coders_decoders import move_up_down_msg, gprmc_position_request
from message_coders_decoders import decode_gprmc_msg
import time
import numpy
import geography
from intelligence import where_to_move


def find_device_name_of_serial():
    output = subprocess.Popen(["bash", "find_ftdi.sh"], stdout=subprocess.PIPE).communicate()[0]
    # improve checking
    if len(output) < 8:
        raise Exception("no serial device is attached")

    return output.strip()


def get_serial_object_for_rotor():
    device_name = find_device_name_of_serial()
    print device_name
    ser = serial.Serial(device_name, 9600, timeout=1)
    return ser


def open_port_send_msg_get_response(msg):
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    sio.write(msg)
    sio.flush()
    h = sio.readline()
    ser.close()
    return h.strip()


def send_and_receive_gprmc(sio):
    sio.write(unicode("$GPRMC\n"))
    sio.flush()
    time.sleep(0.5)
    h = sio.readline()
    return h.strip()


def move_horizontaly(steps):
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    sio.write(unicode(move_up_down_msg("10", steps)))
    sio.flush()
    ser.close()


def degrees_to_steps_for_horizontal(degrees):
    return 14300.0 * (degrees / 360.0)


def open_port_and_get_position():
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    sio.write(unicode("$GPRMC\n"))
    sio.flush()
    h = sio.readline()
    print h
    ser.close()
    resp = decode_gprmc_msg(h.strip())
    return resp


def open_port_and_get_horizontal_position():
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


def prog():
    antenna_position = open_port_and_get_position()
    if antenna_position.gps_status == "A":
        a = geography.azimuth(antenna_position.latitude,
                          antenna_position.longitude,
                          51.1186668,
                          17.0121249)
        desired_azimuth = where_to_move(a, antenna_position.azimuth)
        move_horizontaly(degrees_to_steps_for_horizontal(desired_azimuth))
    else:
        print "cannot determine antenna location"


if __name__ == "__main__":
    prog()