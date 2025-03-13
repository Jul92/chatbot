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

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
        st.write(f"Hochgeladene Datei: {file_details}")
        
        # Speichern der Datei auf dem Server
        with open(os.path.join("temp", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Datei {uploaded_file.name} gespeichert.")

# Nachrichten anzeigen
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Benutzereingabe
prompt = st.chat_input("Deine Nachricht")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # DeepSeek API-Aufruf mit multimodaler Unterstützung
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",  # DeepSeek R1 Multimodal
            messages=st.session_state.messages,
            files=uploaded_files if uploaded_files else None,  # Falls Dateien hochgeladen wurden
            stream=False,  # Stream-Parameter hinzugefügt, falls erforderlich
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        with st.chat_message("assistant"):
            st.markdown(msg)
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")






