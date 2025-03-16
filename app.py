import streamlit as st
from openai import OpenAI
import nbformat
import requests

# ========== Functions ===========
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
        result = {key: data[key][0]
                  for key in ["ids", "documents", "distances"]}
        return result

    else:
        return -1



# ========== App Appearance ==========
st.title("AI Coder")

st.sidebar.markdown("## Parameters")
st.sidebar.divider()
option = st.sidebar.radio(
    "Choose your helper:",
    ["Havard CS50 Database", "Deepseek", "Deepseek Coder"]
)
database_results = 3
max_distance = 1

if option == "Havard CS50 Database":
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



# ========== Deepseek setup ==========
api_key = "sk-8981cca98489449489e2951c8b032959"
#api_key = st.secrets["API_KEY"] # ERSETZE DIES DURCH DEINEN TATSÄCHLICHEN API-SCHLÜSSEL
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)



# ========== Chat ==========
# Chat-start
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# view all messages permanently
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
prompt = st.chat_input("Your message")



# ========== Chatbot answer ==========

if prompt:

    # Call Havard Database:
    if option == "Havard CS50 Database":

        # Call Datenbank
        results = call_vector_database(prompt, number_data= database_results)
        min_distance = min(results["distances"])        # minimum distance in similarity search

        # Write message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get data from database
        if results != -1 and min_distance <= max_distance:
            # DeepSeek API-Aufruf
            try:
                # Define new prompt with input from vector database
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

                # Get result of rag_prompt from deepseek
                response = client.chat.completions.create(
                    model="deepseek-reasoner",  # DeepSeek R1
                    messages=st.session_state.messages,
                    stream=False
                )
                msg = response.choices[0].message.content

                # Write session with answer
                st.session_state.messages.pop()
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": msg})
                with st.chat_message("assistant"):
                    st.markdown(msg)

            except Exception as e:
                st.error(f"An error occured: {e}")

        # no good data found
        elif results != -1 and min_distance > max_distance:
            msg = "Unfortunately there is no data in the CS50 database with the parameters you have set. Therefore, I cannot answer your question."
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": msg})
            with st.chat_message("assistant"):
                st.markdown(msg)

        # database doesn't respond
        else:
            st.error("There is no access to the CS50 database.")



    # Call Deepseek
    elif option == "Deepseek":
        # Write message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # DeepSeek API
        try:
            response = client.chat.completions.create(
                model="deepseek-reasoner",  # DeepSeek R1
                messages=st.session_state.messages,
                stream=False
            )

            # Write session with answer
            msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg})
            with st.chat_message("assistant"):
                st.markdown(msg)

        except Exception as e:
            st.error(f"An error occured: {e}")

    # Call Coder to solve jupyter notebooks
    else:
        st.error(f"Coder is not implemented yet")
