import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Guardian BQ Panel", page_icon="🛡️", layout="wide")
st.title("🛡️ Panel Guardian BQ")
st.subheader("Protección Digital pa' Negocios en Barranquilla")

conn = sqlite3.connect('clientes.db')
try:
    df = pd.read_sql_query("SELECT * FROM stats", conn)
except:
    st.error("Aún no hay datos. Usa el bot primero con /start")
    st.stop()

cliente = st.selectbox("🔍 Busca tu negocio:", df['cliente'].unique())
datos_cliente = df[df['cliente'] == cliente]

col1, col2, col3 = st.columns(3)
col1.metric("🚨 Estafas Bloqueadas", datos_cliente['estafas_bloqueadas'].sum())
col2.metric("📅 Activo desde", datos_cliente['fecha'].iloc[0])
col3.metric("👥 Grupo Protegido", cliente)

st.subheader("📊 Actividad del mes")
if len(datos_cliente) > 1:
    st.bar_chart(datos_cliente.set_index('fecha')['estafas_bloqueadas'])
else:
    st.info("Cuando bloqueemos más estafas, aquí verás el gráfico")

st.caption("Guardian BQ V2 | Soporte: Tu WhatsApp")
