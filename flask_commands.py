from database import *
from playsound import playsound
import webbrowser
import pywhatkit
import pyautogui
import keyboard
import datetime
import requests
import pyttsx3
import difflib
import random
import signal
import time
import os
import re

# Music setup
path = "C:\\Users\\Shiko-store\\Music"
library = os.listdir(path) if os.path.exists(path) else []

# Chrome browser registration
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
chrome_path_x86 = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

if os.path.exists(chrome_path):
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    browser_controller = webbrowser.get('chrome')
elif os.path.exists(chrome_path_x86):
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path_x86))
    browser_controller = webbrowser.get('chrome')
else:
    browser_controller = webbrowser

def open_url(url):
    try:
        browser_controller.open(url)
    except Exception:
        webbrowser.open(url)

# Normal Speech Speed Output
def speak(inp):
    print(f"[ALEX RESPONSE]: {inp}")
    try:
        agent = pyttsx3.init()
        agent.setProperty('rate', 185)  # Set speech speed to normal
        agent.say(inp)
        agent.runAndWait()
        agent.stop()
    except Exception as e:
        print(f"Speech notice: {e}")

# Exact Word Matching Helper
class smart_txt(str):
    def __contains__(self, keyword):
        return bool(re.search(rf"\b{re.escape(str(keyword))}\b", str(self)))

# Processing Command Function
def do_command(text):
    text = smart_txt(text.lower().strip())
    
    # --- Conversation & Greetings ---
    if any(keyword in text for keyword in greetings):
        speak("hey, what's up?, how can i help you today?")
    elif any(keyword in text for keyword in chat):
        speak("i'm good as long as you good , how can i help you today?")
    elif any(keyword in text for keyword in thanks):
        speak("you are welcome , i'm here to help any time")
    elif any(keyword in text for keyword in interests):
        speak("that's cool , your interests are special")
    elif any(keyword in text for keyword in questions):
        speak("sorry i'm not able to answer that kind of questions , may i help in something else?")
    elif any(keyword in text for keyword in agent_id):
        speak("my name is alex but you can give me instructions without my name")
    elif any(keyword in text for keyword in check):
        speak("yes i'm still here for you , can i help you with something")
    elif text in ["alex?", "alex"]:
        speak("yes?")
        
    # --- Browser & Navigation ---
    elif any(keyword in text for keyword in browser) and "close" not in text:
        speak("opening browser")
        open_url("https://google.com")
    elif any(keyword in text for keyword in browse):
        matches = difflib.get_close_matches(text, websites, cutoff=0.4, n=1)
        if matches:
            matched_web = matches[0]
            speak(f"visiting {matched_web}")
            open_url(f"https://{matched_web.strip('.')}.com")
    elif any(keyword in text for keyword in yt):
        clean_text = text.replace("on youtube", "").replace("youtube", "").replace("play", "").replace("online", "").strip()
        speak(f"playing {clean_text} online")
        pywhatkit.playonyt(clean_text)
    elif any(keyword in text for keyword in server):
        speak("opening server")
        open_url("http://localhost:8080")
    elif any(keyword in text for keyword in close_tab):
        speak("closing tab")
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
    elif any(keyword in text for keyword in close_browser):
        speak("closing browser")
        os.system("taskkill /f /im chrome.exe")

    # --- Applications & Local Tools ---
    elif any(keyword in text for keyword in explorer):
        speak("opening explorer")
        os.system("start explorer")
    elif any(keyword in text for keyword in notepad):
        speak("opening notepad")
        os.system("start notepad")
    elif any(keyword in text for keyword in terminal):
        speak("opening terminal")
        os.system("start cmd")
    elif any(keyword in text for keyword in code):
        speak("starting code editor")
        os.system("start code")
    elif any(keyword in text for keyword in valorant):
        speak("because valorant security system i need to go , so yes , goodbye")
        os.system("start valorant")
        exit()

    # --- Music Control ---
    elif any(keyword in text for keyword in music) and "stop" not in text and "off" not in text:
        if library:
            song = random.choice(library)
            speak(f"playing {song}")
            os.startfile(os.path.join(path, song))
        else:
            speak("Music directory is empty.")
            
    elif "play" in text and "music" not in text and "youtube" not in text:
        song_name = text.split("play", 1)[1].strip()
        matches = difflib.get_close_matches(song_name, library, n=1, cutoff=0.4)
        if matches:
            matched_file = matches[0]
            speak(f"playing {matched_file}")
            os.startfile(os.path.join(path, matched_file))
        else:
            speak("sorry i couldn't find the song locally, playing on youtube")
            pywhatkit.playonyt(song_name)
            
    elif any(keyword in text for keyword in randomise) and "song" in text:
        if library:
            song = random.choice(library)
            speak(f"playing {song}")
            os.startfile(os.path.join(path, song))

    elif any(keyword in text for keyword in close_music):
        speak("stopping music")
        os.system("taskkill /f /im AIMP.exe")

    # --- Modes & Controls ---
    elif any(keyword in text for keyword in clapy_mode) and "off" not in text:
        speak("starting clapy")
        if os.path.exists("D:\\Hub\\Alex\\Clapy\\clapy.bat"):
            os.startfile("D:\\Hub\\Alex\\Clapy\\clapy.bat")
    elif any(keyword in text for keyword in clapy_mode_off):
        speak("clap mode off")
        keyboard.press("f7")
    elif any(keyword in text for keyword in sleeping_mode):
        speak("sleeping mode activated")
        keyboard.press("f7")
    elif any(keyword in text for keyword in chill_mode):
        speak("chilling mode on")
        keyboard.press("f7")

    # --- Volume Control ---
    elif any(keyword in text for keyword in vol_up):
        speak("volume up")
        for _ in range(5):
            keyboard.send("volume up")
    elif any(keyword in text for keyword in vol_down):
        speak("volume down")
        for _ in range(5):
            keyboard.send("volume down")
    elif any(keyword in text for keyword in mute):
        speak("mute")
        keyboard.send("volume mute")

    # --- System Controls ---
    elif any(keyword in text for keyword in time_ask):
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"it's {time_now}")
    elif "web off" in text or "web remote off" in text:
        speak("Shutting down Flask server")
        os.kill(os.getpid(), signal.SIGINT)
    elif any(keyword in text for keyword in close):
        speak("shutting down computer")
        os.system("shutdown /s /t 5")
    elif any(keyword in text for keyword in exit_commands):
        speak("goodbye")
