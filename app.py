import streamlit as st
import os
from dotenv import load_dotenv
from generator import generate_script
from generator import generate_topic_suggestions
from voice import generate_voice
from voice import fetch_available_voices
import base64
load_dotenv()
with open("background.jpg", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data).decode()
st.set_page_config(page_title="🎧 AI Podcast Generator", layout="wide")
st.markdown(f"""
<style>
body, .stApp {{
    font-family: Arial, sans-serif;
    color: #FFFFFF;
}}
.stApp {{
    background-image: url("data:image/jpg;base64,{encoded}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
main {{
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 3rem;
    max-width: 800px;
    margin: auto;
}}
h1, h2, h3, p, label {{
    color: #FFFFFF;
}}
.stButton>button {{
    background-color: #4CAF50;
    color: #fff;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.8rem 2rem;
    font-size: 1rem;
}}
.stDownloadButton>button {{
    background-color: #2196F3;
    color: #fff;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.8rem 2rem;
}}
.stTextInput>label, .stTextArea>label {{
    font-weight: 600;
    font-size: 1rem;
    color: #FFFFFF;
}}
</style>
""", unsafe_allow_html=True)
st.markdown("## 🎙️ AI Podcast Generator")
st.markdown("""
Create an engaging podcast script with voice output .
""")
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if st.button("🎯 Generate Topic Suggestions"):
    with st.spinner("🤖 Fetching topic ideas..."):
        st.session_state.suggestions = generate_topic_suggestions("general knowledge")
suggestions = st.session_state.suggestions
if suggestions:
    if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = suggestions[0]
    selected = st.selectbox("💡 Choose a topic", suggestions, key="selected_topic")
    topic = st.text_input("✏️ Confirm or edit topic:", value=selected)
else:
    topic = st.text_input("🔍 Enter your podcast topic:")
duration = st.selectbox(
    "⏱️ Select Podcast Duration",
    options=["1 minute", "2 minutes", "3 minutes", "4 minutes", "5 minutes"],
    index=1
)
duration = int(duration.split()[0])
voices = fetch_available_voices()
if voices:
    voice_names = list(voices.keys())
    selected_voice = st.selectbox("🎙️ Choose a Voice", voice_names, key="voice_selector")
    voice_id, preview_url = voices[selected_voice]
    st.markdown("🔊 **Preview Selected Voice:**")
    st.audio(preview_url, format="audio/mpeg")
else:
    st.warning("⚠️ No voices found. Check your ElevenLabs API key.")
    voice_id = None  
if st.button("✨ Generate Podcast"):
    if topic.strip() == "":
        st.warning("⚠️ Please enter a valid topic.")
    else:
        with st.spinner("🧠 Generating script..."):
            script = generate_script(topic, duration)
        st.success("✅ Script generated successfully!")
        st.markdown("### 📄 Your Podcast Script")
        st.text_area("Script Preview", script, height=300)
        st.markdown(f"🎤 Generating voice using: `{selected_voice}`")
        with st.spinner("🎤 Generating voice..."):
            audio_path = generate_voice(script, voice_id)
        if audio_path and os.path.exists(audio_path):
            st.success("✅ Voice generation complete!")
            st.markdown("### 🔊 Listen to Your Podcast")
            st.audio(audio_path, format="audio/mp3")
            with open(audio_path, "rb") as audio_file:
                st.download_button("📥 Download ", data=audio_file, file_name="podcast.mp3")
        else:
            st.error("❌ Voice generation failed. Check your API key, voice ID, or quota.")
