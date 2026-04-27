# IDs de familia real - NO alertar si ellos hablan
FAMILIA_REAL = [123456789, 987654321, 555444333] # Cambia por los IDs reales

# Palabras clave de estafa
KEYWORDS_ESTAFAS = ["nequi", "daviplata", "urgente", "soy tu hijo", "cambie de numero", "consignar", "transferir"]

# Links sospechosos  
LINKS_SOSPECHOSOS = [".xyz", ".tk", ".ml", "bit.ly", "tinyurl", "cutt.ly", "premio", "ganaste", "reclamar"]

async def detectar_estafa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower()
    user_id = update.effective_user.id
    
    # 1. LISTA BLANCA: Si es familia, no hacer nada
    if user_id in FAMILIA_REAL:
        return
    
    # 2. DETECTOR DE LINKS + PALABRAS CLAVE
    es_link_raro = any(link in mensaje for link in LINKS_SOSPECHOSOS)
    es_estafa_texto = any(palabra in mensaje for palabra in KEYWORDS_ESTAFAS)
    
    if es_link_raro or es_estafa_texto:
        alerta = """
🚨 ALERTA DE ESTAFA DETECTADA 🚨

❌ NO respondas
❌ NO des click a links
❌ NO mandes plata

🛡️ Guardia anti estafas BQ activado
📢 AVÍSALE A TU FAMILIA

Si tienes dudas, llama a tu familiar a su número de siempre.
"""
        await update.message.reply_text(alerta)
