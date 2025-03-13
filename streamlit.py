import streamlit as st
from openai import OpenAI

# DeepSeek API-Schlüssel (ersetze durch deinen eigenen Schlüssel)
API_KEY = "DEIN_API_SCHLÜSSEL_HIER"
BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-coder-v2"

# OpenAI Client für DeepSeek-Coder-V2 initialisieren
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

st.title("DeepSeek Coder V2 Chatbot")

# Chat-Verlauf im Sitzungszustand speichern
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Du bist ein hilfreicher KI-Coding-Assistent."}]

# Bisherige Nachrichten anzeigen
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Benutzereingabe erfassen
prompt = st.chat_input("Deine Nachricht eingeben...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API-Anfrage an DeepSeek-Coder-V2
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=st.session_state.messages,
        )
        
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        with st.chat_message("assistant"):
            st.markdown(msg)
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")

