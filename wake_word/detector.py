import speech_recognition as sr

def wait_for_wake_word():
    recognizer = sr.Recognizer()
    # List of all your custom triggers
    triggers = [
        "hello jarvis", 
        "hey jarvis", 
        "sun jarvis", 
        "jarvis sun", 
        "jarvis", 
        "sun yaar",
        "hello"
    ]
    
    with sr.Microphone() as source:
        print(f"\n[Sleeping...] Say {triggers[0]} or {triggers[-1]} to wake me up.")
        # Fast adjustment for noise to keep it responsive
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            # Increased phrase_time_limit slightly for longer phrases like "Sun Yaar"
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)
            
            # Using Google Recognition for high accuracy
            text = recognizer.recognize_google(audio).lower().strip()
            print(f">>> Heard: {text}")

            # Check if any of our triggers are in the spoken text
            if any(trigger in text for trigger in triggers):
                print("\n[Wake Word Detected!]")
                return True
            
        except sr.UnknownValueError:
            # Just means it heard noise but no words
            return False
        except sr.RequestError:
            print(">>> Network error in Detector. Check internet.")
            return False
        except Exception:
            return False
            
    return False