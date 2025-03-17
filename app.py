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

def get_youtube_link(havard_id, havard_sources):
    # All sources in ids
    ids_list = havard_id.split('_')
    havard_key, havard_lecture, havard_time = ids_list[0], ids_list[1], ids_list[-1]
    # Get youtube Link
    havard_link_key = ""
    if havard_lecture != 'Artificial-Intelligence':
        havard_number = havard_lecture[7:9] if havard_lecture[7:9].isdigit() else havard_lecture[7]
        havard_link_key = havard_key + '_' + havard_lecture[:7] + havard_number
    else:
        havard_link_key = havard_key + '_' + havard_lecture

    # timestamp for youtube video
    hours, minutes, seconds = map(int, havard_time.split(":"))
    time_in_seconds = int(hours * 3600 + minutes * 60 + seconds)
    # Get markdown Code with link
    youtube_link = havard_sources[havard_link_key][:-1] + '&t=' + str(time_in_seconds) + 's)'

    return youtube_link



# ========== App Appearance ==========
st.title("AI Coder")

st.sidebar.markdown("## Parameters")
st.sidebar.divider()
option = st.sidebar.radio(
    "Choose your helper:",
    ["Harvard CS50 Database", "Deepseek", "Deepseek Coder"]
)

database_results = 3
max_distance = 1

