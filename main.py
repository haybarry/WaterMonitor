from machine import Pin, I2C
import time

import network

from umqtt.robust import MQTTClient

#from machine import Timer

import ubinascii

from hcsr04 import HCSR04

from sh1106 import SH1106_SPI, SH1106_I2C
from writer import Writer
import myfont12


i2c = I2C(scl=Pin(5), sda=Pin(4), freq=40000)

#configure display
WIDTH = const(128)
Lastline = 0
NewScreen = False
HEIGHT = 64
shdisp = SH1106_I2C(WIDTH, HEIGHT, i2c, None)
DispTopic = ["","","","",""]
DispMsg = ["","","","",""]
wri2 = Writer(shdisp, myfont12, verbose=False)   #  freesans20
Writer.set_clip(True, True)
wri2.set_textpos(0,0)
wri2.printstring("Distance")
shdisp.show()

#configue Ultrasonic Distance Sensor
sensor = HCSR04(trigger_pin=13, echo_pin=12)

#configure MQTT
channel = [b'Aqua/Tank']


def sub_wifi():
    global np
    print('connecting to network...')

    sta_if.active(True)
    sta_if.connect('canucks_fans_live_here', 'Impre5si0ni5t')
    while not sta_if.isconnected():
        pass

    print('network config:', sta_if.ifconfig())


def sub_MQTT():
    c.connect()


#    np.write()

#    c.subscribe(T_TOPIC)

#    c.subscribe(H_TOPIC)

sta_if = network.WLAN(network.STA_IF)

mac = sta_if.config('mac') # get full mac address

macascii = ubinascii.hexlify(mac)  # turn mac into ascii

node = macascii[6:]  # node for MQTT

server = "192.168.1.180"

print(node)
print(server)

c = MQTTClient(node, server)

sub_wifi()
sub_MQTT()

reftime = time.ticks_ms()
sec30 = 30000
refdistance=700

while True:
    wri2.set_textpos(12, 0)
    distance = sensor.distance_mm()
    wri2.printstring(str(distance) + '        ')
    print("Distance", distance)
    shdisp.show()
    time.sleep(1)
    print("hello")
    now = time.ticks_ms()
    if (now - reftime) > sec30:
        reftime = reftime + sec30
        a = c.publish(channel[0], str(refdistance), qos=1)