# 🌍 Planit - Agencia de Viajes Inteligente

Aplicación web interactiva desarrollada con **Streamlit** que permite explorar destinos turísticos internacionales a través de visualizaciones, filtros dinámicos y consultas con inteligencia artificial (Gemini). Los datos se consumen desde un simulador de API local utilizando **Mockoon**.

---

## 🚀 Funcionalidades principales

- 📊 Visualización por categoría, país, gasto promedio y visitas
- 🧭 Filtros interactivos por país y tipo de turismo
- 🤖 Asistente turístico inteligente (Gemini)
- 🌐 Datos servidos desde una API local Mockoon
- 📍 Información enriquecida por ciudad, temporada, gasto, visitantes y consejos

---

## 📦 Estructura del proyecto

Proyecto_Final/
│
├── app.py # Aplicación principal en Streamlit
├── requirements.txt # Dependencias del proyecto
├── README.md # Este archivo
├── .gitignore # Exclusiones de Git
├── mockoon/
│ └── agencia_viajes_env.json # Configuración del entorno Mockoon
└── data/
└── Sitios-turisticos-final-limpio.json # (usado antes, ahora vía API)

---

## 🛠️ Requisitos

- Python 3.10+
- Streamlit
- Pandas
- Plotly
- Requests
- Google GenerativeAI SDK (`google-generativeai`)
- Mockoon (simulador de API REST)

---

## 🔧 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/Edwinmamu/Proyecto_Final3.git
cd Proyecto_Final3
Crea un entorno virtual y actívalo:


python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS
Instala las dependencias:


pip install -r requirements.txt
Inicia Mockoon y asegúrate de que la API local funcione en http://localhost:3000/destinos.

Ejecuta la app:


streamlit run app.py
🤖 Configuración de Gemini
Agrega tu clave de API de Google Gemini directamente en app.py (no recomendado en producción) o usa variables de entorno:


genai.configure(api_key="TU_API_KEY")
🧪 Demo rápida
Pregunta en la sección Gemini cosas como:

Colombia

playa

gasto México

verano Italia