import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import random
from bots.emotibot import EmotiBot
from config import MONGO_URI, MISTRAL_KEY
from dbs.mongo import MongoConversationStore
from bots.conversation import Conversation
from analyzer.phq9 import PHQ9
from llms.MistralAPI import MistralApi
import json
import pandas as pd

# Function to process chat history
def process_chat(hist):
    return [f"**{entry['actor']}**: {entry['content']}" for entry in hist["general_history"]]

# Cache the EmotiBot instance so it's shared across sessions
@st.cache_resource
def initialize_emotibot():
    return EmotiBot()

# Cache database initialization
@st.cache_resource
def initialize_db():
    db = MongoConversationStore(MONGO_URI, "EMOTI", "CONVERSATIONS")
    return db

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='en-US')
            return text
        except sr.UnknownValueError:
            return "I couldn't understand. Please try again."
        except sr.RequestError:
            return "Connection error with the voice service."

# Function to generate chatbot response
def chatbot_response(conversation, user_input):
    response = conversation.get_result(user_input)
    return response

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    filename = f"response_{random.randint(1, 100000)}.mp3"
    tts.save(filename)
    return filename

# PHQ9 analysis functionality
def phq9_analysis(history, bot):
    phq9 = PHQ9(bot)
    res = []
    batch_size = 10
    for start_idx in range(0, len(history), batch_size):
        batch = history[start_idx:start_idx + batch_size]
        batch = list(map(lambda d: json.dumps(d), batch))
        
        result = []
        for i in range(len(batch) // 2):
            user = batch[2 * i]
            docteur = batch[2 * i + 1]
            final_query = f"User Thoughts : {user}"
            result.append(phq9.get_answers(final_query))
        
        # Create a DataFrame to handle the results
        df = pd.DataFrame(result)
        final_result = df.sum()  # Aggregate the results
        res.append(final_result.sum())
    return res

# Cache initialization of bot and database
emotibot = initialize_emotibot()
db = initialize_db()

# Initialize session state for chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Initialize session state for conversation list
if 'init_history' not in st.session_state:
    st.session_state.init_history = [{}] + db.get_all()

# Sidebar setup
st.sidebar.title("Chat History")

# Display a list of chats in the sidebar
chat_list = [f"Chat {i}" for i in range(len(st.session_state.init_history))]
selected_chat = st.sidebar.selectbox("Select a chat", options=chat_list)

# Update the current chat history when a chat is selected
if chat_list:
    selected_index = chat_list.index(selected_chat)
    db = MongoConversationStore(MONGO_URI, "EMOTI", "CONVERSATIONS")
    st.session_state.init_history = [{}] + db.get_all()

    if selected_index == 0:
        st.session_state.history = []  # Clear chat history
        conversation = Conversation(emotibot, db)  # Create a new conversation without history argument
    else:
        selected_history = st.session_state.init_history[selected_index]
        conversation = Conversation(emotibot, db, selected_history["_id"])
        st.session_state.history = process_chat(selected_history)

# Chatbot title and description
st.title("🤖 Emotional ChatBot")
st.write("Communicate with a chatbot that understands and responds with emotions.")

# Text-based interaction
user_input = st.text_input("Type your message here:")
if st.button("Send"):
    if user_input:
        st.session_state.history.append(f"**User Input**: {user_input}")
        response = chatbot_response(conversation, user_input)
        st.session_state.history.append(f"**ChatBot**: {response}")
        audio_file = text_to_speech(response)
        st.audio(audio_file, format="audio/mp3")

# Speech-based interaction
if st.button("Speak now"):
    user_input = recognize_speech()
    st.session_state.history.append(f"**User Input**: {user_input}")
    if user_input and "error" not in user_input.lower():
        response = chatbot_response(conversation, user_input)
        st.session_state.history.append(f"**ChatBot**: {response}")
        audio_file = text_to_speech(response)
        st.audio(audio_file, format="audio/mp3")

# Display chat history
for interaction in st.session_state.history:
    st.write(interaction)

# PHQ9 Analysis
if st.button("Analyze Conversation (PHQ9)"):
    longest_conversation = max(db.get_all(), key=lambda conver: len(conver["general_history"]))
    history = longest_conversation["general_history"]
    bot = MistralApi(api_key=MISTRAL_KEY, model="mistral-large-latest")
    results = phq9_analysis(history, bot)
    st.write("PHQ9 Analysis Results:")
    st.write(results)

# Add styling to buttons and audio player
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
    }
    .stAudio {
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
