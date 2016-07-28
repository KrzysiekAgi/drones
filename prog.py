import serial
import io
import subprocess
import 

output = subprocess.Popen(["bash", "find_ftdi.sh"], stdout=subprocess.PIPE).communicate()[0]
# print output
# improve checking
if len(output) < 8:
    raise Exception("no serial device is attached")
ser = serial.Serial(output.strip(), 9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

# # 
# # sio.write(unicode("$O10S\n"))
# # sio.write(unicode("$O11E\n"))


sio.write(unicode("$O10D-1430\n"))
# sio.write(unicode("$O11R\n"))
sio.flush() # it is buffering. required to get the data out *now*
hello = sio.readline()
print(hello)
ser.close()