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
    temp_humid = get_from_humid_sensor_or_error()
    if temp_humid:
        return temp_humid[0], temp_humid[1], get_pressure()

    
def get_pressure():
    return barometer.read_pressure()


def get_from_humid_sensor_or_error():
    try:
        humid, temper = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
        if humid is not None and temper is not None:
            return humid, temper
        else:
            print('Error while reading - please wait for the next try!')
            return None
    except KeyboardInterrupt:
        GPIO.cleanup()
        return None


def get_temp():
    data = get_from_humid_sensor_or_error()
    if data:
        return data[1]


def get_humid():
    data = get_from_humid_sensor_or_error()
    if data:
        return data[0]
