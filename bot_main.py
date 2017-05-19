#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 19.05.2017 13:30:38 MSK

import telebot  # импортируем модуль pyTelegramBotAPI
from telebot import types

import request_proc
import page_return
import conf     # импортируем наш секретный токен

bot = telebot.TeleBot(conf.TOKEN)  # создаем экземпляр бота

def limitation(text):
    piecies = text.split('\n')
    l = 0
    msg_txt = ''
    for p in piecies:
        if l > 3000:
            break
        msg_txt += '\n' + p
        l += len(p)
    piecies = msg_txt.split('\n')
    if piecies[-1].startswith('В томе '):
        piecies = piecies[:-1]
        msg_txt = '\n'.join(piecies)
    return msg_txt

        

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Этот бот умеет искать имена в указателе к 90-томнику Л. Н. Толстого.\nПришлите боту текст для поиска среди имён собственых.\nБот надстроен над приложением «91-й том», которое открывается по адресу http://index.tolstoy.ru")

@bot.message_handler(regexp=">>.+?<<")
def handle_message(message):
    name_index = message.text.strip(' ><')
    pairs = request_proc.search_term(name_index)
    #try:
    mentions = page_return.person_get_mentions(pairs[name_index + ' '])
    msg_collected = []
    for vol in mentions:
        vol_item = 'В томе {0} ({1}):\n'.format(vol['volume']['number'], vol['volume']['name'])
        links = []
        for men in vol['mentions']:
            if not men['comment']:
                links.append('* {0}#{1}'.format(vol['volume']['link'], men['start']))
        if links:
            links = '\n'.join(links)
        else:
            links = 'Только в комментариях'
        vol_item = vol_item + links
        msg_collected.append(vol_item)
    msg_text = '\n'.join(msg_collected)
    if len(msg_text) > 3000:
        msg_text = limitation(msg_text)
    bot.send_message(message.chat.id, msg_text)
            
    #except KeyError:
        #bot.send_message(message.chat.id, 'Такого имени в указателе, увы, нет.')
    

@bot.message_handler(content_types=['text'])  # этот обработчик ищет имя в указателе
def send_len(message):
    pairs = request_proc.search_term(message.text)
    if not pairs:
        bot.send_message(message.chat.id, 'К сожалению, так ничего не найти. Пришлите какое-нибудь слово.')
    else:
        keyboard = types.ReplyKeyboardMarkup()
        buttons = []
        for pair in pairs:
            keyboard.row('>> ' + pair + ' <<')
        bot.send_message(message.chat.id, "Выберите имя:", reply_markup=keyboard)
    
if __name__ == '__main__':
    bot.polling(none_stop=True)

