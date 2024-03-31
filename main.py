import telebot.types
from telebot import TeleBot
import sqlite3

token = '6703507248:AAE3ErlqgjUQBayVjBzcz4Xy67XfpCHgtfc'
bot = TeleBot(token)



login = ''
password = ''
id = ''
role = ''

in_system = False


messages = []


class User:
    def init(self, id='', login='', password='', role=''):
        self.id = id
        self.login = login
        self.password = password
        self.role = role



registered_user = User()




product_id=''
name=''
descr=''
price=''
category=''
class Product:
    def init(self, product_id='', name='', descr='', price='', category=''):
        self.product_id = product_id
        self.name = name
        self.descr = descr
        self.price = price
        self.category = category















@bot.message_handler(commands=['start'])
def start(message):
    messages.append(message.message_id)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False)
    btn_1 = telebot.types.KeyboardButton('/register')
    btn_2 = telebot.types.KeyboardButton('/buy')
    btn_3 = telebot.types.KeyboardButton('/sale')
    btn_4 = telebot.types.KeyboardButton('/login')
    btn_5 = telebot.types.KeyboardButton('/logout')
    btn_6 = telebot.types.KeyboardButton('/info')
    markup.row(btn_1)
    markup.row(btn_2, btn_3)
    markup.row(btn_4, btn_5)
    markup.row(btn_6)
    bot_message = bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    messages.append(bot_message.message_id)

@bot.message_handler(commands=['register'])
def register(message):
    messages.append(message.message_id)
    for i in messages:
        bot.delete_message(message.chat.id, i)
    messages.clear()

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY,'
                   'category VARCHAR(30), name VARCHAR(30))')
    connection.commit()
    cursor.close()
    connection.close()
    bot_message = bot.send_message(message.chat.id, 'Начало регистрации. Введи логин: ')
    messages.append(bot_message.message_id)
    bot.register_next_step_handler(message, create_login)



def create_login(message):
    messages.append(message.message_id)
    global login
    login = message.text
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    for user in users:
        if login == user[1]:
            bot_message = bot.send_message(message.chat.id, f'Такой логин уже есть, введите новый логин:')
            messages.append(bot_message.message_id)
            bot.register_next_step_handler(message, create_login)
            break
    else:
        bot_message = bot.send_message(message.chat.id, 'Отлично. Теперь введи пароль: ')
        messages.append(bot_message.message_id)
        bot.register_next_step_handler(message, create_password)
    cursor.close()
    connection.close()

def create_password(message):
    messages.append(message.message_id)
    global password
    password = message.text
    bot_message = bot.send_message(message.chat.id, 'Регистрация завершена.')
    messages.append(bot_message.message_id)
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO users (login, password) VALUES ( "{login}", "{password}" )')
    connection.commit()
    cursor.close()
    connection.close()


@bot.message_handler(commands=['buy'])
def buy(message):
    # Ваш код для выполнения операции покупки
    bot.send_message(message.chat.id, 'Покупка выполнена успешно!')



@bot.message_handler(commands=['login'])
def login(message):
    bot.send_message(message.chat.id, 'Введите логин: ')
    bot.register_next_step_handler(message, get_login)


def get_login(message):
    global login
    global password
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    for user in users:
        if message.text == user[1]:
            bot.send_message(message.chat.id, 'Введите пароль: ')
            login = user[1]
            password = user[2]
            bot.register_next_step_handler(message, get_password)
            break
    else:
        bot.send_message(message.chat.id, 'Такого логина нет')

def get_password(message):
    global in_system
    global login
    global password
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    for user in users:
        if login == user[1] and message.text == user[2]:
            bot.send_message(message.chat.id, 'Вы вошли в систему')
            in_system = True
            print(user[0], user[1], user[2])
            registered_user.id = user[0]
            registered_user.login = user[1]
            registered_user.password = user[2]
            break
    else:
        bot.send_message(message.chat.id, 'Неверный пароль')

@bot.message_handler(commands=['logout'])
def logout(message):
    global in_system
    if in_system:
        in_system = False
        bot.send_message(message.chat.id, f'Вы вышли из системы')
    else:
        bot.send_message(message.chat.id, f'Вы не в системе')

@bot.message_handler(commands=['info'])
def logout(message):
    global in_system
    if in_system:
        bot.send_message(message.chat.id, f'Айди: {registered_user.id}\n'
                                          f'Логин: {registered_user.login}\n'
                                          f'Пароль: {registered_user.password}')
    else:
        bot.send_message(message.chat.id, f'Вы не в системе. Пожалуйста войдите в систему')

    bot.delete_message()



bot.infinity_polling()