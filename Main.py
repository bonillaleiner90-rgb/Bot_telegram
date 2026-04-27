import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

PALABRAS_ESTAFA = [
    "deposita","consigna","giro","nequi","daviplata","urgente",
    "mami","papi","hijo","preso","policia","abogado",
    "transferencia","ya mismo","codigos","clave","prestame"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👮 Guardia Anti-Estafas activo\n\nMándame cualquier mensaje sospechoso y te digo si huele a estafa.")

async def analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    coincidencias = sum(1 for palabra in PALABRAS_ESTAFA if palabra in texto)
    
    if coincidencias >= 2:
        respuesta = f"🚨 ALERTA DE ESTAFA 🚨\n\nEncontré {coincidencias} palabras sospechosas.\n\nNO envíes dinero. Llama a tu familiar directo para confirmar."
    elif coincidencias == 1:
        respuesta = f"⚠️ CUIDADO\n\nEncontré 1 palabra sospechosa.\nVerifica bien antes de hacer cualquier giro."
    else:
        respuesta = "✅ No detecto palabras de estafa comunes.\n\nIgual siempre desconfía y verifica."
    
    await update.message.reply_text(respuesta)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analizar))
    print("Bot iniciado...")
    app.run_polling()

if __name__ == '__main__':
    main()
