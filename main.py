from telebot import TeleBot

token = '6529165154:AAH_5yolucmi9bjeXhVHip6Pc45Vm0WVyAo'
bot = TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello!')

bot.infinity_polling()
