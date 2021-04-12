## @package SIRA
# An IoT solution
# 
#  @version 1 
#
# Pontificia Universidad Javeriana
# 
# Electronic Engineering
# 
# Developed by:
# - Angela Maria Logreira
#       Mail: <angelalogreira@javeriana.edu.co>
#       GitHub: AngelaLogreira
# - Pedro Alejandro Muñoz
#       Mail: <munoz_pedro@javeriana.edu.co>
#       GitHub: Peter8000
# - Pedro Eli Ruiz Zarate
#       Mail: <pedro.ruiz@javeriana.edu.co>
#       GitHub: PedroRuizCode
#  
# With support of:
# - Wilder Eduardo Castellanos
#       Mail: <wecastellanos@javeriana.edu.co>
# - Gabriel Alberto Diaz
#       Mail: <gabriel.diaz@javeriana.edu.co>

import smbus
import paho.mqtt.publish as publish
from time import sleep
import math
import sys
import os
import glob
import time
from requests import get 
import json
from time import time
from w1thermsensor import W1ThermSensor
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()
adc = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=4)
sensor = W1ThermSensor()


## adps9300 class
#
# Define the value of registers
class adps9300(object):
    bus = None
    addr = 0x39
    REG_CONTROL = 0x00
    REG_TIMING = 0x01
    REG_THRESHLOWLOW = 0x02
    REG_THRESHLOWHIGH = 0x03
    REG_THRESHHIGHLOW = 0x04
    REG_THRESHHIGHHIGH = 0x05
    REG_INTERRUPT = 0x06
    REG_CRC = 0x08
    REG_ID = 0x0A
    REG_DATA0LOW = 0x0C
    REG_DATA0HIGH = 0x0D
    REG_DATA1LOW = 0x0E
    REG_DATA1HIGH = 0x0F    
    REG_CONTROL_CMD = 1 << 7
    REG_CONTROL_IRQCLEAR = 1 << 6
    REG_CONTROL_WORD = 1 << 5
    REG_CONTROL_POWER_ON = 0x03
    REG_TIMING_GAIN_1 = 0 << 4
    REG_TIMING_GAIN_16 = 1 << 4
    REG_TIMING_START_CYCLE = 1 << 3    
    REG_TIMING_INTEGRATE_13_7MS = 0
    REG_TIMING_INTEGRATE_101MS = 1
    REG_TIMING_INTEGRATE_402MS = 2    
    REG_TIMING_SCALE_13_7MS = 0.034
    REG_TIMING_SCALE_101MS = 0.252
    REG_TIMING_SCALE_402MS = 1    
    _gain = 0
    _integration = 0

    ## The constructor
    #
    # Here you can configure the device
    # @param self The object pointer.
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.set_power(True)
        self.set_timing(True, 0)

    ## Device status
    #
    # Here you can configure the device status
    # @param self The object pointer.
    # @param on The device status
    def set_power(self, on):
        regval = 0
        if on:
            regval = self.REG_CONTROL_POWER_ON        
        self.bus.write_byte_data(self.addr, self.REG_CONTROL
                                | self.REG_CONTROL_CMD, regval)

    ## Device timing
    #
    # Here you can configure the device timing
    # @param self The object pointer.
    # @param highgain The device gain
    # @param integration Integration flag
    def set_timing(self, highgain, integration):
        print('Settings: high gain', highgain, 'integration', integration)
        regval = 0    
        if highgain:
            regval = regval | self.REG_TIMING_GAIN_16
            self._gain = 1
        else:
            regval = regval | self.REG_TIMING_GAIN_1
            self._gain = 1 / 16.0

        if integration == 0:
            regval = regval | self.REG_TIMING_INTEGRATE_13_7MS
            self._integration = self.REG_TIMING_SCALE_13_7MS
        elif integration == 1:
            regval = regval | self.REG_TIMING_INTEGRATE_101MS
            self._integration = self.REG_TIMING_SCALE_101MS
        else:
            regval = regval | self.REG_TIMING_INTEGRATE_402MS
            self._integration = self.REG_TIMING_SCALE_402MS

        self.bus.write_byte_data(self.addr, self.REG_TIMING
                                | self.REG_CONTROL_CMD, regval)

    ## Read data
    #
    # Here you can read the device output
    # @param self The object pointer.
    def read_raw(self):
        ch0 = self.bus.read_word_data(self.addr, self.REG_CONTROL_CMD
        | self.REG_CONTROL_WORD | self.REG_DATA0LOW)
        ch1 = self.bus.read_word_data(self.addr, self.REG_CONTROL_CMD
        | self.REG_CONTROL_WORD | self.REG_DATA1LOW)
        return [ch0, ch1]

    ## Convert data
    #
    # Here you can convert to humidity the device output
    # @param self The object pointer.
    def read_hum(self):
        ch0, ch1 = self.read_raw()
        return self.calc_hum(ch0, ch1)

    ## Calculate humidity
    #
    # Here you can calculate the humidity of floor
    # @param self The object pointer.
    # @param ch0 Channel 0 data
    # @param ch1 Channel 1 data
    def calc_hum(self, ch0, ch1):        
        ch0 = ch0 / self._gain / self._integration
        ch1 = ch1 / self._gain / self._integration        
        if ch0 == 0:
            return None        
        ch0 = float(ch0)
        ch1 = float(ch1)        
        lux = 0        
        d = ch1 / ch0
        if ch1 == ch0 == 65535:
            return float('nan')
        if d > 0 and d <= 0.5:
            lux = 0.0304 * ch0 - 0.062 * ch0 * math.pow(d, 1.4)
        elif d > 0.5 and d <= 0.61:
            lux = 0.0224 * ch0 - 0.031 * ch1
        elif d > 0.61 and d <= 0.80:
            lux = 0.0128 * ch0 - 0.0153 * ch1
        elif d > 0.80 and d <= 1.30:
            lux = 0.00146 * ch0 - 0.00112 * ch1
        elif d > 1.3:
            lux = 0

        return lux


