# import sys
# import os
# import logging
# from wake_word.detector import wait_for_wake_word
# from speech_to_text.stt_online import recognize_speech
# from text_to_speech.tts_engine import speak
# from system_control.sys_ctrl import execute_command
# from ui.settings_ui import run_gui 
# from nlp_engine.memory import get_chat_response

# # Setup Logs
# if not os.path.exists('logs'): os.makedirs('logs')
# logging.basicConfig(
#     filename='logs/jarvis.log', 
#     level=logging.INFO, 
#     format='%(asctime)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

# def assistant_logic(ui_signal):
#     ui_signal.emit(">>> Jarvis System Online.")
#     logging.info("Jarvis System Online.")
    
#     while True:
#         # --- PHASE 1: WAITING FOR WAKE WORD ---
#         if wait_for_wake_word():
#             ui_signal.emit(">>> Jarvis Awakened!")
#             logging.info("Wake word detected.")
#             speak("Hello Sir, I am online. How can I help you today?")
            
#             silence_count = 0  # Counter for Stage 1 and Stage 2 timeouts
            
#             # --- PHASE 2: CONTINUOUS CONVERSATION ---
#             while True:
#                 ui_signal.emit(">>> Listening...")
#                 user_input = recognize_speech() 
                
#                 if not user_input:
#                     silence_count += 1
                    
#                     if silence_count == 1:
#                         # Stage 1: 10 Seconds of silence
#                         ui_signal.emit(">>> Waiting (10s)...")
#                         speak("I am still here, Sir. Do you need anything else?")
#                         continue 
                        
#                     elif silence_count >= 2:
#                         # Stage 2: 20 Seconds of silence
#                         ui_signal.emit(">>> Standby Mode (20s).")
#                         speak("I'll be here if you need me. Just call my name.")
#                         logging.info("Auto-standby triggered due to silence.")
#                         break # Back to Phase 1
                
#                 # Reset silence counter if user speaks
#                 silence_count = 0
#                 input_lower = user_input.lower().strip()
#                 logging.info(f"User Input: {input_lower}")

#                 # 1. SHUTDOWN COMMAND
#                 if "close yourself" in input_lower or "shut down" in input_lower:
#                     speak("Shutting down all systems. Goodbye, Sir.")
#                     ui_signal.emit("CLOSE_WINDOW") 
#                     return 

#                 # 2. SLEEP COMMAND
#                 if "go to sleep" in input_lower or "bas yaar" in input_lower:
#                     speak("Understood, Sir. Call me if you need me.")
#                     ui_signal.emit(">>> Jarvis is Sleeping...")
#                     break 

#                 # 3. SYSTEM COMMANDS (Open/Close Apps)
#                 sys_res = execute_command(input_lower)
#                 if sys_res:
#                     ui_signal.emit(f"Action: {sys_res}")
#                     speak(sys_res)
#                     continue 

#                 # 4. AI BRAIN
#                 ui_signal.emit(">>> Thinking...")
#                 response = get_chat_response(user_input)
                
#                 if "As an AI" in response and "open" in input_lower:
#                      ui_signal.emit("AI Error: Specific app not found.")
#                      speak("I'm sorry Sir, I couldn't find that specific application.")
#                 else:
#                     ui_signal.emit(f"AI: {response}")
#                     speak(response)

# if __name__ == "__main__":
#     run_gui(assistant_logic)
# ========================================================
import sys
import os
import logging
import webbrowser
from wake_word.detector import wait_for_wake_word
from speech_to_text.stt_online import recognize_speech
from text_to_speech.tts_engine import speak
from system_control.sys_ctrl import execute_command
from ui.settings_ui import run_gui 
from nlp_engine.memory import get_chat_response

# --- 1. SETUP LOGGING ---
if not os.path.exists('logs'): 
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/jarvis.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

