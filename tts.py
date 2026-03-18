import requests
import subprocess

API_KEY = "2516ad38346e41ff6cc0963dd06edb00f71185690e5736882e7a95c091f9a2ba"
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

def speak(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    response = requests.post(url, json=data, headers=headers)

    with open("voice.mp3", "wb") as f:
        f.write(response.content)

    subprocess.run("start voice.mp3", shell=True)