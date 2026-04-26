import os
import telebot

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'hola'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola bro! Soy tu bot 24/7 🔥")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Dijiste: {message.text}")

print("Bot iniciado...")
bot.polling()
