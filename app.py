import streamlit as st
from openai import OpenAI
import nbformat

st.title("AI Coder")

# DeepSeek API-Schlüssel direkt hier einfügen
api_key = "sk-8981cca98489449489e2951c8b032959"
#api_key = st.secrets["API_KEY"] # ERSETZE DIES DURCH DEINEN TATSÄCHLICHEN API-SCHLÜSSEL


# DeepSeek-Client initialisieren
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# Chat-Verlauf (im Sitzungszustand)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Du bist ein hilfreicher Assistent."}]

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

    # DeepSeek API-Aufruf
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",  # DeepSeek R1
            messages=st.session_state.messages,
            stream=False  # Stream-Parameter hinzugefügt, falls erforderlich
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        with st.chat_message("assistant"):
            st.markdown(msg)
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")
