from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    update.message.reply_text('👮 Guardia Anti-Estafas activo\n\nMándame cualquier mensaje sospechoso y lo analizo.')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Solo reenvíame el mensaje, link o número que te parece estafa y te digo si es peligroso.')

def analizar_mensaje(update: Update, context: CallbackContext):
    texto = update.message.text.lower()
    
    # Palabras clave de estafa
    estafa_keywords = ['nequi', 'daviplata', 'premio', 'ganaste', 'bitcoin', 'inversion', 'prestamo', 'link', 'http', 'urgente']
    
    if any(word in texto for word in estafa_keywords):
        respuesta = "🚨 ALERTA DE ESTAFA 🚨\n\nEste mensaje tiene palabras típicas de estafa. NO des click a links ni mandes plata."
    else:
        respuesta = "✅ No detecto palabras de estafa obvias. Igual ten cuidado y nunca des datos personales."
    
    update.message.reply_text(respuesta)
