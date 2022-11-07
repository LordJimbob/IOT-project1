from machine import UART
from micropyGPS import MicropyGPS

def gps_main():
    uart = UART(2, baudrate=9600, bits=8, parity=None,
                stop=1, timeout=5000, rxbuf=1024)
    gps = MicropyGPS()
    while True:
        buf = uart.readline()
        for char in buf:
# Note the conversion to to chr, UART outputs ints normally
            gps.update(chr(char))
            
        print('UTC Timestamp:', gps.timestamp)
        print('Date:', gps.date_string('long'))
        print('Satellites:', gps.satellites_in_use)
        print('Altitude:', gps.altitude)
        print('Latitude:', gps.latitude_string())
        print('Longitude:', gps.longitude_string())
        print('Horizontal Dilution of Precision:', gps.hdop)     
gps_main()




