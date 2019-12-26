# This is script that run when device boot up or wake from sleep.

try:
  import usocket as socket
except:
  import socket

from machine import Pin, I2C
import network
import ubinascii
import time
import dht
import bme280

import esp
esp.osdebug(None)

import gc
gc.collect()

CONNECT_RETRY_COUNT = 30

ssid = 'Nest-Ext'
password = 'divergence'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

counter = 0
while station.isconnected() == False:
  print('.', end='')
  time.sleep(0.5)
  counter += 1
  if counter > CONNECT_RETRY_COUNT:
    break

print('Connection successful\nIP params:')
print(station.ifconfig())
print('MAC addr:')
print(ubinascii.hexlify(station.config('mac'),':').decode())

ht = dht.DHT22(Pin(0, Pin.IN, Pin.PULL_UP))
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)
bme = bme280.BME280(i2c=i2c)
led = Pin(2, Pin.OUT)

