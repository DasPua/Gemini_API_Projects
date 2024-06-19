from dotenv import load_dotenv

load_dotenv() ##loading all the environment variables

import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro-vision")

def gemini_response(question,image):
    if question!="":
        response=model.generate_content([question,image])
    else :
        response=model.generate_content(image)
    return response.text



st.set_page_config(page_title="first gemini vision project")

st.header(body="Gemini Vision Application")

input=st.text_input("Input: ",key="input")

submit=st.button("Get results")



# File uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image=""
# Check if an image has been uploaded
if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)    
    # Display the uploaded image
    st.image(image, caption='Uploaded Image.', use_column_width=True)

if submit:
    response=gemini_response(input,image)
    st.subheader("The response is:")
    st.write(response)



