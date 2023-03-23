import telebot
from telebot import types

import settings

bot = telebot.TeleBot(settings.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Hey, let's fill out the form together!\nTo continue type: /fill_data")


@bot.message_handler(commands=['fill_data'])
def fill_data(message):
    bot.send_message(message.from_user.id, "Your name? Example: 'sonic'")
    bot.register_next_step_handler(message, fill_username)


def fill_username(message):
    username = message.text
    bot.send_message(message.from_user.id, "Your lastname? Example: 'speed'")
    bot.register_next_step_handler(message, fill_lastname, username)


def fill_lastname(message, username):
    lastname = message.text
    bot.send_message(message.from_user.id, "Your email? Example: 'example@email.com'")
    bot.register_next_step_handler(message, fill_email, username, lastname)


def fill_email(message, username, lastname):
    email = message.text
    bot.send_message(message.from_user.id, "Your phone number? Example: '+93-23-52'")
    bot.register_next_step_handler(message, fill_phone, username, lastname, email)


def fill_phone(message, username, lastname, email):
    phone = message.text
    bot.send_message(message.from_user.id, "Your birthday? Example: '24-12-1976'")
    bot.register_next_step_handler(message, fill_birthday, username, lastname, email, phone)


def fill_birthday(message, username, lastname, email, phone):
    birthday = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("Yes")
    btn2 = types.KeyboardButton('No')

    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, "Did you fill it out correctly?", reply_markup=markup)
    bot.register_next_step_handler(message, complete_test, username, lastname, email, phone, birthday)


def complete_test(message, username, lastname, email, phone, birthday):
    approval = message.text

    remove_buttons = telebot.types.ReplyKeyboardRemove()

    if approval.lower() == 'yes':
        bot.send_message(message.chat.id, "Thanks!", reply_markup=remove_buttons)
    else:
        bot.send_message(message.chat.id, "You can repeat this by typing: /fill_data!", reply_markup=remove_buttons)


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
