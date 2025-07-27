import openai
import whisper
import os
from gtts import gTTS
import tempfile
import streamlit as st
from openai import OpenAI

# SETUP: Enter your OpenAI API Key here
client = OpenAI(api_key="sk-proj-0vvUHkF6r0K0PKu8rPWPZr-QGx1Gl9KRYblxxZ-U2D7aPs1lwT1ihFmF13Jzt-R3T8LbkFJ8VSNSCav0NtZ96ShOQHlUyG6zaITgpatM9rJsvCZPj1OPfaEfVXC0b5uNey8n8LoA")

# Load Whisper model
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

# Speak text aloud (only works on desktop with speakers)
def speak(text):
    tts = gTTS(text)
    filename = "response.mp3"
    tts.save(filename)
    st.audio(filename)

# Transcribe uploaded audio
def transcribe(file):
    result = model.transcribe(file)
    return result['text']

# Ask GPT for answers
def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful school teacher."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Generate quiz from topic
def generate_quiz(topic):
    prompt = f"Create 3 easy MCQs with 4 options and correct answers from class 6 science topic: {topic}"
    return ask_gpt(prompt)

# Streamlit UI
st.title("🎓 YASHWANTH Mentor")
st.markdown("Upload your voice (WAV/MP3) and ask a doubt or request a quiz.")

uploaded_file = st.file_uploader("🎤 Upload your voice (WAV/MP3)", type=["wav", "mp3"])
if uploaded_file is not None:
    question = transcribe(uploaded_file)
    st.success(f"Student asked: **{question}**")

    if "test me" in question.lower():
        topic = question.lower().replace("test me on", "").strip()
        quiz = generate_quiz(topic)
        st.subheader(f"📝 Quiz on: {topic.capitalize()}")
        st.text(quiz)
        speak("Here is your test.")
        speak(quiz)
    else:
        reply = ask_gpt("Explain like a school teacher: " + question)
        st.subheader("🧑‍🏫 Mentor says:")
        st.markdown(reply)
        speak(reply)
