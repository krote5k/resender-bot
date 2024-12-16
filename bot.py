# -*- coding: utf-8 -*-
#import config
import telebot
from telebot import types
import requests
from config import *

bot = telebot.TeleBot(token)

def sender_verify(user_id):
    '''Принимает id пользователя и возвращает id чата и его отображаемое в чате имя.'''
    #message.from_user.id
    if user_id in teachers:
        chat_id = teachers.get(user_id)[0]
        sender_name = teachers.get(user_id)[1]
        print("Проверка 1 пройдена!")
        return chat_id, sender_name
    else:
        bot.send_message(message_chat_id, f"*{message.chat.username}* я тебя не знаю ", parse_mode = 'Markdown')
        print("Проверку не прошёл")

def chat_verify(chat_id):
    '''Берет id чата и возвращает id пользователя, которому назначается сообщение.'''
    for id in list(teachers.items()):
        if list(id)[1][0] == chat_id:
            user_id = list(id)[0]
            return user_id

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую. \n\n Отправьте /help для подсказки.')

@bot.message_handler(commands=["help"])
def helps(message):
    chat_id, sender_name = sender_verify(message.from_user.id)
    bot.send_message(message.chat.id, 'Просто отправляете сообщение и оно отправится участникам школьного чата')

#Удаление сообщений
@bot.message_handler(commands=["del"])
def delete(message):
    if  message.reply_to_message is not None:
        bot.delete_message(message.chat.id, message.reply_to_message.id)
        #подтираем за собой
        bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(commands=["расписание"])
@bot.message_handler(regexp="^расписание$")
def send_rasp(message):
    print(message.chat.id)
    bot.send_photo(message.chat.id, open('raspisanie.jpg', 'rb'))

@bot.message_handler(commands=["погода"])
@bot.message_handler(regexp="^погода$")
def send_weather(message):
    response = requests.get('http://pogoda.orsk.ru/')
    temp_orsk = response.text.split('\n')[104].strip()
    bot.send_message(message.chat.id, f"Температура в Орске: {temp_orsk}", parse_mode = 'Markdown')

#Пересылка ответа по реплаю учителю
@bot.message_handler(func=lambda message: message.reply_to_message is not None)
def reply(message):
    user_id = chat_verify(message.chat.id)
#    print(message.chat.id)
#    print(user_id)
    if message.reply_to_message.from_user.username == botname:
        bot.forward_message(user_id, message.chat.id, message.message_id)
    else:
        pass

@bot.message_handler(content_types=["text"])
def send_messages(message):
    chat_id, sender_name = sender_verify(message.from_user.id)
    if int(message.chat.id) == chat_id:
#        print(message)
        try:
            chatId=message.text.split(': ')[0]
            text=message.text.split(': ')[1]
            bot.send_message(chatId, text)
        except:
            pass
    else:
        # При отправке не тем человеком - подставляется его ник
        if message.chat.id in teachers:
            sender_name = sender_name
        else:
            sender_name = str(message.chat.username)
        
        #print(message)
        bot.send_message(chat_id, f"<b>{sender_name}</b>: {message.text}", parse_mode = 'html')
        bot.send_message(message.from_user.id, f"*{message.chat.username}* идет отправка 👍", parse_mode = 'Markdown')

@bot.message_handler(content_types=["photo"])
def send_photo(message):
    chat_id, sender_name = sender_verify(message.from_user.id)
    if int(message.chat.id) == chat_id:
        try:
            chatId=message.text.split(': ')[0]
            text=message.text.split(': ')[1]
            bot.send_message(chatId, text)
        except:
            pass
    else:
        # При отправке не тем человеком - подставляется его ник
        if message.chat.id in teachers:
            sender_name = sender_name
        else:
            sender_name = str(message.chat.username)

        photo = message.photo[-1].file_id

        if message.caption is None:
            message.caption = ""

        bot.send_photo(chat_id, photo, f"<b>{sender_name}</b>: {message.caption}", parse_mode='html')
        bot.send_message(message.chat.id, f"*{message.chat.username}*, фото отправлено.", parse_mode = 'Markdown')


@bot.message_handler(content_types=["document"])
def send_doc(message):
    chat_id, sender_name = sender_verify(message.from_user.id)
    if int(message.chat.id) == chat_id:
        try:
            chatId=message.text.split(': ')[0]
            text=message.text.split(': ')[1]
            bot.send_message(chatId, text)
        except:
            pass
    else:
        # При отправке не тем человеком - подставляется его ник
        if message.chat.id in teachers:
            sender_name = sender_name
        else:
            sender_name = str(message.chat.username)
 
        bot.forward_message(chat_id, message.chat.id, message.message_id) 
        bot.send_message(message.chat.id, "Переслал документ.")



if __name__ == '__main__':
    bot.polling(none_stop = True)