havard_sources = {
	'CS50x_Lecture0': '[CS50x Lecture 0](https://www.youtube.com/watch?v=2WtPyqwTLKM)',  # CS50 CS50x lectures
	'CS50x_Lecture1': '[CS50x Lecture 1](https://www.youtube.com/watch?v=89cbCbWrM4U)',
	'CS50x_Lecture2': '[CS50x Lecture 2](https://www.youtube.com/watch?v=Y8qnryVy5sQ)',
	'CS50x_Lecture3': '[CS50x Lecture 3](https://www.youtube.com/watch?v=iCx3zwK8Ms8)',
	'CS50x_Lecture4': '[CS50x Lecture 4](https://www.youtube.com/watch?v=kcRdFGbzR1I)',
	'CS50x_Lecture5': '[CS50x Lecture 5](https://www.youtube.com/watch?v=aV8LlSmd1E8)',
	'CS50x_Lecture6': '[CS50x Lecture 6](https://www.youtube.com/watch?v=0eNc5lJfZFM)',
	'CS50x_Lecture7': '[CS50x Lecture 7](https://www.youtube.com/watch?v=ZA25WHO62ZA)',
	'CS50x_Lecture8': '[CS50x Lecture 8](https://www.youtube.com/watch?v=xiWUL3M9D8c)',
	'CS50x_Lecture9': '[CS50x Lecture 9](https://www.youtube.com/watch?v=1r-dFbPQ7Z8)',
	'CS50x_Lecture10': '[CS50x Lecture 10](https://www.youtube.com/watch?v=WGEy-Bu5Hos)',
	'CS50x_Artificial-Intelligence': '[CS50x Artificial Intelligence](https://www.youtube.com/watch?v=1HuD2ryeOLg)',
	'CS50-AI_Lecture0': '[CS50-AI Lecture 0](https://www.youtube.com/watch?v=WbzNRTTrX0g)',  # CS50 AI lectures
	'CS50-AI_Lecture1': '[CS50-AI Lecture 1](https://www.youtube.com/watch?v=HWQLez87vqM)',
	'CS50-AI_Lecture2': '[CS50-AI Lecture 2](https://www.youtube.com/watch?v=D8RRq3TbtHU)',
	'CS50-AI_Lecture3': '[CS50-AI Lecture 3](https://www.youtube.com/watch?v=qK46ET1xk2A)',
	'CS50-AI_Lecture4': '[CS50-AI Lecture 4](https://www.youtube.com/watch?v=-g0iJjnO2_w)',
	'CS50-AI_Lecture5': '[CS50-AI Lecture 5](https://www.youtube.com/watch?v=J1QD9hLDEDY)',
	'CS50-AI_Lecture6': '[CS50-AI Lecture 6](https://www.youtube.com/watch?v=QAZc9xsQNjQ)',
	'CS50-Business_Lecture1': '[CS50-Business Lecture 1](https://www.youtube.com/watch?v=Q2f9h_-_Fv4)',  # CS50 Business lectures
	'CS50-Business_Lecture2': '[CS50-Business Lecture 2](https://www.youtube.com/watch?v=31CxTRTi9ns)',
	'CS50-Business_Lecture3': '[CS50-Business Lecture 3](https://www.youtube.com/watch?v=JWqoTRWQWQM)',
	'CS50-Business_Lecture4': '[CS50-Business Lecture 4](https://www.youtube.com/watch?v=ggX6EO8gMJ4)',
	'CS50-Business_Lecture5': '[CS50-Business Lecture 5](https://www.youtube.com/watch?v=ggX6EO8gMJ4)',
	'CS50-Business_Lecture6': '[CS50-Business Lecture 6](https://www.youtube.com/watch?v=ngK97cSXWoM)',
	'CS50-Cybersecurity_Lecture0': '[CS50-Cybersecurity Lecture 0](https://www.youtube.com/watch?v=fJYdAN4Vh5c)',  # CS50 Cybersecurity lectures
	'CS50-Cybersecurity_Lecture1': '[CS50-Cybersecurity Lecture 1](https://www.youtube.com/watch?v=X3DVaMnl5n8)',
	'CS50-Cybersecurity_Lecture2': '[CS50-Cybersecurity Lecture 2](https://www.youtube.com/watch?v=9phdZjF8qOk)',
	'CS50-Cybersecurity_Lecture3': '[CS50-Cybersecurity Lecture 3](https://www.youtube.com/watch?v=5rsKrTh3fAo)',
	'CS50-Cybersecurity_Lecture4': '[CS50-Cybersecurity Lecture 4](https://www.youtube.com/watch?v=6IeqJtudKnk)',
	'CS50-for-Lawyers_Lecture1': '[CS50-for-Lawyers Lecture 1](https://www.youtube.com/watch?v=0OpqkCs871o)',  # CS50 for Lawyers lectures
	'CS50-for-Lawyers_Lecture2': '[CS50-for-Lawyers Lecture 2](https://www.youtube.com/watch?v=KCYiwhBel9U)',
	'CS50-for-Lawyers_Lecture3': '[CS50-for-Lawyers Lecture 3](https://www.youtube.com/watch?v=FnPn6RH-75M)',
	'CS50-for-Lawyers_Lecture4': '[CS50-for-Lawyers Lecture 4](https://www.youtube.com/watch?v=G9jJ9ge7UeE)',
	'CS50-for-Lawyers_Lecture5': '[CS50-for-Lawyers Lecture 5](https://www.youtube.com/watch?v=3CjkDQUu3Ow)',
	'CS50-for-Lawyers_Lecture6': '[CS50-for-Lawyers Lecture 6](https://www.youtube.com/watch?v=1bOQnBINfNs)',
	'CS50-for-Lawyers_Lecture7': '[CS50-for-Lawyers Lecture 7](https://www.youtube.com/watch?v=VFxdfTQSCXo)',
	'CS50-for-Lawyers_Lecture8': '[CS50-for-Lawyers Lecture 8](https://www.youtube.com/watch?v=7Jlbmg6b2UI)',
	'CS50-for-Lawyers_Lecture9': '[CS50-for-Lawyers Lecture 9](https://www.youtube.com/watch?v=KrCMU9hhD54)',
	'CS50-for-Lawyers_Lecture10': '[CS50-for-Lawyers Lecture 10](https://www.youtube.com/watch?v=a9mzwAljhnE)',
	'CS50-Python_Lecture0': '[CS50-Python Lecture 0](https://www.youtube.com/watch?v=JP7ITIXGpHk)',  # CS50 Python lectures
	'CS50-Python_Lecture1': '[CS50-Python Lecture 1](https://www.youtube.com/watch?v=_b6NgY_pMdw)',
	'CS50-Python_Lecture2': '[CS50-Python Lecture 2](https://www.youtube.com/watch?v=-7xg8pGcP6w)',
	'CS50-Python_Lecture3': '[CS50-Python Lecture 3](https://www.youtube.com/watch?v=LW7g1169v7w)',
	'CS50-Python_Lecture4': '[CS50-Python Lecture 4](https://www.youtube.com/watch?v=MztLZWibctI)',
	'CS50-Python_Lecture5': '[CS50-Python Lecture 5](https://www.youtube.com/watch?v=tIrcxwLqzjQ)',
	'CS50-Python_Lecture6': '[CS50-Python Lecture 6](https://www.youtube.com/watch?v=KD-Yoel6EVQ)',
	'CS50-Python_Lecture7': '[CS50-Python Lecture 7](https://www.youtube.com/watch?v=hy3sd9MOAcc)',
	'CS50-Python_Lecture8': '[CS50-Python Lecture 8](https://www.youtube.com/watch?v=e4fwY9ZsxPw)',
	'CS50-Python_Lecture9': '[CS50-Python Lecture 9](https://www.youtube.com/watch?v=6pgodt1mezg)',
	'CS50-R_Lecture1': '[CS50-R Lecture 1](https://www.youtube.com/watch?v=QkqotQEwvxc)',  # CS50 R lectures
	'CS50-R_Lecture2': '[CS50-R Lecture 2](https://www.youtube.com/watch?v=zBS0Vnq6JcA)',
	'CS50-R_Lecture3': '[CS50-R Lecture 3](https://www.youtube.com/watch?v=i0h8vp3A9j8)',
	'CS50-R_Lecture4': '[CS50-R Lecture 4](https://www.youtube.com/watch?v=wIPyom1ozW0)',
	'CS50-R_Lecture5': '[CS50-R Lecture 5](https://www.youtube.com/watch?v=ej187bgCIPw)',
	'CS50-R_Lecture6': '[CS50-R Lecture 6](https://www.youtube.com/watch?v=T4SktHZ17IU)',
	'CS50-R_Lecture7': '[CS50-R Lecture 7](https://www.youtube.com/watch?v=0q6jwG4ZPYc)',
	'CS50-Scratch_Lecture1': '[CS50-Scratch Lecture 1](https://www.youtube.com/watch?v=3pIdX9__-OI)',  # CS50 Scratch lectures
	'CS50-Scratch_Lecture2': '[CS50-Scratch Lecture 2](https://www.youtube.com/watch?v=M5ngdlBeUrM)',
	'CS50-Scratch_Lecture3': '[CS50-Scratch Lecture 3](https://www.youtube.com/watch?v=7P4QR2o3pME)',
	'CS50-Scratch_Lecture4': '[CS50-Scratch Lecture 4](https://www.youtube.com/watch?v=4psGe3sOAwo)',
	'CS50-Scratch_Lecture5': '[CS50-Scratch Lecture 5](https://www.youtube.com/watch?v=0GLECNrj_T4)',
	'CS50-Scratch_Lecture6': '[CS50-Scratch Lecture 6](https://www.youtube.com/watch?v=LTlVuFgBXSE)',
	'CS50-Scratch_Lecture7': '[CS50-Scratch Lecture 7](https://www.youtube.com/watch?v=PWdijfqVvqs)',
	'CS50-Scratch_Lecture8': '[CS50-Scratch Lecture 8](https://www.youtube.com/watch?v=D1WjtbQj8sM)',
	'CS50-Scratch_Lecture9': '[CS50-Scratch Lecture 9](https://www.youtube.com/watch?v=cTAE_e9A65U)',
	'CS50-SQL_Lecture0': '[CS50-SQL Lecture 0](https://www.youtube.com/watch?v=vHYeChEf2lA)',  # CS50 SQL lectures
	'CS50-SQL_Lecture1': '[CS50-SQL Lecture 1](https://www.youtube.com/watch?v=_2t18Hy9Z0Y)',
	'CS50-SQL_Lecture2': '[CS50-SQL Lecture 2](https://www.youtube.com/watch?v=QzRW6bfv3Fo)',
	'CS50-SQL_Lecture3': '[CS50-SQL Lecture 3](https://www.youtube.com/watch?v=BD08USRd2M8)',
	'CS50-SQL_Lecture4': '[CS50-SQL Lecture 4](https://www.youtube.com/watch?v=jZwGVuA8PMI)',
	'CS50-SQL_Lecture5': '[CS50-SQL Lecture 5](https://www.youtube.com/watch?v=qa5-mKVSQHQ)',
	'CS50-SQL_Lecture6': '[CS50-SQL Lecture 6](https://www.youtube.com/watch?v=jXbXGkgT2Xg)',
	'CS50-Web_Lecture0': '[CS50-Web Lecture 0](https://www.youtube.com/watch?v=zFZrkCIc2Oc)',  # CS50 Web lectures
	'CS50-Web_Lecture1': '[CS50-Web Lecture 1](https://www.youtube.com/watch?v=NcoBAfJ6l2Q)',
	'CS50-Web_Lecture2': '[CS50-Web Lecture 2](https://www.youtube.com/watch?v=EOLPQdVj5Ac)',
	'CS50-Web_Lecture3': '[CS50-Web Lecture 3](https://www.youtube.com/watch?v=w8q0C-C1js4)',
	'CS50-Web_Lecture4': '[CS50-Web Lecture 4](https://www.youtube.com/watch?v=YzP164YANAU)',
	'CS50-Web_Lecture5': '[CS50-Web Lecture 5](https://www.youtube.com/watch?v=x5trGVMKTdY)',
	'CS50-Web_Lecture6': '[CS50-Web Lecture 6](https://www.youtube.com/watch?v=jrBhi8wbzPw)',
	'CS50-Web_Lecture7': '[CS50-Web Lecture 7](https://www.youtube.com/watch?v=WbRDkJ4lPdY)',
	'CS50-Web_Lecture8': '[CS50-Web Lecture 8](https://www.youtube.com/watch?v=6PWTxRGh_dk)',
}

