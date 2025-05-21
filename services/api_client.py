import requests
import pandas as pd
import streamlit as st

def fetch_tourism_data():
    try:
        response = requests.get("http://localhost:3000/users")
        response.raise_for_status()  # lanza excepción si status != 200
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener datos del servidor: {e}")
        return pd.DataFrame()
