#!/usr/bin/python3

import threading
from datetime import datetime, timedelta
from time import sleep

import telepot
from telepot.loop import MessageLoop

import sensors

PROXY_ADDRESS = '62.171.161.146'
PROXY_PORT = 8080

running_events = dict()


def value_with_measure_unit(value, unit):
    return '_{}{}_'.format(value, unit)


def get_sensors_pretty_string():
    sensor_values = sensors.get_sensor_values()
    return '\n'.join(map(lambda item: '*{}*: {}'.format(item[0], value_with_measure_unit(item[1], item[2])), sensor_values))


def handle_plan(chat_id):
    print("Sending subscription to {}...".format(chat_id))
    bot.sendMessage(chat_id, get_sensors_pretty_string(), parse_mode='Markdown')
    event = threading.Timer(timedelta(seconds=10).total_seconds(), handle_plan, args=(chat_id,))
    running_events[chat_id] = event
    event.start()


def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message

    print('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/get':
        bot.sendMessage(chat_id, get_sensors_pretty_string(), parse_mode='Markdown')
    elif command == '/getTemp':
        bot.sendMessage(chat_id, value_with_measure_unit(sensors.get_temp(), sensors.TEMP_UNIT), parse_mode='Markdown')
    elif command == '/getHumid':
        bot.sendMessage(chat_id, value_with_measure_unit(sensors.get_humid(), sensors.HUMID_UNIT), parse_mode='Markdown')
    elif command == '/getPress':
        bot.sendMessage(chat_id, value_with_measure_unit(sensors.get_pressure(), sensors.PRESSURE_UNIT), parse_mode='Markdown')
    elif command.split()[0] == '/subscribe':
        if chat_id not in running_events:
            param = command.split(' ')[1]
            planned_time = datetime.strptime(param, "%H:%M")
            planned_date = datetime.now().replace(hour=planned_time.hour, minute=planned_time.minute, second=0) + timedelta(seconds=1)
            diff = planned_date - datetime.now()
            diff_sec = diff.total_seconds()
            event = threading.Timer(diff_sec, handle_plan, args=(chat_id,))
            running_events[chat_id] = event
            event.start()
            bot.sendMessage(chat_id, 'Подписка на {} добавлена. Введите /unsubscribe для её отмены.'.format(param))
        else:
            bot.sendMessage(chat_id, 'У вас уже есть активная подписка. Введите /unsubscribe для её отмены.')
    elif command == '/unsubscribe':
        if chat_id in running_events:
            running_events[chat_id].cancel()
            del running_events[chat_id]
            bot.sendMessage(chat_id, 'Активная подписка удалена. Добавьте новую с помощью /subscribe HH:MM.')
        else:
            bot.sendMessage(chat_id, 'У вас нет активной подписки. Добавьте с помощью /subscribe HH:MM.')
    else:
        bot.sendMessage(chat_id, 'Я тебя не понимать..(')


if __name__ == '__main__':
    telepot.api.set_proxy('http://{}:{}'.format(PROXY_ADDRESS, PROXY_PORT))
    bot = telepot.Bot('1233829922:AAF5_3cWBQwNJQhHxkuKD4Us4-EF9ZDU0Vc')
    print(bot.getMe())

    # Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
    MessageLoop(bot, handle).run_as_thread()
    print('Listening....')

    while 1:
        sleep(10)