if option == "Harvard CS50 Database":
    database_results = st.sidebar.slider(
        "Number of retrieved data: ",
        value = 3,
        min_value=1,
        max_value=20,
        step=1
    )
    max_distance = st.sidebar.slider(
        "Similarity: ",
        value = 1.00,
        min_value=0.01,
        max_value = 5.00,
        step=0.01
    )
    display_sources = st.sidebar.checkbox("Display sources: ")



# ========== Deepseek setup ==========
api_key = st.secrets["API_KEY"] # ERSETZE DIES DURCH DEINEN TATSÄCHLICHEN API-SCHLÜSSEL
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
    if option == "Harvard CS50 Database":

        # Call Datenbank
        results = call_vector_database(prompt, number_data= database_results)
        min_distance = min(results["distances"])        # minimum distance in similarity search

        # Write message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get data from database
        if results != -1 and min_distance <= max_distance:
            # DeepSeek API
            try:
                # Define new prompt with input from vector database
                db_txt_data = '\n\n'.join(results['documents'])
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

                # Display sources in vector database
                if display_sources:
                    sources = ""
                    for element in results['ids']:
                        youtube_link = get_youtube_link(element, havard_sources)
                        # Add youtube video
                        sources += '\n\n' + youtube_link
                    msg = msg + sources

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
