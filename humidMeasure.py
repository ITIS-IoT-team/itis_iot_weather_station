#!/usr/bin/python3
# coding=utf-8

# Needed modules will be imported
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
from lps331ap import LPS331AP as Barometer

barometer = Barometer()

sleeptime = 10
DHTSensor = Adafruit_DHT.DHT11
GPIO_Pin = 9

print('KY-015 sensortest - temperature and humidity')

try:
    while(True):
        humid, temper = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
        if humid is not None and temper is not None:
            print('temperature = {0:0.1f}°C; rel. humidity = {1:0.1f}%; pressure = {2}mmHg'.format(
                temper, humid, barometer.read_pressure()))
        else:
            print('Error while reading - please wait for the next try!')
        time.sleep(sleeptime)
except KeyboardInterrupt:
    GPIO.cleanup()
