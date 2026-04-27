import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Guardia Anti Estafas BQ", layout="wide")
st.title("🛡️ Panel Guardian BQ")
st.subheader("Protección Digital para Barranquilla")

# CAMBIO 1: Ahora lee estafas.db no clientes.db
conn = sqlite3.connect('estafas.db')

try:
    # CAMBIO 2: Leer tabla usuarios
    df_usuarios = pd.read_sql_query("SELECT * FROM usuarios", conn)
    df_alertas = pd.read_sql_query("SELECT * FROM alertas", conn)
except:
    st.error("Aún no hay datos. Usa el bot de Telegram y envía /start")
    st.stop()

st.success(f"✅ Usuarios registrados: {len(df_usuarios)}")
st.success(f"🚨 Alertas detectadas: {len(df_alertas)}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Usuarios Activos")
    if len(df_usuarios) > 0:
        st.dataframe(df_usuarios)
    else:
        st.info("Nadie ha usado /start aún")

with col2:
    st.subheader("🚨 Últimas Alertas")
    if len(df_alertas) > 0:
        st.dataframe(df_alertas.sort_values('fecha', ascending=False))
    else:
        st.info("No se han detectado estafas aún")

conn.close()
