import streamlit as st
from openai import OpenAI
import os

st.title("AI Coder - DeepSeek R1 Multimodal")

# DeepSeek API-Schlüssel direkt hier einfügen
api_key = os.getenv("DEEPSEEK_API_KEY", "sk-2c8fc6bcd4db4cefa226a4cc0e89e28e")  # ERSETZE DIES DURCH DEINEN TATSÄCHLICHEN API-SCHLÜSSEL

# DeepSeek-Client initialisieren
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# Chat-Verlauf (im Sitzungszustand)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Du bist ein hilfreicher Assistent mit multimodalen Fähigkeiten."}]

# Hochladen von Dateien
uploaded_files = st.file_uploader("Dateien hochladen (Jupyter Notebooks, Pickle-Files, Bilder, PDFs)", accept_multiple_files=True)

# Verarbeiten und Hochladen der Dateien zur API
file_data = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.read()
        file_data.append({
            "name": uploaded_file.name,
            "type": uploaded_file.type,
            "content": file_bytes
        })
        st.success(f"Datei {uploaded_file.name} hochgeladen.")

# Nachrichten anzeigen
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Benutzereingabe
prompt = st.chat_input("Deine Nachricht")
if prompt or file_data:
    user_message = {"role": "user", "content": prompt if prompt else "Datei(en) hochgeladen"}
    st.session_state.messages.append(user_message)
    with st.chat_message("user"):
        st.markdown(user_message["content"])

    # DeepSeek API-Aufruf mit Dateiunterstützung
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",  # DeepSeek R1 Multimodal
            messages=st.session_state.messages,
            files=file_data if file_data else None,  # Falls Dateien hochgeladen wurden
            stream=False,  # Stream-Parameter hinzugefügt, falls erforderlich
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        with st.chat_message("assistant"):
            st.markdown(msg)
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")







