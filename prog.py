import serial
import io
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

# 
# sio.write(unicode("$O10S\n"))
# sio.write(unicode("$O11E\n"))


sio.write(unicode("$O10D-14300\n"))
# sio.write(unicode("$O11R\n"))
sio.flush() # it is buffering. required to get the data out *now*
hello = sio.readline()
print(hello)
ser.close()