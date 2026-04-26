import os
import telebot

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

PALABRAS_ESTAFAS = ['soy tu hijo', 'nequi', 'daviplata', 'urge', 'emergencia', 'transferir', 'prestame', 'mami', 'papi', 'plata', 'consignar', 'bancolombia', 'cuenta', 'deposito', 'giro']

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🛡️ Guardia anti estafas BQ activado\n\nReenvíame cualquier mensaje sospechoso y lo analizo")

@bot.message_handler(func=lambda message: True)
def detectar_estafa(message):
    texto = message.text.lower()
    
    for palabra in PALABRAS_ESTAFAS:
        if palabra in texto:
            bot.reply_to(message, 
                "🚨 ALERTA DE ESTAFA DETECTADA 🚨\n\n"
                "❌ NO respondas\n"
                "❌ NO des click\n" 
                "❌ NO mandes plata\n\n"
                "🛡️ Guardia anti estafas BQ activado\n\n"
                "📢 AVÍSALE A TU FAMILIA"
            )
            return

print("Bot iniciado...")
bot.polling()
