# This is script that run when device boot up or wake from sleep.

from machine import Pin, I2C
import network
import ubinascii
import time
import esp
import dht
import gc

import bme280

# Get rid of debug and free some memory
esp.osdebug(None)
gc.collect()

# How many times to wait until WiFi connection
CONNECT_RETRY_COUNT = 30


def get_wifi_creds(creds_file='wifi-credentials.txt'):
    """
    file should be in format: SSID\nPassword

    :param creds_file:
    :return: list
    """

    try:
        return [line.strip() for line in open(creds_file, 'r').readlines()]
    except IOError as err:
        print("Error loading WiFi credentials: ", err)

    return None


def connect_to_wifi():
    """
    Connects to WiFi and waits until connection

    :return: connection status
    """

    creds = get_wifi_creds()
    print("Using {} password to connect to {}".format(
        creds[1],
        creds[0]
    ))

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(creds[0], creds[1])

    counter = 0
    while not station.isconnected():
        print('.', end='')
        time.sleep(0.3)
        counter += 1
        if counter > CONNECT_RETRY_COUNT:
            print("\nTimed out connection to {} WiFi network".format(creds[0]))
            return False

    print('\nConnected to {} WiFi network.\nIP params: {}\nMac: {}'.format(
        creds[0],
        station.ifconfig(),
        ubinascii.hexlify(station.config('mac'), ':').decode()
    ))
    return True


# Connect to WiFi
connect_to_wifi()

# Init globals to main.py
ht = dht.DHT22(Pin(0, Pin.IN, Pin.PULL_UP))
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)
bme = bme280.BME280(i2c=i2c)
