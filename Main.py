from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ Guardia anti estafas BQ ACTIVADO\n\n"
        "Estoy aquí para detectar estafas. Reenvíame cualquier mensaje sospechoso."
    )

async def detectar_estafa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    
    # Palabras clave de estafa
    if "soy tu hijo" in texto or "soy tu hija" in texto:
        await update.message.reply_text(
            "🚨 ALERTA DE ESTAFA DETECTADA 🚨\n\n"
            "❌ NO respondas\n"
            "❌ NO des click\n" 
            "❌ NO mandes plata\n\n"
            "🛡️ Los estafadores se hacen pasar por familiares.\n"
            "📢 AVÍSALE A TU FAMILIA"
        )
    elif "nequi" in texto or "daviplata" in texto or "plata" in texto or "urgente" in texto:
        await update.message.reply_text(
            "⚠️ POSIBLE ESTAFA ⚠️\n\n"
            "Te están pidiendo plata urgente por Nequi/Daviplata.\n"
            "1. Llama a tu familiar por teléfono\n"
            "2. NO transfieras sin confirmar\n"
            "3. Reporta el número"
        )
    elif "hola" in texto:
        await update.message.reply_text("Hola 👋 Soy el Guardia anti estafas. Reenvíame mensajes sospechosos.")
    else:
        await update.message.reply_text("Recibido. Si es una estafa escribe /alerta")

async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚨 ALERTA ACTIVADA 🚨\n"
        "Comparte este mensaje con tu familia:\n\n"
        "'OJO: Si te escriben pidiendo plata urgente diciendo que son tu hijo, ES ESTAFA. Llama primero.'"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("alerta", alerta))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detectar_estafa))
    print("Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
