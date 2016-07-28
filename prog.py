import serial
import io
import subprocess
from message_coders_decoders import move_up_down_msg

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

def prog():

    ser = get_serial_object_for_rotor()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    # # sio.write(unicode("$O10S\n"))
    # # sio.write(unicode("$O11E\n"))


    sio.write(unicode(move_up_down_msg("10" , 5000)))
    # sio.write(unicode("$O11R\n"))
    sio.flush() # it is buffering. required to get the data out *now*
    hello = sio.readline()
    print(hello)
    ser.close()

if __name__ == "__main__":
    prog()