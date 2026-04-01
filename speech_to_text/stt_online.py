import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Listening...] Speak now (English/Hindi)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        # Defaults to English, handles Hinglish well
        text = recognizer.recognize_google(audio)
        return text
    except:
        return ""