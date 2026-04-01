🤖 JARVIS AI System (2026 Edition)
A high-performance, voice-activated desktop assistant built with Python, PyQt6, and the Gemini 3.1 Flash Lite engine. Jarvis is designed to be a "System-First" assistant, prioritizing hardware control and web automation over long AI conversations.

🌟 Key Features
Wake Word Detection: Responds to "Sun Yaar" (or your custom wake word).

Hardware Control: Voice-controlled System Volume and Screen Brightness using PowerShell and WMI.

Universal App Opener: Launches both Desktop (.exe) and Windows System Apps (Camera, Settings, Calculator).

YouTube Automation: Instant "Lucky" playback using pywhatkit.

Web Automation: Quick access to WhatsApp Web and Google Chrome searches.

Lecture Guard: AI responses are strictly limited to 1-2 sentences with no markdown symbols (*, #).

Smart Standby: Two-stage timeout (10s nudge, 20s sleep) to save resources.

🛠️ Installation
1. Prerequisites
Ensure you have Python 3.10+ installed on Windows 11.

2. Install Required Libraries
Open your terminal and run:

Bash
pip install PyQt6 google-genai pycaw screen-brightness-control comtypes pywhatkit pyautogui edge-tts pygame duckduckgo_search
3. API Setup
Obtain a Gemini API Key from the Google AI Studio.

Open nlp_engine/memory.py.

Replace the GEMINI_API_KEY value with your personal key.

📂 Project Structure
Plaintext
📦 Intelligent-System-Assistant
 ┣ 📂 logs                # System and AI interaction logs
 ┣ 📂 nlp_engine          # Gemini AI & Web Search logic
 ┣ 📂 speech_to_text      # Online/Offline STT engines
 ┣ 📂 system_control      # Hardware & App automation (sys_ctrl.py)
 ┣ 📂 text_to_speech      # Edge-TTS voice engine
 ┣ 📂 ui                  # PyQt6 Graphical User Interface
 ┣ 📂 wake_word           # Porcupine/Custom wake word detector
 ┗ 📜 main.py             # Main execution script
🚀 Usage
Launch: Run python main.py (Run as Administrator for Volume/Brightness control).

Wake: Say "Sun Yaar".

Command Examples:

"Open Camera"

"Set volume to 70 percent"

"Play One Love on YouTube"

"Open WhatsApp"

"Brightness Max"

Exit: Say "Shut down" or "Close yourself".

⚠️ Important Notes
Administrator Mode: Windows 11 blocks hardware changes unless the terminal/IDE is running with Admin privileges.

Focus: Media commands (Pause, Tabs) require the target window (Chrome/Edge) to be the active window.

No Lectures: If Jarvis starts giving long answers, check the system_instruction in nlp_engine/memory.py.
