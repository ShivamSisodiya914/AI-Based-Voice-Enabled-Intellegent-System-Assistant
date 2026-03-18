import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    
    # --- VOICE SELECTION LOGIC ---
    voices = engine.getProperty('voices')
    
    # Try to find a Hindi voice (usually contains 'Hindi' or 'India')
    hindi_voice_found = False
    for voice in voices:
        if "hindi" in voice.name.lower() or "india" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            hindi_voice_found = True
            break
            
    # If no Hindi voice, at least use a female voice (often clearer than the default)
    if not hindi_voice_found:
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    # --- VOICE TUNING ---
    engine.setProperty('rate', 160)    # Slows it down slightly for better clarity
    engine.setProperty('volume', 1.0) # Maximum volume
    
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()