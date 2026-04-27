import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Panel import start, help_command, analizar_mensaje

TOKEN = os.environ.get("TOKEN")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, analizar_mensaje))

    print("Bot iniciado...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