def assistant_logic(ui_signal):
    """
    Core logic for the Assistant. 
    Handles Phase 1 (Waiting for Wake Word) and Phase 2 (Continuous Conversation).
    """
    ui_signal.emit(">>> Jarvis System Online.")
    logging.info("System Started.")
    
    while True:
        # --- PHASE 1: WAITING FOR WAKE WORD ---
        if wait_for_wake_word():
            ui_signal.emit(">>> Jarvis Awakened!")
            logging.info("Wake Word Detected.")
            speak("Hello Sir, I am online. How can I help you today?")
            
            silence_count = 0 
            
            # --- PHASE 2: CONTINUOUS CONVERSATION ---
            while True:
                ui_signal.emit(">>> Listening...")
                user_input = recognize_speech() 
                
                # Handle Silence / Timeouts
                if not user_input:
                    silence_count += 1
                    if silence_count == 1:
                        # Stage 1: 10 Seconds of silence
                        ui_signal.emit(">>> Waiting (10s)...")
                        speak("I am still here, Sir. Do you need anything else?")
                        continue 
                    elif silence_count >= 2:
                        # Stage 2: 20 Seconds of silence
                        ui_signal.emit(">>> Standby Mode (20s).")
                        speak("I'll be here if you need me. Just call my name.")
                        logging.info("Auto-standby triggered due to silence.")
                        break # Go back to Phase 1 (Waiting for Wake Word)
                
                # Reset silence counter if user speaks
                silence_count = 0
                input_lower = user_input.lower().strip()
                logging.info(f"User Input: {input_lower}")

                # --- 1. SYSTEM SHUTDOWN (Highest Priority) ---
                if "close yourself" in input_lower or "shut down" in input_lower:
                    speak("Shutting down all systems. Goodbye, Sir.")
                    logging.info("Manual Shutdown.")
                    ui_signal.emit("CLOSE_WINDOW") 
                    return 

                # --- 2. SLEEP COMMAND (Manual Standby) ---
                if "go to sleep" in input_lower or "bas yaar" in input_lower:
                    speak("Understood, Sir. Call me if you need me.")
                    ui_signal.emit(">>> Jarvis is Sleeping...")
                    break 

                # --- 3. SYSTEM COMMANDS (Hardware, Apps, Media) ---
                # This check happens BEFORE the AI Brain to prevent "Lectures"
                sys_res = execute_command(input_lower)
                
                # Handle App Not Found Fallback
                if sys_res == "APP_NOT_FOUND":
                    app_name = input_lower.replace("open", "").strip()
                    speak(f"I couldn't find {app_name} on your system, Sir. Shall I open it in Google Chrome instead?")
                    
                    ui_signal.emit(">>> Waiting for Permission...")
                    permission = recognize_speech()
                    if permission and any(word in permission.lower() for word in ["yes", "ok", "haan", "sure"]):
                        webbrowser.open(f"https://www.google.com/search?q={app_name}")
                        speak(f"Opening {app_name} in your browser, Sir.")
                    else:
                        speak("Understood. I will not open the browser.")
                    continue

                # If a standard system command was executed (Volume, YouTube, etc.)
                if sys_res:
                    ui_signal.emit(f"Action: {sys_res}")
                    logging.info(f"Action Executed: {sys_res}")
                    speak(sys_res)
                    # This 'continue' skips the AI stage entirely
                    continue 

                # --- 4. AI BRAIN (General Conversation) ---
                # Only runs if no system command matched above
                ui_signal.emit(">>> Thinking...")
                response = get_chat_response(user_input)
                
                # Double-check: If AI accidentally mentions an 'open' link it can't execute
                if "As an AI" in response and "open" in input_lower:
                     ui_signal.emit("AI Error: Specific app not found.")
                     speak("I'm sorry Sir, I couldn't find that specific application.")
                else:
                    ui_signal.emit(f"AI: {response}")
                    logging.info("AI Response Sent.")
                    speak(response)

# --- START THE APPLICATION ---
if __name__ == "__main__":
    # This launches the PyQt6 GUI and passes the assistant_logic to the background thread
    run_gui(assistant_logic)
