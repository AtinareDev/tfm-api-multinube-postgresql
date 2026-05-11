import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="TFM API Multinube",
    page_icon="☁️",
    layout="centered",
)

st.title("TFM - API Multinube")
st.write("Aplicación cliente para consumir la API multinube con PostgreSQL.")

st.subheader("Estado de la API")

try:
    response = requests.get(f"{API_URL}/health", timeout=5)

    if response.status_code == 200:
        st.success("La API está funcionando correctamente.")
        st.json(response.json())
    else:
        st.error(f"La API respondió con código {response.status_code}.")
        st.text(response.text)

except requests.exceptions.RequestException as error:
    st.error("No se pudo conectar con la API.")
    st.text(str(error))