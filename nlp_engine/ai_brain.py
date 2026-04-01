from nlp_engine.memory import get_chat_response
from google import genai
import os
from dotenv import load_dotenv



# Load the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


# Check if the key exists
if not api_key:
    print("❌ CRITICAL ERROR: GEMINI_API_KEY is missing from your .env file!")
else:
    genai.configure(api_key=api_key)


def get_ai_response(user_input):
    try:
        # This calls our main memory logic which has the API key
        response_text = get_chat_response(user_input)
        return response_text
    except Exception as e:
        print(f"--- Brain Error Detail: {e} ---")
        return "Brain connection error. Please check your internet."

# def get_ai_response(user_input):
#     try:
#         # Using a highly stable model name
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         response = get_chat_response(user_input)
#         return response.text
#     except Exception as e:
#         # THIS IS THE KEY: We print 'e' to see why it's failing
#         print(f"--- Brain Error Detail: {e} ---")
#         return "Brain connection error. Check your VS Code Terminal for details."

# import google.generativeai as genai
# import warnings

# warnings.filterwarnings("ignore", category=FutureWarning)

# # Replace with your NEW key
# genai.configure(api_key="AIzaSyBuq4pqAnqg4GEzOqNtbdVYaiScUKe_zgs")

# def get_ai_response(user_input):
#     # 1. Try the Real AI first
#     try:
#         model = genai.GenerativeModel('gemini-1.5-flash-latest')
#         response = model.generate_content(user_input)
#         return response.text
    
#     # 2. If API Key fails, use the "Local Brain" so the demo still looks good
#     except Exception:
#         text = user_input.lower()
#         if "hello" in text or "kaise" in text:
#             return "Namaste! I am your AI assistant. My cloud connection is syncing, but I can hear you loud and clear!"
#         elif "your name" in text or "kaun ho" in text:
#             return "I am the AI Voice Intelligence system created for this project."
#         elif "time" in text:
#             from datetime import datetime
#             return f"The time is {datetime.now().strftime('%H:%M')}."
#         else:
#             return f"I heard you say: {user_input}."