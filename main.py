import telebot.types
from telebot import TeleBot
import sqlite3

token = '6703507248:AAGBUOUbkVNIEhz35zuCCvVw7T34XS8Pn3M'
bot = TeleBot(token)





in_system = False


messages = []


class User:
    def __init__(self, id='', login='', password='', role=''):
        self.id = id
        self.login = login
        self.password = password
        self.role = role



registered_user = User()





class Product:
    def __init__(self, id='', name='', descr='', price='', category='', user_id=''):
        self.id = id
        self.name = name
        self.descr = descr
        self.price = price
        self.category = category
        self.user_id = user_id





product = Product()




def create_products_table():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY,'
                   'category VARCHAR(30), name VARCHAR(30), descr VARCHAR(100), price INTEGER, user_id INTEGER , FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)')
    connection.commit()
    cursor.close()
    connection.close()
create_products_table()


def create_users_table():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,'
                   'login VARCHAR(30), password VARCHAR(30))')
    connection.commit()
    cursor.close()
    connection.close()
create_users_table()


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

@bot.message_handler(commands=['sale'])
def sale(message):
    if in_system:
        messages.append(message.message_id)
        for i in messages:
            bot.delete_message(message.chat.id, i)
        messages.clear()
        bot_message = bot.send_message(message.chat.id, 'Создание товара. Выберите категорию ')
        messages.append(bot_message.message_id)
        bot.register_next_step_handler(message, create_category)
    else:
        bot.send_message(message.chat.id, 'Войдите в систему ')



def create_category(message):
    messages.append(message.message_id)
    global category
    category = message.text
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()


    if category == 'еда':
        bot_message = bot.send_message(message.chat.id, 'Отлично. Теперь введи название: ')
        messages.append(bot_message.message_id)
        bot.register_next_step_handler(message, create_name)

    elif category == 'одежда':
        bot_message = bot.send_message(message.chat.id, 'Отлично. Теперь введи название: ')
        messages.append(bot_message.message_id)
        bot.register_next_step_handler(message, create_name)

    elif category == 'техника':
        bot_message = bot.send_message(message.chat.id, 'Отлично. Теперь введи название: ')
        messages.append(bot_message.message_id)
        bot.register_next_step_handler(message, create_name)

    elif category == 'информация':
        bot_message = bot.send_message(message.chat.id, 'Отлично. Теперь введи название: ')
        messages.append(bot_message.message_id)
        bot.register_next_step_handler(message, create_name)

    else:
        bot_message = bot.send_message(message.chat.id, f'Такой категории нет, выберете одну из предложенных:')
        messages.append(bot_message.message_id)
        bot.register_next_step_handler(message, create_category)
    cursor.close()
    connection.close()

def create_name(message):
    messages.append(message.message_id)
    global name
    name = message.text
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    for product in products:
        if name == product[1]:
            bot_message = bot.send_message(message.chat.id, f'Такое название уже есть, введите другое название:')
            messages.append(bot_message.message_id)
            bot.register_next_step_handler(message, create_name)
            break
    else:
        bot_message = bot.send_message(message.chat.id, 'Отлично. Теперь введи описание: ')
        messages.append(bot_message.message_id)
        bot.register_next_step_handler(message, create_descr)
    cursor.close()
    connection.close()

def create_descr(message):
    messages.append(message.message_id)
    global descr
    descr = message.text
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    for product in products:
        if descr == product[1]:
            bot_message = bot.send_message(message.chat.id, f'Такое название уже есть, введите другое название:')
            messages.append(bot_message.message_id)
            bot.register_next_step_handler(message, create_descr)
            break
    else:
        bot_message = bot.send_message(message.chat.id, 'Отлично. Теперь введи цену: ')
        messages.append(bot_message.message_id)
        bot.register_next_step_handler(message, create_price)
    cursor.close()
    connection.close()

def create_price(message):
    messages.append(message.message_id)
    global price
    global registered_user
    global product
    price = message.text
    bot_message = bot.send_message(message.chat.id, 'Создание товара завершено.')
    messages.append(bot_message.message_id)
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO products (category, name, descr, price, user_id ) VALUES ( "{category}", "{name}", "{descr}", "{price}", "{registered_user.id}" )')
    connection.commit()
    cursor.close()
    connection.close()
    product = Product(category=category, name=name, descr=descr, price=price, user_id=registered_user.id)

@bot.message_handler(commands=['info'])
def info(message):
    global product
    global registered_user

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM products WHERE user_id = "{registered_user.id}" ')
    products = cursor.fetchall()



    for product in products:
        bot.send_message(message.chat.id,f' {product[1]}, \n{product[2]}, \n{product[3]}, \n{product[4]}')


    cursor.close()
    connection.close()

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
    global registered_user
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

@bot.message_handler(commands=['show'])
def logout(message):
    global in_system
    if in_system:
        bot.send_message(message.chat.id, f'Айди: {registered_user.id}\n'
                                          f'Логин: {registered_user.login}\n'
                                          f'Пароль: {registered_user.password}')
    else:
        bot.send_message(message.chat.id, f'Вы не в системе. Пожалуйста войдите в систему')

    bot.delete_message()

@bot.message_handler(commands=['delete'])
def delete_user(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(f'DELETE FROM users WHERE id = "{id}" ')

    conn.commit()
    conn.close()



bot.infinity_polling()