import streamlit as st
from utils import write_message
from agent import gen_res
from streamlit_extras.stylable_container import stylable_container
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
from tempfile import NamedTemporaryFile
import speech_recognition as sr
import os

audio_query = []

def gen_audio(text):
    myobj = gTTS(text=text, lang='en', slow=False)
    myobj.save("speech.mp3")
    with st.sidebar:
        st.audio(data="./speech.mp3",autoplay=True)
    os.remove("./speech.mp3")

def inference(audio):
    # Save audio to a file:
    with NamedTemporaryFile(suffix=".mp3") as temp:
        text = ""
        with open(".\\audio.mp3", "wb") as f:
            f.write(audio)
        r = sr.Recognizer()
        with sr.AudioFile(".\\audio.mp3") as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            try:
                text = r.recognize_google(audio_data)
            except:
                text= "***ERROR***"
        os.remove(".\\audio.mp3")
        return text

# tag::setup[]
# Page Config
st.set_page_config("Movie chat bot", page_icon=":movie_camera:")
# end::setup[]

with st.sidebar:
    audio = audio_recorder("Click for an ask:", "Recording...")
    if audio is not None:
        audio_query.append(audio)

# tag::session[]
# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm an expert movie Chatbot!  How can I help you?"},
    ]
    gen_audio("Hi, I'm an expert movie Chatbot!  How can I help you?")

# end::session[]

# tag::submit[]
# Submit handler
def handle_submit(message):
    # Handle the response
    with st.spinner('Thinking...'):

        response = gen_res(message)
        gen_audio(response)
        write_message('assistant', response)
        
# end::submit[]

# tag::chat[]
# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle any user input
if prompt := st.chat_input("What is up?") or audio is not None:
    if prompt is True and len(audio_query) > 0:
        prompt = inference(audio_query[0])
    # Display user message in chat message container
    if prompt != "***ERROR***":
        write_message('user', prompt)
        # Generate a response
        handle_submit(prompt)
    else:
        write_message('assistant',"Try speaking again, I didn't understand")
        gen_audio("Try speaking again, I didn't understand")
# end::chat[]