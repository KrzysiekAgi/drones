import subprocess
import serial
import io
from message_coders_decoders import decode_gprmc_msg, get_position_msg
from math_utils.intelligence import where_to_move_absolute


def find_device_name_of_serial():
    output = subprocess.Popen(["bash", "find_ftdi.sh"], stdout=subprocess.PIPE).communicate()[0]
    # improve checking
    if len(output) < 8:
        raise Exception("no serial device is attached")

    return output.strip()


def get_serial_object_for_rotor():
    device_name = find_device_name_of_serial()
    ser = serial.Serial(device_name, 9600, timeout=1)
    return ser


def open_port_and_get_position():
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    sio.write(unicode("$GPRMC\n"))
    sio.flush()
    h = sio.readline()
    ser.close()
    resp = decode_gprmc_msg(h.strip())
    return resp


def move_to_expected_azimuth(expected):
    current = get_horizontal_position()
    d = float(current) / 14300.0 * 360
    t = where_to_move_absolute(expected, d)
    move_to_azimuth(d + t)


def get_horizontal_position():
    string = open_port_send_msg_get_response(unicode(get_position_msg("10")))
    return string[5:]


def move_to_azimuth(expe):
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    expect_steps = degrees_to_steps_for_horizontal(expe)
    msg = unicode("$O10W" + str(expect_steps) + "\n")
    sio.write(unicode(msg))
    sio.flush()
    ser.close()


def open_port_send_msg_get_response(msg):
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    sio.write(msg)
    sio.flush()
    h = sio.readline()
    ser.close()
    return h.strip()


def degrees_to_steps_for_horizontal(degrees):
    return 14300.0 * (degrees / 360.0)

