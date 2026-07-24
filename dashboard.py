
import streamlit as st          
import pandas as pd
import mysql.connector 


# INFORMACIÓN DE CONEXIÓN A LA BASE DE DATOS
try:
    conexion_db = mysql.connector.connect(
        host="sql10.freesqldatabase.com",
        user="sql10833735",
        password="9UeFiiSCXD",
        database="sql10833735"
    )

    consulta_sql = "SELECT * FROM ventas_vehiculos" 
    df = pd.read_sql(consulta_sql, conexion_db)     

except Exception as error:
    print(f"SE ENCONTRÓ UN PROBLEMA: {error}")
    

# CONFIGURACIÓN DE DASHBOARD CON STREAMLIT:

st.set_page_config(page_title = "Wigo Motors", 
                   layout="wide")      

st.title("WIGO MOTORS S.A.C.")                      
st.subheader("Buscador comercial") 

st.sidebar.header("Buscador")
tipo_busqueda = st.sidebar.selectbox("Seleccione tipo de búsqueda", ["Marca", "Asesor comercial", "Sede"])  

df_filtrado = df.copy()     # Haciendo una copia del DataFrame 


# FILTRO POR MARCA:

if tipo_busqueda == "Marca":
    valor = st.sidebar.selectbox("Seleccionar marca", df["marca"].unique()) # Mostrar las marcas disponibles y sin repetir
    df_filtrado = df[df["marca"] == valor]                                   # Filtrar búsqueda por marca  
    
elif tipo_busqueda == "Asesor comercial":
    valor = st.sidebar.selectbox("Seleccionar asesor", df["asesor_comercial"].unique()) # Mostrar las marcas disponibles y sin repetir
    df_filtrado = df[df["asesor_comercial"] == valor]                                   # Filtrar búsqueda por marca  
    
elif tipo_busqueda == "Sede":
    valor = st.sidebar.selectbox("Seleccionar sede", df["tienda"].unique()) # Mostrar las marcas disponibles y sin repetir
    df_filtrado = df[df["tienda"] == valor]                                   # Filtrar búsqueda por marca  
    

# MOSTRAR RESULTADOS (TABLA):

st.success(f"Registros encontrados: {len(df_filtrado)}")        # Mostrar la cantidad de filas encontradas (color verde)
st.dataframe(df_filtrado)


# INDICADORES GENERALES: 

st.subheader("Indicadores:")

c1, c2, c3, c4 = st.columns(4)          # CREANDO 4 COLUMNAS  

c1.metric("Precio Total", f"S/{df_filtrado["precio_venta"].sum():,.2f}")          # Calcular el total de monto 
c2.metric("Unidades vendidas", f"{df_filtrado["cantidad"].sum()}")                # Calcular el total de unidades vendidad
c3.metric("Precio promedio", f"S/{df_filtrado["precio_venta"].mean():,.2f}")      # Calculcar el precio promedio
c4.metric("Operaciones", len(df_filtrado))                                        # Cantidad de registros 

c5, c6, c7, c8 = st.columns(4)  

c5.metric("Precio más alto", f"S/{df_filtrado["precio_venta"].max():,.2f}")
c6.metric("Precio más bajo", f"S/{df_filtrado["precio_venta"].min():,.2f}")


# GRÁFICOS DE BARRAS EN STREAMLIT:

import plotly.express as px

# GRÁFICO 1
ventas = df_filtrado.groupby("marca")["cantidad"].sum().reset_index()

grafico01 = px.bar(
    ventas,
    x = "marca",
    y = "cantidad",
    title = "Ventas por Marca"
)


# GRÁFICO 2
promedio = df_filtrado.groupby("marca")["precio_venta"].mean().reset_index()

grafico02 = px.bar(
    promedio,
    x = "marca",
    y = "precio_venta",
    title = "Precio promedio por marca"
)



st.plotly_chart(grafico01)  # Mostrar el gráfico en el Dashboard
st.plotly_chart(grafico02) 
