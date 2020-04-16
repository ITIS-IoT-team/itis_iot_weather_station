import RPi.GPIO as GPIO
import Adafruit_DHT
import time
from lps331ap import LPS331AP as Barometer

barometer = Barometer()

sleeptime = 10
DHTSensor = Adafruit_DHT.DHT11
GPIO_Pin = 9

print('KY-015 sensortest - temperature and humidity')

def get_sensor_values():
    try:
        humid, temper = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
        if humid is not None and temper is not None:
            value = 'temperature = {0:0.1f}°C; rel. humidity = {1:0.1f}%; pressure = {2}mmHg'.format(
                temper, humid, barometer.read_pressure())
#            print(value)
            return value
        else:
            print('Error while reading - please wait for the next try!')
            return ''
    except KeyboardInterrupt:
        GPIO.cleanup()
        return ''
