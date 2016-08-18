import serial
import io
import subprocess
from message_coders_decoders import move_up_down_msg, gprmc_position_request
from message_coders_decoders import decode_gprmc_msg, get_position_msg
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
    ser = serial.Serial(device_name, 9600, timeout=1)
    return ser

def enable_vertical():
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    msg = unicode(move_up_down_msg("11", steps))
    sio.write(unicode(msg))
    sio.flush()
    ser.close()

def move_vertical(steps):
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    msg = unicode(move_up_down_msg("11", steps))
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
    ser.close()
    resp = decode_gprmc_msg(h.strip())
    return resp


def open_port_and_get_horizontal_position():
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


def get_horizontal_position():
    string = open_port_send_msg_get_response(unicode(get_position_msg("10")))
    return string[5:]

def move_to_azimuth(expe):
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    expect_steps = degrees_to_steps_for_horizontal(expe)
    msg = unicode("$O10W" + str(expect_steps)  + "\n")
    sio.write(unicode(msg))
    sio.flush()
    ser.close()

def move_to_expected_azimuth(expected):
    current = get_horizontal_position()
    d = float(current)/14300.0 *360
    t  = where_to_move(expected, d)
    move_to_azimuth(d + t)


def prog():
    # move_to_expected_azimuth(0)
    prev = []
    # for i in range(1)
    while True:
        o = open_port_and_get_position()
        if len(prev) > 20:
            print str(o.longitude) + "\t" + str(o.latitude - prev[-20])
        prev.append(o.latitude)


if __name__ == "__main__":
    prog()
