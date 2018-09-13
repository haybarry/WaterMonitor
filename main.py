from machine import Pin, I2C
import time

import network

from umqtt.robust import MQTTClient

#from machine import Timer

import ubinascii

from hcsr04 import HCSR04

from sh1106 import SH1106_SPI, SH1106_I2C
from writer import Writer
import myfont15


i2c = I2C(scl=Pin(5), sda=Pin(4), freq=40000)

#configure display
WIDTH = const(128)
Lastline = 0
NewScreen = False
HEIGHT = 64
shdisp = SH1106_I2C(WIDTH, HEIGHT, i2c, None)
DispTopic = ["","","","",""]
DispMsg = ["","","","",""]
wri2 = Writer(shdisp, myfont15, verbose=False)   #  freesans20
Writer.set_clip(True, True)
wri2.set_textpos(0,0)
wri2.printstring("Distance")
shdisp.show()

#configue Ultrasonic Distance Sensor
sensor = HCSR04(trigger_pin=13, echo_pin=12)

#configure wifi
wlan = network.WLAN(network.STA_IF)
#configure MQTT
mac = wlan.config('mac')  # get full mac address
macascii = ubinascii.hexlify(mac)  # turn mac into ascii
node = b'Yellow' + macascii[6:]  # node for MQTT
server = "192.168.1.180"
c = MQTTClient(node, server)
channel = [b'Aqua/Tank']


sec30 = 30000
refdistance=700

def do_connect():
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('canucks_fans_live_here', 'Impre5si0ni5t')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


    print(node)
    print(server)


    try:
        c.connect()
        print('MQTT Connected')
    except Exception as e:
        print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        sys.exit()





def main():
    do_connect()
    # ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME1
    # mqtt_feedname1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME1), 'utf-8')
    # mqtt_feedname2 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME2), 'utf-8')
    reftime = time.ticks_ms()
    while True:
        wri2.set_textpos(12, 0)
        distance = sensor.distance_mm()
        wri2.printstring(str(distance) + '        ')
        print("Distance", distance)
        shdisp.show()
        time.sleep(1)
        now = time.ticks_ms()
        if (now - reftime) > sec30:
            reftime = reftime + sec30
            a = c.publish(channel[0], str(distance), qos=1)
            print("Message Sent")


if __name__ == '__main__':
    main()
