from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

# TOKEN desde Railway Variables
TOKEN = os.environ.get('TOKEN')

# LISTA BLANCA - Pon nombres EXACTOS de Telegram
FAMILIA_BLANCA = ["Leiner Bonilla", "Lucely", "Yo"]

# PALABRAS QUE ACTIVAN LA ALARMA
PALABRAS_PROHIBIDAS = ["nequi", "daviplata", "codigo", "clave", "urgente", "transferencia", "prestamo"]

async def proteger_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message
    if not mensaje or not mensaje.text:
        return
    
    texto = mensaje.text.lower()
    usuario = mensaje.from_user.first_name
    user_id = mensaje.from_user.id
    
    # Si es de la familia, no hacer nada
    if any(nombre in usuario for nombre in FAMILIA_BLANCA):
        return
    
    # Buscar palabras prohibidas
    for palabra in PALABRAS_PROHIBIDAS:
        if palabra in texto:
            try:
                # 1. BORRA EL MENSAJE
                await mensaje.delete()
                
                # 2. EXPULSA AL ESTAFADOR - ANTI-FANTASMA
                await context.bot.ban_chat_member(
                    chat_id=mensaje.chat_id, 
                    user_id=user_id
                )
                
                # 3. MANDA ALERTA
                await context.bot.send_message(
                    chat_id=mensaje.chat_id,
                    text=f"🚨 ALERTA ROJA: AMENAZA ELIMINADA\n\n"
                         f"Usuario expulsado: {usuario}\n"
                         f"Motivo: Intento de estafa detectado\n"
                         f"Acción: Mensaje borrado + Usuario bloqueado\n\n"
                         f"🛡️ Guardia BQ: Tu familia sigue 100% protegida."
                )
                print(f"Estafador {usuario} expulsado")
                
            except Exception as e:
                print(f"Error al expulsar: {e}")
                await context.bot.send_message(
                    chat_id=mensaje.chat_id,
                    text=f"⚠️ No pude expulsar a {usuario}. Dame permiso de 'Restringir miembros'."
                )
            break

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, proteger_grupo))
    print("Guardia BQ 2.0 Activado...")
    app.run_polling()

if __name__ == '__main__':
    main()
