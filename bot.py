# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую. \n\n Отправьте /help для подсказки.')

@bot.message_handler(commands=["help"])
def helps(message):
    bot.send_message(message.chat.id, 'Просто отправляете сообщение и оно отправится участникам школьного чата')

@bot.message_handler(commands=["расписание"])
@bot.message_handler(regexp="^расписание$")
def send_rasp(message):
    bot.send_photo(config.chat, open('raspisanie.jpg', 'rb'))


"""
@bot.message_handler(commands=['w', 'п'])
@bot.message_handler(regexp="^.п$")
def send_weather(message):
    # get temperature ORSK
    r = requests.get(own_link)
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
        value = doc['current']['temperature']['@value']
        print('ORSK T:' + value)
        bot.send_message(message.chat.id, 'ORSK T: ' + value)
    else:
        bot.send_message(message.chat.id, u"cannot get content of ( URL: {own_link})... ERROR:" + str(r.status))
"""

@bot.message_handler(content_types=["text"])
def messages(message):
    if int(message.chat.id) == int(config.chat):
        try:
            chatId=message.text.split(': ')[0]
            text=message.text.split(': ')[1]
            bot.send_message(chatId, text)
        except:
            pass
    else:
        # При отправке не тем человеком - подставляется его ник
        if message.chat.id == int(config.sender_id):
            sender_name = config.sender_name
        else:
            sender_name = str(message.chat.username)

        bot.send_message(config.chat, f"*{sender_name}*: {message.text}", parse_mode = 'Markdown')
        bot.send_message(message.chat.id, f"*{message.chat.username}* идет отправка 👍", parse_mode = 'Markdown')

@bot.message_handler(content_types=["photo"])
def get_photo(message):

    if message.chat.id == int(config.sender_id):
        sender_name = config.sender_name
    else:
        sender_name = str(message.chat.username)

    photo = message.photo[-1].file_id
    bot.send_photo(config.chat, photo, f"*{sender_name}*: {message.caption}", parse_mode='Markdown')
    bot.send_message(message.chat.id, f"*{message.chat.username}*, фото отправлено.", parse_mode = 'Markdown')


@bot.message_handler(content_types=["document"])
def command_doc(message):
#        bot.send_message(config.chat, sender_name + ': ' + message.text)
    bot.send_message(message.chat.id, "Отправка документов пока не реализована.")

if __name__ == '__main__':
    bot.polling(none_stop = True)
