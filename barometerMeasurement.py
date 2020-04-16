#!/usr/bin/python3
import time

from lps331ap import LPS331AP as Barometer

barometer = Barometer()

while True:
    print('Pressure: {} mmHg, Temperature: {} C'.format(
        barometer.read_pressure(), barometer.read_temperature()))
    time.sleep(3)

