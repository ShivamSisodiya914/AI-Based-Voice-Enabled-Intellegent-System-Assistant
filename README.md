# AI-Based-Voice-Enabled-Intelligent-System-Assistant

AI-based Voice Enabled Intelligent System Assistant is a smart application that understands voice commands using speech recognition and NLP. It performs tasks like answering queries, opening apps, and automating basic system operations to improve user productivity.

---

## 🚀 Key Features
- **Bilingual Support:** Understands and processes commands in both **Hindi and English** (Hinglish).
- **AI Brain:** Powered by **Google Gemini 1.5 Flash** for intelligent, generative responses.
- **Smart Listening:** Includes ambient noise adjustment to work in noisy environments.
- **Offline TTS:** Fast, local Text-to-Speech synthesis for immediate feedback.
- **Modular Architecture:** Clean separation between Speech, NLP, and Voice modules for easy scaling.

---

## 🏗️ Project Architecture

The system follows a linear pipeline architecture:
1. **Voice Input:** Captures audio via Microphone.
2. **STT (Speech-To-Text):** Converts audio to text using Google Speech Recognition.
3. **NLP (AI Brain):** Processes text through Gemini API to generate a context-aware response.
4. **TTS (Text-To-Speech):** Converts the response back to audio using `pyttsx3`.



---

## 📂 Folder Structure
```text
AI-Voice-Assistant/
├── main.py                  # Main entry point & system controller
├── requirements.txt         # List of dependencies
├── speech_to_text/
│   └── stt_engine.py        # STT logic & Hindi/English detection
├── nlp_engine/
│   └── ai_brain.py          # Gemini API integration & Fallback logic
└── text_to_speech/
    └── tts_engine.py        # TTS configuration & voice selection