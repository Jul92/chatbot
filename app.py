import streamlit as st
from openai import OpenAI
import nbformat
import requests

# ========== Functions ===============
# Call vector database
def call_vector_database(query_text, number_data):
    # Vector database API URL
    database_url = "https://vector-db-245941724758.europe-west1.run.app/call_db"
    params = {
        "query": query_text,
        "number_results": str(number_data)
    }

    # Make a GET request
    response = requests.get(database_url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        print("✅ Data received:")
        result = {key: data[key][0]
                  for key in ["ids", "documents", "distances"]}
        return result

    else:
        return -1


# ======== App skeleton ===========
st.title("AI Coder")

st.sidebar.markdown("## Parameters")
st.sidebar.divider()
option = st.sidebar.checkbox("Use CS50 Database")
database_results = st.sidebar.number_input(
    "Number of retrieved data: ",
    value = 3,
    min_value=1,
    max_value=20,
    step=1
)
max_distance = st.sidebar.number_input(
    "Maximum distance to embedded query: ",
    value = 1.00,
    min_value=0.01,
    step=0.01
)

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
    # Call Datenbank
    results = call_vector_database(prompt, number_data= database_results)
    print(results["distances"])

    # Write message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get data from database
    if results != -1 and option:
        # DeepSeek API-Aufruf
        try:
            # Neuer Prompt mit Vektor Datenbank
            db_txt_data = '/n/n'.join(results['documents'])
            rag_prompt = f"""

                        You are an assistent which answers questions based on knowledge which is provided to you.
                        While answering, you don't use your internal knowledge,
                        but solely the information in the "The knowledge" section.
                        You don't mention anything to the user about the povided knowledge.

                        The question: {prompt}

                        The knowledge: {db_txt_data}
                        """
            st.session_state.messages.append({"role": "user", "content": rag_prompt})

            # Prompt mit deepseek verbinden
            response = client.chat.completions.create(
                model="deepseek-reasoner",  # DeepSeek R1
                messages=st.session_state.messages,
                stream=False  # Stream-Parameter hinzugefügt, falls erforderlich
            )
            msg = response.choices[0].message.content

            # Session schreiben
            st.session_state.messages.pop()
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": msg})
            with st.chat_message("assistant"):
                st.markdown(msg)

        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")

    elif not option:
        st.session_state.messages.append({"role": "user", "content": prompt})

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

    else:
        st.error(f"Datenbank ist nicht erreichbar.")
