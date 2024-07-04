import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from textblob import TextBlob
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def chat_response(question):
    response = chat.send_message(question, stream=True)
    return response

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment

def extract_entities(text):
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    chunks = ne_chunk(pos_tags)
    entities = []
    for chunk in chunks:
        if hasattr(chunk, 'label'):
            entity = ' '.join(c[0] for c in chunk)
            entities.append((entity, chunk.label()))
    return entities

st.set_page_config(page_title="Gemini Chatbot")

st.header("Gemini Chatbot")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input:", key="input")
submit = st.button("Get results")

if submit:
    response = chat_response(input_text)
    st.session_state['chat_history'].append(('you', input_text))
    st.subheader("The response is:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(('bot', chunk.text))

    st.subheader("NLP Analysis")
    
    sentiment = analyze_sentiment(input_text)
    st.write("Sentiment Analysis:")
    st.write(f"Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}")

    entities = extract_entities(input_text)
    st.write("Named Entities:")
    st.write(entities)

st.subheader("Previous chat:")
for person, message in st.session_state['chat_history']:
    st.write(f"{person}: {message}")
