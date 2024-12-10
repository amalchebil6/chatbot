import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import random
import openai

# Fonction pour la reconnaissance vocale
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Parlez maintenant...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='fr-FR')
            return text
        except sr.UnknownValueError:
            return "Je n'ai pas compris. Réessayez."
        except sr.RequestError:
            return "Erreur de connexion au service vocal."

# Fonction pour générer la réponse émotionnelle du chatbot
def chatbot_response(user_input):
    return "Hiii"

# Fonction pour lire une réponse avec gTTS
def text_to_speech(text):
    tts = gTTS(text=text, lang="fr")
    filename = f"response_{random.randint(1, 100000)}.mp3"
    tts.save(filename)
    return filename

# Interface principale avec Streamlit
st.set_page_config(page_title="ChatBot Émotionnel", layout="wide", initial_sidebar_state="expanded")

# Initializing session state for history if not already present
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar setup
st.sidebar.title("Historique Chat")
st.sidebar.button("New Chat", on_click=lambda: st.session_state.history.clear())

# Chatbot title and description
st.title("🤖 ChatBot Émotionnel")
st.write("Communiquez avec un chatbot qui comprend et répond avec des émotions.")

# Zone d'interaction avec le chatbot (Text Input)
user_input = st.text_input("Tapez votre message ici :")
if st.button("Envoyer"):
    if user_input:
        # Save user input and response to history (append to end)
        st.session_state.history.append(f"**User Input**: {user_input}")
        response = chatbot_response(user_input)
        st.session_state.history.append(f"**ChatBot**: {response}")
        audio_file = text_to_speech(response)
        st.audio(audio_file, format="audio/mp3")

# Zone d'interaction avec le chatbot (Speech Recognition)
if st.button("Parlez maintenant"):
    user_input = recognize_speech()
    st.session_state.history.append(f"**User Input**: {user_input}")
    if user_input and "Erreur" not in user_input:
        response = chatbot_response(user_input)
        st.session_state.history.append(f"**ChatBot**: {response}")
        audio_file = text_to_speech(response)
        st.audio(audio_file, format="audio/mp3")

# Display chat history in order (oldest at top, newest at bottom)
for interaction in st.session_state.history:
    st.write(interaction)

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
