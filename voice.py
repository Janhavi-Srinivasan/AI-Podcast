import os
import requests
import re
from dotenv import load_dotenv
import streamlit as st  
load_dotenv()
def clean_script(text):
    text = re.sub(r'\*+', '', text)                  
    text = re.sub(r'\(.*?\)', '', text)                
    text = re.sub(r'^\s*\w+:\s*', '', text, flags=re.MULTILINE)  
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if re.search(r"(subscribe|review|follow us|rate us|like|comment|see you next time|stay tuned)", line, re.IGNORECASE):
            continue  
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)
def generate_voice(script_text, voice_id):
    API_KEY = os.getenv("ELEVENLABS_API_KEY")
    script_text = clean_script(script_text)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": script_text,
        "model_id": "eleven_monolingual_v1"
    }
    st.write("📄 Cleaned Script:", script_text[:300] + "..." if len(script_text) > 300 else script_text)
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            os.makedirs("output", exist_ok=True)
            path = "output/podcast.mp3"
            with open(path, "wb") as f:
                f.write(response.content)
            st.success("✅ Voice generation successful!")
            return path
        else:
            st.error("❌ ElevenLabs error:")
            st.code(response.text, language="json")
            return None
    except Exception as e:
        st.error(f"❌ Exception during voice generation: {str(e)}")
        return None
def fetch_available_voices():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    headers = {"xi-api-key": api_key}
    url = "https://api.elevenlabs.io/v1/voices"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            voices = response.json().get("voices", [])
            return {
                voice["name"]: (voice["voice_id"], voice["preview_url"])
                for voice in voices if "preview_url" in voice
            }
    except Exception as e:
        print("Error fetching voices:", e)
    return {}
