import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")
def generate_script(topic):
    prompt = f"Generate a 2-minute podcast script about: {topic}. Make it engaging, informative, and suitable for an audio format."
    response = model.generate_content(prompt)
    script = response.text.strip()
    os.makedirs("output", exist_ok=True)
    with open("output/script.txt", "w") as f:
        f.write(script)
    return script
if __name__ == "__main__":
    topic = input("🎙️ Enter a podcast topic: ")
    script = generate_script(topic)
    print("\n📄 Generated Script:\n")
    print(script)
