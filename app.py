import streamlit as st
import requests
import pandas as pd
import json

API_URL = "https://xwsh8degbh.execute-api.us-east-1.amazonaws.com/prod/"

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Detector de emociones</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Detecta emociones en imágenes de personas</h2>", unsafe_allow_html=True)

if "historial" not in st.session_state:
    st.session_state.historial = []

col1, col2 = st.columns([1, 1])
with col1:
    uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Imagen cargada", width=300)
        image_bytes = uploaded_file.read()
        try:
            with st.spinner("🔄 Procesando imagen..."):
                response = requests.post(API_URL, data=image_bytes, headers={"Content-Type": "application/octet-stream"})
                data = response.json()
            if response.status_code != 200:
                st.error(f"❌ Error: {data['error']}")
                st.stop()
            else:
                st.session_state.historial.append({
                    "url": data["image_url"],
                    "emocion": data["emocion"],
                    "porcentaje": data["porcentaje"],
                    "emoji": data["emoji"]
                })
                st.success("✅ Emoción detectada:")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with col2:
    st.subheader("📊 Resultados anteriores:")
    if st.session_state.historial:
        for i, item in enumerate(reversed(st.session_state.historial), 1):
            st.markdown(f"### 📷 Imagen #{len(st.session_state.historial) - i + 1}")
            st.image(item["url"], width=300, caption="Miniatura procesada")
            st.write(f"🎭 **Emoción detectada:** {item['emocion']} {item['emoji']}")
            st.write(f"📊 **Confianza:** {item['porcentaje']}%")
            st.markdown(f"[🔗 Ver imagen en tamaño completo]({item['url']})", unsafe_allow_html=True)
            st.markdown("---")

