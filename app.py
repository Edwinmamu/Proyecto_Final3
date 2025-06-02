import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import requests

# Configurar la API de Gemini (SDK actualizado)
genai.configure(api_key="AIzaSyDIXqMCSXXX4FF8ZX-D22MSEsBABswVaCY")
modelo = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="Agencia de Viajes", layout="wide")

url = "http://localhost:3000/destinos"
response = requests.get(url)
data = response.json()
df_visible = pd.DataFrame(data)

# Limpieza de columnas clave para evitar errores de filtrado y mostrar datos coherentes
df_visible["pais"] = df_visible["pais"].astype(str).str.strip().str.title()
df_visible["categoria"] = df_visible["categoria"].astype(str).str.strip().str.title()
df_visible["ciudad"] = df_visible["ciudad"].astype(str).str.strip().str.title()




# Sidebar
st.sidebar.title("🌍 PLANIT")
menu = st.sidebar.radio("Selecciona una sección:", ["Inicio", "Por Categoría", "Por Gasto", "Por Visitantes", "Por País", "Gemini"])

st.sidebar.title("🔍 Filtros")
paises = st.sidebar.multiselect("Filtrar por país", sorted(df_visible['pais'].unique()))
categorias = st.sidebar.multiselect("Filtrar por categoría", sorted(df_visible['categoria'].unique()))

df_v = df_visible.copy()
if paises:
    df_v = df_v[df_v['pais'].isin(paises)]
if categorias:
    df_v = df_v[df_v['categoria'].isin(categorias)]

# Inicio
if menu == "Inicio":
    st.title("📋 Resumen de Destinos Turísticos")
    df_resumen = df_v.sort_values(by=["pais", "visitas"], ascending=[True, False])
    st.dataframe(
        df_resumen[["nombre", "pais", "ciudad", "categoria", "visitas", "gasto_promedio", "avg_spending_usd"]].rename(columns={
            "nombre": "Lugar turístico",
            "pais": "País",
            "ciudad": "Ciudad",
            "categoria": "Categoría",
            "visitas": "Visitantes",
            "gasto_promedio": "Gasto Prom. (Moneda Local)",
            "avg_spending_usd": "Gasto Prom. (USD)"
        }),
        use_container_width=True
    )

elif menu == "Por Categoría":
    st.title("🌍 Destinos por Categoría")
    seleccion = st.selectbox("Selecciona una categoría", df_v["categoria"].unique())
    st.dataframe(df_v[df_v["categoria"] == seleccion])

