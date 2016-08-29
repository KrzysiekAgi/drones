import subprocess
import serial
import io
from message_coders_decoders import decode_gprmc_msg


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
