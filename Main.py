async def proteger_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message
    if not mensaje or not mensaje.text:
        return
    
    texto = mensaje.text.lower()
    usuario = mensaje.from_user.first_name
    user_id = mensaje.from_user.id
    
    # Si es de la familia, no hacer nada
    if usuario in FAMILIA_BLANCA:
        return
    
    # Buscar palabras prohibidas
    for palabra in PALABRAS_PROHIBIDAS:
        if palabra in texto:
            try:
                # 1. BORRA EL MENSAJE
                await mensaje.delete()
                
                # 2. EXPULSA AL ESTAFADOR DEL GRUPO 🔥 NUEVO
                await context.bot.ban_chat_member(
                    chat_id=mensaje.chat_id, 
                    user_id=user_id
                )
                
                # 3. MANDA ALERTA PRO
                await context.bot.send_message(
                    chat_id=mensaje.chat_id,
                    text=f"🚨 ALERTA ROJA: AMENAZA ELIMINADA\n\n"
                         f"Usuario expulsado: {usuario}\n"
                         f"Motivo: Intento de estafa\n"
                         f"Acción: Mensaje borrado + Usuario bloqueado\n\n"
                         f"🛡️ Guardia BQ: Tu familia sigue 100% protegida.\n"
                         f"NUNCA volverá a molestar."
                )
                print(f"Estafador {usuario} expulsado del grupo")
                
            except Exception as e:
                print(f"Error al expulsar: {e}")
                # Si falla expulsar, al menos avisa
                await context.bot.send_message(
                    chat_id=mensaje.chat_id,
                    text=f"⚠️ No pude expulsar a {usuario}. Revísame los permisos de Admin."
                )
            break
