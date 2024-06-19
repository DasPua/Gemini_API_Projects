from dotenv import load_dotenv

load_dotenv()

import os
import google.generativeai as genai
import streamlit as st 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro")

chat=model.start_chat(history=[])

def chat_response(question):
    response=chat.send_message(question,stream=True)
    return response

st.set_page_config(page_title="first gemini chatbot")

st.header(body="ChatBot")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

input=st.text_input("Input: ",key="input")

submit=st.button("Get results")

if submit:
    response=chat_response(input)
    st.session_state['chat_history'].append(('you',input))
    st.subheader("The response is:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(('bot',chunk.text))
        
st.subheader("Previous chat:")

for person,response in st.session_state['chat_history']:
    st.write(f"{person} : {response}")