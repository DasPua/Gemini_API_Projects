from dotenv import load_dotenv

load_dotenv() ##loading all the environment variables

import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro")

def gemini_response(question):
    response=model.generate_content(question)
    return response.text

st.set_page_config(page_title="first gemini project")

st.header(body="Gemini Application")

input=st.text_input("Input: ",key="input")

submit=st.button("Get results")

if submit:
    response=gemini_response(input)
    st.subheader("The response is:")
    st.write(response)

