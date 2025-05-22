import streamlit as st
import plotly.express as px
from services.api_client import fetch_tourism_data
from utils.filters import *
from google import genai

st.set_page_config(page_title="Agencia de Viajes", layout="wide")

df = fetch_tourism_data()

st.title("✈️ Agencia de Viajes Planit")
st.markdown("""
Bienvenido a la plataforma de análisis de destinos turísticos más populares del mundo.
Aquí podrás explorar destinos por categoría, gasto, visitantes y mucho más usando gráficos interactivos.
""")

tabs = st.tabs(["🏠 Inicio", "🌍 Por Categoría", "💸 Por Gasto", "👥 Por Visitantes", "📍 Por País ", "🤖 Gemini"])

# 🏠 Inicio
with tabs[0]:
    st.subheader("Visión general")
    st.dataframe(df)
    
    
    
# 🌍 Por Categoría
with tabs[1]:
    st.subheader("Filtrar por categoría")
    categorias = df["categoria"].unique()
    seleccion = st.selectbox("Selecciona una categoría", categorias)
    st.dataframe(df[df["categoria"] == seleccion])



# 💸 Por Gasto
with tabs[2]:
    st.subheader("Destinos más costosos en cada país")
    
    paises = df['pais'].unique()
    pais_seleccionado = st.selectbox("Selecciona un país", paises, key="selectbox_gasto")

    destinos_filtrados = df[df['pais'] == pais_seleccionado]
    top_destinos = destinos_filtrados.sort_values(by='avg_spending_usd', ascending=False).head(5)

    fig = px.pie(
        top_destinos,
        names='nombre',
        values='avg_spending_usd',
        title=f"Top destinos más costosos en {pais_seleccionado}",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    st.plotly_chart(fig, use_container_width=True)


# 👥 Por Visitantes
with tabs[3]:
    st.subheader("Top destinos por cantidad de visitantes")
    top_visited = filter_by_top_visitors(df)

    # Crear columna combinada con nombre y país
    top_visited['Destino (Pais)'] = top_visited['nombre'] + " (" + top_visited['pais'] + ")"

    fig = px.bar(
        top_visited,
        x="Destino (Pais)",
        y="visitas",
        color="categoria",  
        title="Top destinos por visitantes (con país)",
        labels={
            "visitas": "Cantidad de visitantes",
            "Destino (Pais)": "Destino"
        }
    )
    st.plotly_chart(fig)



# 📍 Por País
with tabs[4]:
    countries = df['pais'].unique()
    country = st.selectbox("Selecciona un país", countries, key="selectbox_pais")
    filtered = filter_by_country(df, country)
    fig = px.bar(filtered, x="nombre", y="avg_spending_usd", color="categoria", title=f"Gasto promedio en ciudades de {country}")
    st.plotly_chart(fig)

# 🤖 Gemini
with tabs[5]:
    st.subheader("Chat con Gemini")
    st.info("Ingresa un tema o pregunta para obtener una respuesta generada por Gemini.")
    # markdown
    prompt = st.text_input("Escribe tu pregunta o tema:", placeholder="Ej. Explica cómo funciona la IA en pocas palabras")
    enviar = st.button("Generar Respuesta")

    # Función que usa el código original
    def generar_respuesta(prompt):
        if not prompt:
            return "Por favor, ingresa un tema o pregunta."
        try:
            client = genai.Client(api_key="AIzaSyDBqlHTXUWbP0Py86QmLnn1bzvwVpnAfw4")  # Código original
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt  # Código original con prompt dinámico
            )
            return response.text  # Código original
        except Exception as e:
            return f"Error: {str(e)}"

    # Lógica principal
    if enviar and prompt:
        with st.spinner("Generando respuesta..."):
            respuesta = generar_respuesta(prompt)
            st.subheader("Respuesta:")
            st.markdown(respuesta)
    else:
        st.info("Escribe un tema o pregunta y haz clic en Generar Respuesta.")

