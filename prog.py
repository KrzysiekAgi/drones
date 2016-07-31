import serial
import io
import subprocess
from message_coders_decoders import move_up_down_msg, gprmc_position_request
from message_coders_decoders import decode_gprmc_msg
import time
import numpy
import geography


def find_device_name_of_serial():
    output = subprocess.Popen(["bash", "find_ftdi.sh"], stdout=subprocess.PIPE).communicate()[0]
    # print output
    # improve checking
    if len(output) < 8:
        raise Exception("no serial device is attached")

    return output.strip()


def get_serial_object_for_rotor():
    device_name = find_device_name_of_serial()
    ser = serial.Serial(device_name, 9600, timeout=1)
    return ser


def send_and_receive_gprmc(sio):
    sio.write(unicode("$GPRMC\n"))
    sio.flush()
    h = sio.readline()
    return h.strip()


def move_horizontaly(sio, steps):
    sio.write(unicode(move_up_down_msg("10", steps)))
    sio.flush()


def degrees_to_steps_for_horizontal(degrees):
    return 14300.0 * (degrees / 360.0)

def get_position(sio):
    # history = []
    # for i in range(0,10):
        # time.sleep(1)
    position_msg = send_and_receive_gprmc(sio)
    decoded = decode_gprmc_msg(position_msg)
        # history.append(decoded.azimuth)
        # print decoded.azimuth

    # decoded.azimuth = numpy.mean(history)
    return decoded


def prog():
    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    antenna_position = get_position(sio)
    print antenna_position.longitude
    a = geography.azimuth(antenna_position.latitude,
                      antenna_position.longitude,
                      1,
                      1)
    print a
    ser.close()


if __name__ == "__main__":
    prog()