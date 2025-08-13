import streamlit as st
import requests
import base64
import json

st.set_page_config(page_title="Texto <-> Audio", layout="wide")
st.title("🎤 Conversión de Texto ↔ Audio")

# URL de tu API
API_TEXTO_A_AUDIO = "https://xtix8s42ng.execute-api.us-east-1.amazonaws.com/default/Trancripcion"

col1, col2 = st.columns(2)

# -------------------
# COLUMNA 1: Texto -> Audio
# -------------------
with col1:
    st.header("📝 Texto → 🔊 Audio")
    texto = st.text_area("Escribe el texto a convertir", height=150)
    if st.button("Generar Audio"):
        if texto.strip():
            # Ejemplo de envío de texto a la API
            response = requests.post(API_TEXTO_A_AUDIO, json={"mode" : "text-to-audio", "text": texto})
            print (response)
            if response.status_code == 200:
                audio_base64 = response.json().get("audio_base64")
                print(audio_base64)
                
                if audio_base64:
                    audio_bytes = base64.b64decode(audio_base64)
                    st.audio(audio_bytes, format="audio/mp3")
                else:
                    st.error("No se recibió audio de la API.")
            else:
                st.error(f"Error en la API: {response.status_code}")
        else:
            st.warning("Por favor ingresa un texto.")

# -------------------
# COLUMNA 2: Audio -> Texto
# -------------------
with col2:
    st.header("🔊 Audio → 📝 Texto")
    audio_file = st.file_uploader("Sube un archivo de audio", type=["mp3", "wav", "m4a"])
    if st.button("Transcribir Audio"):
        if audio_file is not None:
            # Convertir el archivo a Base64
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

            # Enviar a la API
            response = requests.post(
                API_TEXTO_A_AUDIO,
                json={"mode": "audio-to-text", "audio_base64": audio_base64}
            )

            if response.status_code == 200:
                transcripcion = response.json().get("texto")
                if transcripcion:
                    st.success("Texto transcrito:")
                    st.write(transcripcion)
                else:
                    st.error("No se recibió texto de la API.")
            else:
                st.error(f"Error en la API: {response.status_code}")
        else:
            st.warning("Por favor sube un archivo de audio.")
