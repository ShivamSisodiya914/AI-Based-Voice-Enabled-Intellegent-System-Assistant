# from google import genai
# import time

# # Direct Key as requested
# GEMINI_API_KEY = "AIzaSyBLwLBpPeZUlzrCAyS29spk9JH2f9ai5pY"
# client = genai.Client(api_key=GEMINI_API_KEY)
# MODEL_ID = "gemini-2.0-flash" # Switching to 2.0-flash for faster response time

# def get_chat_response(user_input):
#     # This 'System Instruction' makes the AI actually feel like Jarvis
#     system_prompt = (
#         "You are JARVIS, a sophisticated AI assistant. "
#         "Your responses must be concise, professional, and slightly witty. "
#         "Address the user as 'Sir' or by their name if known. "
#         "Do not use bold text or markdown. Just plain text."
#     )
    
#     for attempt in range(2):
#         try:
#             response = client.models.generate_content(
#                 model=MODEL_ID,
#                 contents=f"{system_prompt}\n\nUser: {user_input}"
#             )
#             return response.text
#         except Exception as e:
#             if "429" in str(e):
#                 time.sleep(1)
#                 continue
#             return "Systems are slightly unstable, Sir. Please try again."
#     return "I am unable to process that at the moment."


# ====================================================================================
# working code

# from google import genai
# import time

# # HARDCODED API KEY (As you requested)
# GEMINI_API_KEY = "AIzaSyBLwLBpPeZUlzrCAyS29spk9JH2f9ai5pY"

# # Initialize the 2026 Client
# client = genai.Client(api_key=GEMINI_API_KEY)

# # Use the latest 2026 Flash Lite model (Fast & Free)
# MODEL_ID = "gemini-3.1-flash-lite-preview"



# def get_chat_response(user_input):
#     for attempt in range(3):
#         try:
#             response = client.models.generate_content(
#                 model=MODEL_ID,
#                 contents=user_input
#             )
#             return response.text
#         except Exception as e:
#             # Handle rate limiting (429) automatically
#             if "429" in str(e):
#                 print(f"🔄 API Busy... retrying in 2s (Attempt {attempt+1}/3)")
#                 time.sleep(2)
#                 continue
#             # If it's a different error, return it
#             print(f"Detailed Error: {e}")
#             return f"I'm having a brain freeze. Error detail: {str(e)}"
    
#     return "I'm a bit overwhelmed right now. Please try again in a few seconds."


# ==================================================
from google import genai
import time

# HARDCODED API KEY
GEMINI_API_KEY = "AIzaSyBLwLBpPeZUlzrCAyS29spk9JH2f9ai5pY"

# Initialize the 2026 Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Use the latest 2026 Flash Lite model
MODEL_ID = "gemini-3.1-flash-lite-preview"

def get_chat_response(user_input):
    # --- THE LECTURE GUARD & CLEAN TEXT RULES ---
    system_instruction = (
        "You are JARVIS, a professional and concise AI assistant. "
        "Rules: 1. NEVER give long explanations or lectures. "
        "2. Responses MUST be under 2 sentences. "
        "3. NEVER use markdown symbols like asterisks (*), hashtags (#), or bullet points. "
        "4. Use plain text only. 5. Be polite but brief."
    )

    for attempt in range(3):
        try:
            # We combine the instruction with the user input
            full_prompt = f"{system_instruction}\n\nUser: {user_input}"
            
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=full_prompt
            )
            
            # Clean up any unexpected whitespace or newlines
            clean_res = response.text.replace("*", "").replace("#", "").strip()
            return clean_res

        except Exception as e:
            if "429" in str(e):
                print(f"🔄 API Busy... retrying in 2s (Attempt {attempt+1}/3)")
                time.sleep(2)
                continue
            
            print(f"Detailed Error: {e}")
            return "Systems are slightly unstable, Sir. Please try again."
    
    return "I am unable to process that at the moment, Sir."