from speech_to_text.stt_engine import listen_and_convert
from nlp_engine.ai_brain import get_ai_response
from text_to_speech.tts_engine import speak

def start_assistant():
    speak("Jarvis is Online. How can I assist you today?")
    
    while True:
        # 1. Voice Input -> Speech to Text
        user_input = listen_and_convert()
        
        if not user_input or user_input == "":
            continue
            
        print(f"User: {user_input}")

        # 2. Stop Logic
        # Logic to stop the assistant
        if "exit" in user_input.lower() or "bye" in user_input.lower() or "अलविदा" in user_input:
            speak("Goodbye! Closing the system.")
            import os
            os._exit(0) # This kills the process instantly to avoid the pyttsx3 errors

        # 3. Send to API (AI Brain)
        response = get_ai_response(user_input)

        # 4. Get Response -> Text to Speech
        speak(response)

if __name__ == "__main__":
    start_assistant()