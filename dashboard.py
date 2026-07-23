import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# ======================================================
# LOGIN
# ======================================================

USUARIO = "admin"
PASSWORD = "123456"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:

    st.set_page_config(
        page_title="Login",
        page_icon="🔐",
        layout="centered"
    )

    st.title("🔐 Inicio de Sesión")
    st.write("Ingrese sus credenciales para acceder al Dashboard.")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar", use_container_width=True):

        if usuario == USUARIO and password == PASSWORD:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos.")

    # Detiene la ejecución para que no se cargue el dashboard
    st.stop()

# ======================================================
# DASHBOARD
# ======================================================

st.set_page_config(
    page_title="Dashboard Ventas Laptops",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Dashboard de Ventas de Laptops")

# Botón para cerrar sesión
if st.sidebar.button("🚪 Cerrar sesión"):
    st.session_state.autenticado = False
    st.rerun()

# ---------------------------------------
# CONEXIÓN MYSQL
# ---------------------------------------

conexion = mysql.connector.connect(
    host="sql10.freesqldatabase.com",
    user="sql10833126",
    password="K9UJ4pHHZS",
    database="sql10833126"
)

consulta = """
SELECT
id_venta,
fecha_venta,
distrito,
marca,
modelo,
categoria,
precio_soles,
cantidad
FROM ventas_laptops;
"""

df = pd.read_sql(consulta, conexion)

conexion.close()

# ---------------------------------------
# FILTROS
# ---------------------------------------

st.sidebar.header("🔎 Filtros")

marca = st.sidebar.multiselect(
    "Marca",
    sorted(df["marca"].unique()),
    default=sorted(df["marca"].unique())
)

categoria = st.sidebar.multiselect(
    "Categoría",
    sorted(df["categoria"].unique()),
    default=sorted(df["categoria"].unique())
)

distrito = st.sidebar.multiselect(
    "Distrito",
    sorted(df["distrito"].unique()),
    default=sorted(df["distrito"].unique())
)

texto = st.sidebar.text_input("Buscar modelo")

df_filtrado = df[
    (df["marca"].isin(marca)) &
    (df["categoria"].isin(categoria)) &
    (df["distrito"].isin(distrito))
]

if texto != "":
    df_filtrado = df_filtrado[
        df_filtrado["modelo"].str.contains(texto, case=False)
    ]

# ---------------------------------------
# KPIs
# ---------------------------------------

st.subheader("📊 Indicadores")

col1, col2, col3, col4 = st.columns(4)

ventas = len(df_filtrado)
ingresos = (df_filtrado["precio_soles"] * df_filtrado["cantidad"]).sum()
precio_promedio = df_filtrado["precio_soles"].mean()
unidades = df_filtrado["cantidad"].sum()

col1.metric("Ventas", ventas)
col2.metric("Ingresos", f"S/ {ingresos:,.2f}")
col3.metric("Precio Promedio", f"S/ {precio_promedio:,.2f}")
col4.metric("Unidades Vendidas", unidades)

st.divider()

# ---------------------------------------
# GRÁFICOS
# ---------------------------------------

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        df_filtrado.groupby("marca")["cantidad"].sum().reset_index(),
        x="marca",
        y="cantidad",
        color="marca",
        title="Cantidad Vendida por Marca"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        df_filtrado,
        names="categoria",
        title="Ventas por Categoría"
    )
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    ventas_distrito = df_filtrado.groupby("distrito")["cantidad"].sum().reset_index()

    fig = px.bar(
        ventas_distrito,
        x="distrito",
        y="cantidad",
        color="distrito",
        title="Ventas por Distrito"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    ventas_fecha = df_filtrado.groupby("fecha_venta")["cantidad"].sum().reset_index()

    fig = px.line(
        ventas_fecha,
        x="fecha_venta",
        y="cantidad",
        markers=True,
        title="Evolución de Ventas"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# TOP 10 MODELOS
# ---------------------------------------

st.subheader("🏆 Top 10 Modelos")

top = (
    df_filtrado.groupby("modelo")["cantidad"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top,
    x="cantidad",
    y="modelo",
    orientation="h",
    color="cantidad",
    title="Top 10 Modelos Más Vendidos"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# TABLA
# ---------------------------------------

st.subheader("📋 Datos")

st.dataframe(df_filtrado, use_container_width=True)

# ---------------------------------------
# DESCARGAR CSV
# ---------------------------------------

csv = df_filtrado.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Descargar CSV",
    csv,
    file_name="ventas_laptops.csv",
    mime="text/csv"
)
