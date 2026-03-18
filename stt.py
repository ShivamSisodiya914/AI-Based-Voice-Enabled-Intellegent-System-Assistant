import speech_recognition as sr


def listen():
    """Listen for a voice command.

    Falls back to typed input when the microphone is not available or PyAudio
    is not installed (common on some Windows/Python versions).
    """

    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as err:
            print("Speech recognition error:", err)
            return ""

    except (AttributeError, OSError) as e:
        # PyAudio is often missing on Windows for newer Python versions
        # (e.g. 3.14) and can be hard to install without build tools.
        print("Microphone unavailable or PyAudio not installed. Falling back to text input.")
        return input("Type your command: ").strip().lower()
