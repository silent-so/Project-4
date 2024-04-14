import telebot
import sqlite3

TOKEN = '7043497776:AAE3BnBDmwwvEGC3r1OxCibvURmNaRrC8Jw'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!Тут ты можешь добавлять свои товары /add')

@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, 'Введите название:')
    bot.register_next_step_handler(message,item_name)


def item_name(message):
    bot.send_message(message.chat.id,'Хорошо,теперь отправь характеристику товара')
    bot.register_next_step_handler(message, item_price)

def item_price(message):
    bot.send_message(message.chat.id, 'Введите цену товара:')
    bot.register_next_step_handler(message, item_reg)

def item_reg(message):
    bot.send_message(message.chat.id, 'Введите свой регион:')
    bot.register_next_step_handler(message, item_bio)

def item_bio(message):
    bot.send_message(message.chat.id,'Хорошо,теперь отправь фото товара')

@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(message.chat.id, 'Отлично!Добавляем ваш товар на склад...')
    bot.send_message(message.chat.id, 'Обновление...')
    bot.send_message(message.chat.id, 'Ваш товар добавлен на склад')

@bot.callback_query_handler(func=lambda call:True)
def get_callback(call):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM table WHERE category =''')
    table = cursor.fetchall()



bot.infinity_polling()
