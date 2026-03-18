import speech_recognition as sr

def listen_and_convert():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n[Listening...] Speak naturally (Hindi or English)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("[Processing...] Detecting language...")
        # REMOVING language='hi-IN' allows the API to default to its multi-language detection
        # It will now prioritize English script for English words
        text = recognizer.recognize_google(audio) 
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "Error: Check Internet"