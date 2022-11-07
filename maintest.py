import umqtt_robust2 as mqtt
from machine import Pin, ADC
from time import sleep
from machine import PWM
import tm1637
import gps_funktion
from machine import I2C
import mpu6050
import sys
import neopixel
from neotimer import *

mytimer = Neotimer(30000)
mytimer2 = Neotimer(20000)
analog_pin = ADC(Pin(34))
analog_pin.atten(ADC.ATTN_11DB)
analog_pin.width(ADC.WIDTH_12BIT)
n = 12
p = 23
np= neopixel.NeoPixel(Pin(p, Pin.OUT), n)
i2c = I2C(scl=Pin(21), sda=Pin(22))
mpu = mpu6050.accel(i2c)
likes = 1
n = 0
tm1 = tm1637.TM1637(clk=Pin(2), dio=Pin(4))
tm2 = tm1637.TM1637(clk=Pin(15), dio=Pin(5))
tm1.number(0)
tm2.number(0)
test = False
while True:
    try:
        # Jeres kode skal starte her
        gps_data = gps_funktion.gps_to_adafruit
        
        if mytimer.repeat_execution():
            mqtt.web_print(gps_data, 'jimm1480/feeds/mapfeed/csv')
            print(f"\ngps_data er: {gps_data}")
        
        if mqtt.besked2 == "a":
            tm2.number(likes)
            likes = likes + 1
            mqtt.besked2 = ""
        acy = mpu.get_values()
        print(acy)
        stor = acy["AcX"]
        if stor > -9500 and test == False:
            n = n + 1
            test = True
            tm1.number(n)
        elif stor < -9000 and test == True:
            test = False
        analog_val = analog_pin.read()
        print ("RAW analog value: ", analog_val)
        volts = (analog_val * 0.000901)*5
        print("The voltage is:", volts, "v")
        battery_percentage = volts*50-320
        print("The battery persentage is:", battery_percentage, "%")
        if battery_percentage < 100 and battery_percentage > 86:
            for j in range(0,12):
                np[j] = (0, 0, 0)
            for j in range(0,12):
                np[j] = (0, 5, 0)
        elif battery_percentage < 85 and battery_percentage > 61:
            for j in range(0,12):
                np[j] = (0, 0, 0)
            for j in range(0,10):
                np[j] = (0, 5, 0)
        elif battery_percentage < 60 and battery_percentage > 46:
            for j in range(0,12):
                np[j] = (0, 0, 0)
            for j in range(0,8):
                np[j] = (10, 5, 0)
        elif battery_percentage < 45 and battery_percentage > 31:
            for j in range(0,12):
                np[j] = (0, 0, 0)
            for j in range(0,6):
                np[j] = (10, 5, 0)
        elif battery_percentage < 30 and battery_percentage > 16:
            for j in range(0,12):
                np[j] = (0, 0, 0)
            for j in range(0,4):
                np[j] = (16, 5, 0)
        elif battery_percentage < 15 and battery_percentage > 1:
            for j in range(0,12):
                np[j] = (0, 0, 0)
            for j in range(0,2):
                np[j] = (5, 0, 0)
        elif battery_percentage == 0:
            for j in range(0,12):
                np[j] = (0, 0, 0)
        if mytimer2.repeat_execution():
            mqtt.web_print(battery_percentage)
        np.write()
        # procenten svinger meget, så derfor 30 sekunder på opdatering til SEGDISP.
        # Jeres kode skal slutte her
        sleep(0.5)
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""            
        mqtt.syncWithAdafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        print(".", end = '') # printer et punktum til shell, uden et enter        
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()