## Define temperature value
#
# Here you can get data from temperature sensor
def get_temp():
    temperature = sensor.get_temperature()
    return temperature


## Get weather from server
#
# Here we get weather data from darksky servers
def get_weather():
    ip = os.popen('curl https://ipapi.co/ip/').read()
    key_ip = '773f022b886487a6103266c0a71377e9'
    url = 'http://api.ipstack.com/%s?access_key=%s&output=json' % (ip, key_ip)
    loc = get(url)
    la = loc.json()['latitude']
    lo = loc.json()['longitude']
    key_wh = '3bb84459e7c76e4c4d81cabe2e7448a0'
    _w = 'exclude=minutely,hourly,alerts,flags&units=auto'
    url = 'https://api.darksky.net/forecast/%s/%s,%s?%s' % (key_wh, la, lo, _w)
    wt = get(url)
    return wt


if __name__ == "__main__":
    h = 'mqtt.thingspeak.com'
    c_id = '1355207'
    c_k = 'UTTBYG4DXAXCI4UM'
    c_u1 = 'https://api.thingspeak.com/channels'
    c_u2 = 'feeds/last.json?api_key'
    t = "channels/" + c_id + "/publish/" + c_k
    while True:
        for i in range(5):
            print("Temperatura en ºC")
            print(get_temp())
            wt = get_weather()
            temp = (wt.json()['currently']["temperature"])
            hum = (wt.json()['currently']["humidity"])		
            humidity = adc.read_adc(1, gain=1)
            print("Humedad=", humidity)
            x = adps9300()
            print("Hum value is %s" % x.read_hum())
            m = "field1=" + str(get_temp()) + "&field2="
                        + str(humidity) + "&field3=" + str(x.read_hum())
                        + "&field4=" + str(temp) + "&field5=" + str(hum)
                        + "&field6=" + str(i)
            t1 = time()
            try:
                publish.single(t, payload=m, hostname=h, port=1883, tls=None, transport='tcp')
                while time() - t1 < 15:
                    pass
            except:
                print('Error')
            try:
                ack = get('%s/%s/%s=%s&results=2') % (c_u1, c_id, c_u2, ck)
                print(ack.json()['field6'])
            except:
                print("There was an error while reading the data.")

## @var temperature
# It takes temperature from the sensor

## @var ip
# This is the IP of the device

## @var la
# This is the latitude

## @var lo
# This is the longitude

## @var h
# This is the hostname

## @var t
# This is the topic of mqtt

## @var m
# This is the MQTT message

## @var temp
# This is the temperature loaded from the server

## @var hum
# This is the humidity loaded from the server

## @var temp
# This is the temperature loaded from the server

## @var c_id
# This is the thingspeak channel id

## @var c_k
# This is the thingspeak API key

## @var c_u1
# This is the first part of the URL

## @var c_u2
# This is the second part of the URL
