from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai
import os, sqlite3
from datetime import datetime

TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Base de datos simple
conn = sqlite3.connect('clientes.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS stats
               (chat_id TEXT, cliente TEXT, estafas_bloqueadas INTEGER, fecha TEXT)''')
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat_id)
    # Registra cliente nuevo
    cursor.execute("INSERT OR IGNORE INTO stats VALUES (?,?, 0,?)",
                   (chat_id, "Cliente Nuevo", datetime.now().strftime("%d-%m")))
    conn.commit()
    await update.message.reply_text(
        "🛡️ GUARDIAN BQ ACTIVADO\n\n"
        "Reenvíame cualquier mensaje sospechoso de estafa.\n"
        "Comandos:\n"
        "/stats - Ver estafas bloqueadas\n"
        "/empresa - Poner nombre de tu negocio"
    )

async def poner_empresa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = ' '.join(context.args)
    if not nombre:
        await update.message.reply_text("Uso: /empresa Tienda El Vecino")
        return
    chat_id = str(update.message.chat_id)
    cursor.execute("UPDATE stats SET cliente=? WHERE chat_id=?", (nombre, chat_id))
    conn.commit()
    await update.message.reply_text(f"✅ Listo. Ahora protejo a: {nombre}")

async def analizar_estafa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text
    chat_id = str(update.message.chat_id)
    await update.message.chat.send_action("typing")

    prompt = f"""Eres Guardian BQ, experto anti-estafas en Colombia.
    Analiza este mensaje: "{mensaje}"
    Responde SOLO con:
    1. RIESGO: ALTO/MEDIO/BAJO
    2. RAZÓN: 1 línea
    3. CONSEJO: 1 línea"""

    respuesta = model.generate_content(prompt)
    resultado = respuesta.text

    # Si es riesgo alto, suma 1 al contador
    if "ALTO" in resultado:
        cursor.execute("UPDATE stats SET estafas_bloqueadas = estafas_bloqueadas + 1 WHERE chat_id=?", (chat_id,))
        conn.commit()
        resultado += "\n\n🚨 Bloqueada y reportada en tu panel."

    await update.message.reply_text(resultado)

async def ver_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat_id)
    cursor.execute("SELECT cliente, estafas_bloqueadas FROM stats WHERE chat_id=?", (chat_id,))
    data = cursor.fetchone()
    if data:
        await update.message.reply_text(f"📊 PANEL {data[0]}\n\nEstafas bloqueadas este mes: {data[1]}\n\nPanel web: https://guardianbq.streamlit.app")
    else:
        await update.message.reply_text("Usa /start primero")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("empresa", poner_empresa))
    app.add_handler(CommandHandler("stats", ver_stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analizar_estafa))
    print("Guardian BQ V2 corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
