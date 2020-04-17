# Dump for testing without raspberry
# use like this:
# import sensors_dump as sensors

HUMID_UNIT = '%'
TEMP_UNIT = '°C'
PRESSURE_UNIT = 'mmHg'


def get_sensor_values():
    return [
        ('Humidity', 0, HUMID_UNIT),
        ('Temperature', 0, TEMP_UNIT),
        ('Pressure', 0, PRESSURE_UNIT)
    ]


def get_pressure():
    return 0


def get_temp():
    return 0


def get_humid():
    return 0
