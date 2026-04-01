# =============================================
# new code

# import edge_tts
# import asyncio
# import pygame
# import os
# import re

# # Initialize Pygame mixer for instant audio playback
# pygame.mixer.init()

# def is_hindi(text):
#     # Quick check for Devanagari characters (Hindi script)
#     return bool(re.search(r'[\u0900-\u097F]', text))

# async def _generate_and_play(text):
#     # 1. Choose Voice: 'Madhur' for Hindi, 'Christopher' for Professional English
#     voice = "hi-IN-MadhurNeural" if is_hindi(text) else "en-GB-ThomasNeural"
    
#     # 2. Set the speed (Jarvis should be fast)
#     communicate = edge_tts.Communicate(text, voice, rate="+20%")
    
#     # 3. Save to a temporary file
#     temp_file = "speech.mp3"
#     await communicate.save(temp_file)
    
#     # 4. Play instantly
#     pygame.mixer.music.load(temp_file)
#     pygame.mixer.music.play()
    
#     # Wait for audio to finish
#     while pygame.mixer.music.get_busy():
#         await asyncio.sleep(0.1)
    
#     pygame.mixer.music.unload()
#     if os.path.exists(temp_file):
#         os.remove(temp_file)


# def speak(text):
#     """The main function called by main.py"""
#     if not text:
#         return
#     print(f"JARVIS: {text}")
#     # Run the async function inside a standard function
#     asyncio.run(_generate_and_play(text))

# ==============================================
import edge_tts
import asyncio
import pygame
import os
import re

# Initialize Pygame mixer for instant audio playback
pygame.mixer.init()

def is_hindi(text):
    # Quick check for Devanagari characters (Hindi script)
    return bool(re.search(r'[\u0900-\u097F]', text))

def clean_text_for_speech(text):
    """Removes annoying characters and keeps speech concise."""
    # 1. Remove all markdown symbols (*, #, _, ~, - at start of lines)
    text = re.sub(r'[*#_~]', '', text)
    text = re.sub(r'^\s*-\s*', '', text, flags=re.MULTILINE)
    
    # 2. Limit speech to the first two sentences to prevent 'lectures'
    sentences = re.split(r'(?<=[.!?]) +', text)
    if len(sentences) > 2:
        text = " ".join(sentences[:2])
    
    # 3. Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def _generate_and_play(text):
    # Clean the text BEFORE it reaches the voice engine
    speech_text = clean_text_for_speech(text)
    
    if not speech_text:
        return

    # Choose Voice: 'Madhur' for Hindi, 'Thomas' for British English
    voice = "hi-IN-MadhurNeural" if is_hindi(speech_text) else "en-GB-ThomasNeural"
    
    # Set the speed (Jarvis should be crisp)
    communicate = edge_tts.Communicate(speech_text, voice, rate="+20%")
    
    temp_file = "speech.mp3"
    await communicate.save(temp_file)
    
    # Play instantly
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)
    
    pygame.mixer.music.unload()
    if os.path.exists(temp_file):
        try:
            os.remove(temp_file)
        except:
            pass # File might be locked by system

def speak(text):
    """The main function called by main.py"""
    if not text:
        return
        
    # We print the original text for the UI console, 
    # but the 'clean' version is what gets spoken.
    print(f"JARVIS: {text}")
    
    try:
        asyncio.run(_generate_and_play(text))
    except Exception as e:
        print(f"TTS Error: {e}")