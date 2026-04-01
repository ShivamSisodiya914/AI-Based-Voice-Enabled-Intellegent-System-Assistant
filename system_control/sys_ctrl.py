# import os
# import subprocess
# import difflib # Used to find the "closest" matching app name

# def execute_command(command):
#     cmd = command.lower().strip()
    
#     # List of common directories where Windows keeps .exe shortcuts
#     search_paths = [
#         r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
#         r"C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs".format(os.getlogin()),
#         r"C:\Windows\System32"
#     ]

#     # --- 1. OPENING LOGIC ---
#     if "open" in cmd:
#         app_query = cmd.replace("open", "").replace("the", "").replace("application", "").strip()
        
#         # Immediate common nicknames
#         nicknames = {"word": "winword", "powerpoint": "powerpnt", "excel": "excel", "chrome": "chrome"}
#         target = nicknames.get(app_query, app_query)

#         try:
#             # Try direct launch first
#             os.startfile(f"{target}.exe")
#             return f"Opening {app_query} now, Sir."
#         except:
#             # --- SMART SUGGESTION LOGIC ---
#             found_apps = []
#             # Scan Start Menu for actual installed app names
#             for path in search_paths:
#                 if os.path.exists(path):
#                     for root, dirs, files in os.walk(path):
#                         for file in files:
#                             if file.endswith(".lnk") or file.endswith(".exe"):
#                                 found_apps.append(file.replace(".lnk", "").replace(".exe", "").lower())

#             # Find the top 3 closest matches to what the user said
#             matches = difflib.get_close_matches(app_query, found_apps, n=3, cutoff=0.4)

#             if matches:
#                 suggestions = ", ".join(matches)
#                 return f"I couldn't find {app_query} directly. Did you mean {suggestions}? Please say the exact name to open it."
#             else:
#                 return f"I am sorry Sir, I cannot find any application named {app_query} on this PC."

#     # --- 2. CLOSING LOGIC ---
#     if "close" in cmd:
#         app_to_close = cmd.replace("close", "").replace("the", "").strip()
#         # Basic mapping
#         close_map = {"word": "winword.exe", "chrome": "chrome.exe"}
#         process = close_map.get(app_to_close, app_to_close + ".exe")

#         result = os.system(f"taskkill /f /im {process} /t")
#         if result == 0:
#             return f"Closed {app_to_close} successfully, Sir."
#         else:
#             return f"I could not find an active window for {app_to_close}."

#     return None
# =========================================================
import os
import subprocess
import webbrowser
import pywhatkit
import pyautogui
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def set_system_volume(level):
    """Sets system volume using Pycaw with a PowerShell fallback for Windows 11."""
    try:
        # Method 1: Pycaw
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return True
    except:
        try:
            # Method 2: Force via PowerShell (Bypasses security blocks)
            val = level / 100
            powershell_cmd = f"$obj = New-Object -ComObject MMDeviceEnumerator; $dev = $obj.GetDefaultAudioEndpoint(0, 0); $dev.AudioEndpointVolume.MasterVolumeLevelScalar = {val}"
            subprocess.run(["powershell", "-Command", powershell_cmd], capture_output=True)
            return True
        except:
            return False

def execute_command(command):
    cmd = command.lower().strip()
    
    # --- 1. HARDWARE: VOLUME ---
    if "volume" in cmd or "sound" in cmd:
        level = None
        if "full" in cmd or "max" in cmd or "100" in cmd: level = 100
        elif "high" in cmd: level = 80
        elif "mid" in cmd or "half" in cmd or "50" in cmd: level = 50
        elif "low" in cmd: level = 20
        elif "mute" in cmd or "0" in cmd: level = 0
        
        nums = [int(s) for s in cmd.split() if s.isdigit()]
        if nums: level = min(max(nums[0], 0), 100)

        if level is not None:
            set_system_volume(level)
            return f"System volume set to {level} percent, Sir."

    # --- 2. HARDWARE: BRIGHTNESS ---
    if "brightness" in cmd or "light" in cmd:
        level = None
        if "full" in cmd or "max" in cmd: level = 100
        elif "high" in cmd: level = 80
        elif "mid" in cmd or "half" in cmd: level = 50
        elif "low" in cmd: level = 20
        
        nums = [int(s) for s in cmd.split() if s.isdigit()]
        if nums: level = min(max(nums[0], 0), 100)

        if level is not None:
            try:
                # Method 1: Library
                sbc.set_brightness(level)
                return f"Brightness adjusted to {level} percent."
            except:
                try:
                    # Method 2: Force via WMI (Windows Management Instrumentation)
                    wmi_cmd = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"
                    subprocess.run(["powershell", "-Command", wmi_cmd], capture_output=True)
                    return f"Brightness forced to {level} percent."
                except:
                    return "I cannot control the brightness on this display, Sir."

    # --- 3. MEDIA: YOUTUBE PLAYBACK ---
    if "play" in cmd:
        song_name = cmd.replace("play", "").replace("on youtube", "").strip()
        if song_name:
            try:
                pywhatkit.playonyt(song_name)
                return f"Playing {song_name} on YouTube, Sir."
            except:
                webbrowser.open(f"https://www.youtube.com/results?search_query={song_name}")
                return f"Searching YouTube for {song_name}."

    # --- 4. MEDIA: CONTROLS (Pause/Tabs/Mute) ---
    if any(word in cmd for word in ["pause", "resume", "stop"]):
        pyautogui.press('k')
        return "Toggled playback."

    if "mute" in cmd and "volume" not in cmd:
        pyautogui.press('m')
        return "Video muted."

    if "new tab" in cmd:
        pyautogui.hotkey('ctrl', 't')
        return "New tab opened."

    if "close tab" in cmd or "close this tab" in cmd:
        pyautogui.hotkey('ctrl', 'w')
        return "Tab closed."

    # --- 5. APPS: OPEN/CLOSE ---
    if "open" in cmd:
        app_query = cmd.replace("open", "").replace("the", "").strip()
        if "whatsapp" in app_query:
            webbrowser.open("https://web.whatsapp.com/")
            return "Opening WhatsApp Web."
        if "youtube" in app_query:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube Home."

        nicknames = {"word": "winword", "chrome": "chrome", "edge": "msedge", "notepad": "notepad"}
        target = nicknames.get(app_query, app_query)
        try:
            os.startfile(f"{target}.exe")
            return f"Opening {app_query}."
        except:
            return "APP_NOT_FOUND"

    if "close" in cmd:
        app = cmd.replace("close", "").replace("the", "").strip()
        close_map = {"word": "winword.exe", "chrome": "chrome.exe", "youtube": "chrome.exe", "whatsapp": "chrome.exe"}
        process = close_map.get(app, app + ".exe")
        os.system(f"taskkill /f /im {process} /t")
        return f"Closed {app} successfully."

    return None