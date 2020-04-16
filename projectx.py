#!/usr/bin/python3

import sched
import time
from datetime import datetime, timedelta
from time import sleep

import sensors
import telepot
from telepot.loop import MessageLoop

s = sched.scheduler(time.time, time.sleep)


def handlePlan(bot):
    print("Doing stuff...")
    # sent msg to bot 
    bot.sendMessage('\n'.join(map(str, sensors.get_sensor_values())))
    s.enter(timedelta(seconds=10).total_seconds(), 1, handlePlan, (bot,))


def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message

    print ('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/get':
        bot.sendMessage (chat_id, '\n'.join(map(str, sensors.get_sensor_values())))
    elif command.split()[0] == '/subscribe':
        param = command.split(' ')[1]
        planned_time = datetime.strptime(param, "%H:%M")
        planned_date = datetime.now().replace(hour=planned_time.hour, minute=planned_time.minute) + timedelta(seconds=1)
        diff = planned_date - datetime.now()
        diff_sec = diff.total_seconds()
        s.enter(diff_sec, 1, handlePlan, (bot,))
    else:
        bot.sendMessage('Я тебя не понимать..(')


if __name__ == '__main__':
    telepot.api.set_proxy('http://193.37.56.10:3128')
    bot = telepot.Bot('1233829922:AAF5_3cWBQwNJQhHxkuKD4Us4-EF9ZDU0Vc')
    print (bot.getMe())

    # Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
    MessageLoop(bot, handle).run_as_thread()
    print ('Listening....')

    while 1:
        sleep(10)