elif menu == "Por Gasto":
    st.title("💸 Destinos más costosos")
    pais = st.selectbox("Selecciona un país", df_v["pais"].unique(), key="gasto")
    top_destinos = df_v[df_v["pais"] == pais].sort_values(by="avg_spending_usd", ascending=False).head(5)
    st.subheader(f"Top destinos más costosos en {pais}")
    st.dataframe(
        top_destinos[["nombre", "gasto_promedio", "avg_spending_usd"]].rename(columns={
            "nombre": "Destino",
            "gasto_promedio": "Gasto Promedio (Moneda Local)",
            "avg_spending_usd": "Gasto Promedio (USD)"
        }),
        use_container_width=True
    )
    fig = px.pie(top_destinos, names="nombre", values="avg_spending_usd",
                 title=f"Distribución del gasto promedio (USD) en {pais}",
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition="inside", texttemplate="%{label}<br>$%{value:,.0f} USD")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Por Visitantes":
    st.title("👥 Destinos más visitados")
    top_visited = df_v.sort_values(by="visitas", ascending=False).head(10)
    top_visited["Destino"] = top_visited["nombre"] + " (" + top_visited["pais"] + ")"
    fig = px.bar(top_visited, x="Destino", y="visitas", color="categoria", title="Top destinos por visitantes")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Por País":
    st.title("📍 Análisis por País")
    country = st.selectbox("Selecciona un país", df_v["pais"].unique(), key="pais")
    tipo_grafico = st.selectbox("Selecciona el tipo de visualización", ["Barras", "Líneas"], key="tipo_grafico")
    data_country = df_v[df_v["pais"] == country].sort_values(by="avg_spending_usd", ascending=False)
    if tipo_grafico == "Barras":
        fig = px.bar(data_country, x="nombre", y="avg_spending_usd", color="categoria",
                     title=f"Gasto promedio por ciudad en {country}",
                     labels={"nombre": "Ciudad", "avg_spending_usd": "Gasto Promedio (USD)"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.line(data_country, x="nombre", y="avg_spending_usd", markers=True,
                      title=f"Gasto promedio por ciudad en {country}",
                      labels={"nombre": "Ciudad", "avg_spending_usd": "Gasto Promedio (USD)"})
        st.plotly_chart(fig, use_container_width=True)

# Gemini
elif menu == "Gemini":
    st.title("🤖 Chat Turístico con Gemini")
    st.info("Puedes escribir una sola palabra como 'colombia', 'gasto méxico' o 'playa' para obtener información contextual.")

    pregunta = st.text_input("Escribe tu búsqueda o palabra clave:")
    enviar = st.button("Generar Respuesta")

    def generar_prompt_contextualizado(pregunta, df):
        pregunta = pregunta.lower()
        contexto = """
Eres un asistente turístico inteligente y útil que recomienda destinos alrededor del mundo con base en datos actualizados. 
A continuación se presenta información del usuario que debe ser tenida en cuenta para ofrecer una respuesta clara, contextualizada y útil.

### Datos disponibles:
- Sitios turísticos más relevantes de cada país (por visitas y gasto promedio)
- Categorías: Aventura, Cultural, Natural, Playa, Histórico, Romántico, Urbano, Económico, Moderno, Misterioso, Espiritual.
- Gasto promedio en moneda local y en USD
- Número de visitantes
- Ciudades asociadas a los destinos

### Considera también:
- Temporadas del año (invierno, verano, etc.) si se menciona en la pregunta
- Ofrece consejos prácticos de viaje si aplica (clima, transporte, idioma, moneda)
- Si el usuario pregunta por un país, responde con los destinos más visitados o recomendados en ese país
- Si el usuario menciona una ciudad, ofrece información del destino en esa ciudad
- Si el usuario menciona una categoría (como “playa” o “aventura”), responde con sitios destacados en esa categoría
- Si el usuario pregunta por "gasto", ofrece sitios con mayor o menor gasto promedio
- Si el usuario pregunta por "temporada", recomienda destinos ideales para esa época
"""

        for pais in df["pais"].unique():
            if pais.lower() in pregunta:
                destinos = df[df["pais"] == pais]["nombre"].unique()
                lista = ", ".join(destinos[:5])
                contexto += f"\n🌍 Los destinos turísticos más importantes en {pais} son: {lista}."

        for cat in df["categoria"].str.lower().unique():
            if cat in pregunta:
                destinos = df[df["categoria"].str.lower() == cat]["nombre"].unique()
                lista = ", ".join(destinos[:5])
                contexto += f"\n🌴 Destinos destacados en la categoría '{cat}': {lista}."

        if pregunta.startswith("gasto "):
            pais = pregunta.replace("gasto ", "").capitalize()
            if pais in df["pais"].values:
                top = df[df["pais"] == pais].sort_values(by="avg_spending_usd", ascending=False)
                gastos = [f"{row['nombre']}: {row['gasto_promedio']} / ${row['avg_spending_usd']} USD" for _, row in top.iterrows()]
                contexto += f"\n🧾 Gasto promedio en {pais}: " + ", ".join(gastos[:5])

        for ciudad in df["ciudad"].dropna().unique():
            if ciudad.lower() in pregunta:
                destinos = df[df["ciudad"] == ciudad]["nombre"].unique()
                contexto += f"\n🏙️ En la ciudad de {ciudad} se encuentran sitios como: {', '.join(destinos[:5])}."

        for temporada in ["invierno", "verano", "otoño", "primavera"]:
            if temporada in pregunta:
                contexto += f"\n📅 La temporada {temporada} es ideal para visitar lugares como playas, zonas naturales y ciudades cálidas."

        return contexto + f"\n\n### Pregunta del usuario:\n{pregunta}\n\nGenera una respuesta detallada, útil y relevante."

    if enviar and pregunta:
        with st.spinner("Consultando a Gemini..."):
            try:
                prompt = generar_prompt_contextualizado(pregunta, df_v)
                respuesta = modelo.generate_content(prompt)
                st.subheader("Respuesta:")
                st.markdown(respuesta.text)
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
