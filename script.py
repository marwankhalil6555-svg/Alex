#import modules
from faster_whisper import WhisperModel
import speech_recognition as audio
from playsound import playsound
from database import *
import sounddevice
import webbrowser
import pywhatkit
import pyautogui
import keyboard
import datetime
import requests
import pyttsx3
import difflib
import random
import time
import os
import re
#set vars
library = os.listdir("C:\\Users\\Shiko-store\\Music")
path = "C:\\Users\\Shiko-store\\Music"
translator = audio.Recognizer()
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
chrome = webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chrome_path))
default_browser = os.environ['BROWSER'] = chrome_path
model = WhisperModel("small.en", device="cpu", compute_type="int8")
sample_rate = 16000
duration = 5
#speak function
def speak(inp):
    agent = pyttsx3.init()
    agent.say(inp)
    agent.setProperty('rate',150)
    agent.runAndWait()
    del agent
#processing command function
def do_command(text):
    if any(keyword in text for keyword in greetings):
        speak("hey, what's up?, how can i help you today?")
        #chat
    elif any(keyword in text for keyword in chat):
        speak("i'm good as long as you good , how can i help you today?")
    #thanks
    elif any(keyword in text for keyword in thanks):
        speak("you are welcome ,  i'm here to help any time")
    #chat about interests
    elif any(keyword in text for keyword in interests):
        speak("that's cool , your interests are special")
    #questions like do you love something
    elif any(keyword in text for keyword in questions):
        speak("sorry i'm not able to answer that kind of questions , may i help in something else?")
    #agent main infos
    elif any(keyword in text for keyword in agent_id):
        speak("my name is alex but you can give me instructions without my name")
    #check the program still working
    elif any(keyword in text for keyword in check):
        speak("yes i'm still here for you , can i help you with something")
    #checks
    elif text in ["alex?","alex"]:
        speak("yes?")
    # ==========================================
    # 2. Browser, Web Navigation & NAS Server
    # ==========================================
    #open browser on google
    elif any(keyword in text for keyword in browser) and "close" not in text:
        speak("opening browser")
        webbrowser.get('chrome').open("https://google.com")
    #social media
    elif any(keyword in text for keyword in browse):
        matches = difflib.get_close_matches(text,websites,cutoff=0.4,n=1)
        if matches:
            matched_web = matches[0]
            speak(f"visiting {matched_web}")
            webbrowser.get('chrome').open(f"{matched_web.strip(".")}.com")
    #youtube
    elif any(keyword in text for keyword in yt):
        text = text.split("on youtube" or "online" or "youtube" and "play",1)
        speak(f"playing {text[1]} online")
        pywhatkit.playonyt(f"{text[1]}",)
    #nas server
    elif any(keyword in text for keyword in server):
        speak("opening server")
        webbrowser.get('chrome').open("http://localhost:8080")
    #close tab
    elif any(keyword in text for keyword in close_tab):
        speak("closeing tab")
        time.sleep(1)
        pyautogui.hotkey('ctrl','w')
    #close browser
    elif any(keyword in text for keyword in close_browser):
        speak("closeing browser")
        os.system("taskkill /f /im chrome.exe")

        # ==========================================
        # 3. Applications & Local Tools
        # ==========================================
        #open file manager
    elif any(keyword in text for keyword in explorer):
        speak("opening explorer")
        os.startfile("c:\\windows\\explorer")
    #open notepad
    elif any(keyword in text for keyword in notepad):
        speak("opening notepad")
        os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\notepad")
    elif any(keyword in text for keyword in terminal):
        speak("opening terminal")
        os.startfile("C:\\Users\\Shiko-store\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\System Tools\\Command Prompt")
    #open coder
    elif any(keyword in text for keyword in code):
        speak("starting code editor")
        os.startfile("C:\\Users\\Shiko-store\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code")
    #valorant
    elif any(keyword in text for keyword in valorant):
        os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Riot Games\\VALORANT")
        speak("because valorant security system i need to go , so yes , goodbye")
        keyboard.press("f7")
        exit()
    # ==========================================
    # 4. Music Playback & Control
    # ==========================================
    #start music with keyword "music"
    elif any(keyword in text for keyword in music) and "stop" not in text and "off" not in text:
        if not any(keyword in text for keyword in randomise):
            speak("what can i play for you?")
        #telling the music name
            with audio.Microphone() as mic:
                print("Listening for song name...")
                translator.pause_threshold = 2.5
                text = ''
                lst = translator.listen(mic)
                text = translator.recognize_whisper(lst,model="base",language='arabic')
                text = text.lower().strip()
                text = smart_txt(text)
                print(f"Song requested: {text}")
            #randomise algorithm to choose random song
                if any(keyword in text for keyword in randomise):
                    song = random.choice(library)
                    os.startfile(f"{path}\\{song}")
            #auto correction to songs
                matches = difflib.get_close_matches(text, library, n=1, cutoff=0.4)
                if matches:
                    matched_file = matches[0] 
                    speak(f"playing {matched_file}")
                    os.startfile(os.path.join(path, matched_file))
                else:
                    speak("Sorry, I couldn't find that song.")
    #play music without the keyword "music" only music name
    elif "play" in text and "music" not in text and "youtube" not in text:
        if not any(keyword in text for keyword in randomise):
            name = text.split("play",1)
            song = name[1].strip()
            matches = difflib.get_close_matches(song,library,n=1,cutoff=0.4)
            if matches:
                matched_file = matches[0]
                speak(f"playing {matched_file}")
                os.startfile(os.path.join(path,matched_file))
            else:
                speak("sorry i couldn't find the song")
        else:
            song = random.choice(library)
            os.startfile(f"{path}\\{song}")
    #random music without keyword music
    elif any(keyword in text for keyword in randomise) and "song" in text:
        speak("playing a random song")
        time.sleep(0.5)
        song = random.choice(library)
        os.startfile(f"{path}\\{song}")
    #stop music
    elif any(keyword in text for keyword in close_music):
        speak("stoping music")
        os.system("taskkill /f /im AIMP.exe")
    # ==========================================
    # 6. modes & remote
    # ==========================================
    #clap mode on
    elif any(keyword in text for keyword in clapy_mode) and "off" not in text:
        speak("starting clapy")
        os.startfile("D:\\Hub\\Alex\\Clapy\\clapy.bat")
    #clap mode off
    elif any(keyboard in text for keyboard in clapy_mode_off):
        speak("clap mode off")
        keyboard.press("f7")
    #sleeping mode
    elif any(keyword in text for keyword in sleeping_mode) and "play" not in text and "visit" not in text:
        speak("sleeping mode")
        while True:
            keyboard.wait("f8")
            speak("i am awake now")
            break
    #chill mode
    elif any(keyword in text for keyword in chill_mode) and "play" not in text:
        chill_song = random.choice(os.listdir("D:\\Hub\\Alex\\chill music"))
        speak("chilling mode on")
        time.sleep(1.3)
        keyboard.press("f7")
        os.startfile("D:\\Hub\\Alex\\Clapy\\clapy.bat")
        time.sleep(1.5)
        os.startfile("D:\\Hub\\Alex\\powershell commands\\chill.vbs")
        os.startfile(f"D:\\Hub\\Alex\\chill music\\{chill_song}")
        webbrowser.get("chrome").open("https://pinterest.com")
    #movies mode
    elif any(keyword in text for keyword in movies):
        speak("starting netflex")
        os.startfile("C:\\Users\\Shiko-store\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Jellyfin Server\\Jellyfin Tray App.lnk")
        webbrowser.get("chrome").open("http://localhost:8096/web/#/wizard/library")
    # ==========================================
    # 5. Volume & Audio Control
    # ==========================================
    #sound control up
    elif any(keyword in text for keyword in vol_up):
        speak("volume up")
        for _ in range(15):
            keyboard.send("volume up")
    #sound control down
    elif any(keyword in text for keyword in vol_down):
        speak("volume down")
        for _ in range(10):
            keyboard.send("volume down")
    #mute
    elif any(keyword in text for keyword in mute):
        speak("mute")
        keyboard.send("volume mute")
    # ==========================================
    # 6. System Commands, Shutdown & Exit
    # ==========================================
    #asking time
    elif any(keyword in text for keyword in time_ask):
        time_now_old = datetime.datetime.now().strftime("%I:%M:%p")
        time_now = time_now_old.replace("0","",1)
        time_now = time_now.replace(":"," ")
        speak(f"it's , {time_now}")
        print(time_now_old)
    #shut down pc
    elif any(keyword in text for keyword in close):
        speak("are you sure you want shutdown pc?")
        with audio.Microphone() as mic:
            text = ''
            lst = translator.listen(mic)
            text = translator.recognize_whisper(lst,model="base")
            text = text.lower().strip()
            text = smart_txt(text)
            if any(keyword in text for keyword in accept):
                os.system("shutdown /s")
                speak("shutting pc down")
                exit()
            else:
                pass
        #exit
    elif any(keyword in text for keyword in exit_commands):
        speak("glad to help you today , goodbye")
        keyboard.press("f7")
        exit()
#oop
class smart_txt(str):
    def __contains__(self,keyword):
        return bool(re.search(rf"\b{re.escape(keyword)}\b",str(self)))
#the program
speak("Hello i am alex , how can i help you?")
while True:
    try:
        #set key
        keyboard.wait("f9")
        #recognition settings
        playsound("D:\\Hub\\Alex\\sfx\\sfx.wav")
        print("Listening for command...")
        audio = sounddevice.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32"
        )
        sounddevice.wait()
        audio = audio.flatten()

        sgmts,info=model.transcribe(audio,language="en",vad_filter=True,beam_size=5,temperature=0,
         vad_parameters={
        "min_silence_duration_ms": 700
            },
        best_of=5,
        condition_on_previous_text=False)
        
        text = ""
        for sgmt in sgmts:
            text += sgmt.text
            text = text.lower().strip()
        print('' .join(text))
        commands = [smart_txt(cmd.strip()) for cmd in text.split(" and ")]
        for text in commands:
            do_command(text)
        #off sound
        playsound("D:\\Hub\\Alex\\sfx\\sfx.wav")

    #errors area
    except Exception as e:
        speak(f"sorry command error , {e}")
        print(f"{e}")
#   dev_name: marwan-same
