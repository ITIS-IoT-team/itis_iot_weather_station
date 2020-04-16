import telepot
import sensors
from telepot.loop import MessageLoop
from time import sleep

def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message

    print ('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/get':
        bot.sendMessage (chat_id, sensors.get_sensor_values())

telepot.api.set_proxy('http://51.38.127.211:8080')
bot = telepot.Bot('1233829922:AAF5_3cWBQwNJQhHxkuKD4Us4-EF9ZDU0Vc')
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(10)


