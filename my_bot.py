from parsing import *
import telebot
from telebot.types import *
from mytoken import *


bot = telebot.TeleBot(TOKEN)


button_start = KeyboardButton('/start')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_start.add(button_start)

button_description = KeyboardButton('Description')
button_photo = KeyboardButton('Photo')
button_exit = KeyboardButton('❌ Quit')
show = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
show.add(button_description, button_photo)
show.row(button_exit)


@bot.message_handler(commands = ['start'])
def show_news(message):
    articles = get_data2()
    news = get_titles(articles)
    s = ''
    for i in range(20):
        s += f'{i+1}) {news[i]}\n'
    bot.send_message(message.chat.id, s)
    msg = bot.send_message(message.chat.id, 'Выберите новость (от 1 до 20):', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, printmsg, news, articles)


def start_check(msg):
    if msg.text == '/start':
        show_news(msg)
    else:
        start_func(msg)


def start_func(msg):
    bot.send_message(msg.chat.id, '👋', reply_markup=kb_start)
    bot.register_next_step_handler(msg, start_check)

def check(msg, article):
    if msg.text == 'Description':
        description = get_description(article)
        bot.send_message(msg.chat.id, description, reply_markup=show)
        bot.register_next_step_handler(msg, check, article)

    elif msg.text == 'Photo':
        try:
            photo = article.find('img').get('src')
            bot.send_photo(msg.chat.id, photo, reply_markup=show)
        except AttributeError:
            bot.send_message(msg.chat.id, 'Нет фото', reply_markup=show)
        bot.register_next_step_handler(msg, check, article)

    elif msg.text == '❌ Quit':
        bot.send_message(msg.chat.id, 'До свидания!', reply_markup=ReplyKeyboardRemove())
        start_func(msg)

    else:
        bot.send_message(msg.chat.id, 'Нажмите Description или Photo:', reply_markup=show)
        bot.register_next_step_handler(msg, check, article)

def printmsg(msg, news, articles):
    if not msg.text.isdigit():
        msg2 = bot.send_message(msg.chat.id, 'Вы ввели не число')
        bot.register_next_step_handler(msg2, printmsg, news, articles)
    elif int(msg.text) < 1 or int(msg.text) > 20:
        msg2 = bot.send_message(msg.chat.id, 'Введите число от 1 до 20')
        bot.register_next_step_handler(msg2, printmsg, news, articles)
    else:
        bot.send_message(msg.chat.id, news[int(msg.text) - 1])
        msg2 = bot.send_message(msg.chat.id, 'Вы можете увидеть описание данной новости (Description) и фотку (Photo)', reply_markup=show)
        bot.register_next_step_handler(msg2, check, articles[int(msg.text)-1])



bot.polling()