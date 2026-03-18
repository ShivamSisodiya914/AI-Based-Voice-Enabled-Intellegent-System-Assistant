from stt import listen
from tts import speak

speak("Jarvis system online")

while True:
    command = listen()

    if "hello" in command:
        speak("Hello sir, how can I assist you")

    elif "your name" in command:
        speak("I am Jarvis, your AI assistant")

    elif "stop" in command:
        speak("Shutting down")
        break