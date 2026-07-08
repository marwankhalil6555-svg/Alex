r#import modules
import speech_recognition as audio
import pyttsx3
import os
import time
import webbrowser
import difflib
import random
from database import *
#set vars
library = os.listdir("D:\\Hub\\Alex\\music")
path = "D:\\Hub\\Alex\\music"
#the program
while True:
    try:
        #recognition settings
        translator = audio.Recognizer()
        translator.energy_threshold = 200
        translator.dynamic_energy_threshold = False
        print("\nListening for a command...")
        #microphone
        with audio.Microphone() as mic:
            text = ''
            lst = translator.listen(mic)
            text = translator.recognize_whisper(lst)
            text = text.lower().strip()
            print(f"You said: {text}")
        
        if not text:
            continue
        #greetings [hello,hi,...else]
        if any(keyword in text for keyword in greetings):
            agent = pyttsx3.init()
            talk_rate = agent.getProperty('rate')
            agent.setProperty("rate", 180)
            agent.say("hey, what's up?, how can i help you today?")
            agent.runAndWait()
            del agent
        #chat
        elif any(keyword in text for keyword in chat):
            agent = pyttsx3.init()
            agent.say("i'm good as long as you good , how can i help you today?")
            agent.runAndWait()
            del agent
        #open browser on google
        elif any(keyword in text for keyword in browse):
            agent = pyttsx3.init()
            agent.say("running browser")
            agent.runAndWait()
            webbrowser.open("google.com")
            del agent
        #start music wit keyword "music"
        elif any(keyword in text for keyword in music):
            agent = pyttsx3.init()
            agent.say("what can i play for you?")
            agent.runAndWait()
            del agent
            #telling the music name
            with audio.Microphone() as mic:
                print("Listening for song name...")
                translator.pause_threshold = 2.5
                text = ''
                lst = translator.listen(mic)
                text = translator.recognize_whisper(lst)
                text = text.lower().strip()
                print(f"Song requested: {text}")
                #randomise algorithm to choose random song
                if any(keyword in text for keyword in randomise):
                    song = random.choice(library)
                    os.startfile(f"D:\\Hub\\Alex\\music\\{song}")
                    continue
                #auto correction to songs
                matches = difflib.get_close_matches(text, library, n=1, cutoff=0.4)
                if matches:
                    matched_file = matches[0] 
                    agent = pyttsx3.init()
                    agent.say(f"Playing {matched_file}")
                    agent.runAndWait()
                    os.startfile(os.path.join(path, matched_file))
                    del agent
                else:
                    agent = pyttsx3.init()
                    agent.say("Sorry, I couldn't find that song.")
                    agent.runAndWait()
                    del agent
        #open file manager
        elif any(keyword in text for keyword in explorer):
            agent = pyttsx3.init()
            agent.say("starting explorer")
            agent.runAndWait()
            os.startfile("c:\\windows\\explorer")
            del agent
        #open notepad
        elif any(keyword in text for keyword in notepad):
            agent = pyttsx3.init()
            agent.say("opening notepad")
            agent.runAndWait()
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\notepad")
            del agent
        #chat about interests
        elif any(keyword in text for keyword in interests):
            agent = pyttsx3.init()
            agent.say("that's cool , your interests are special")
            agent.runAndWait()
            del agent
        #questions like do you love something
        elif any(keyword in text for keyword in questions):
            agent = pyttsx3.init()
            agent.say("sorry i'm not able to answer that kind of questions , may i help in something else?")
            agent.runAndWait()
            del agent
        #agent main infos
        elif any(keyword in text for keyword in agent_id):
            agent = pyttsx3.init()
            agent.say("i don't have a specific name or age ,  you can call me what you want")
            agent.runAndWait()
            del agent
        #check the program still working
        elif any(keyword in text for keyword in check):
            agent = pyttsx3.init()
            agent.say("yes i'm still here for you , can i help you with something")
            agent.runAndWait()
            del agent
        #play music without the keyword "music" only music name
        elif "play" in text and "music" not in text:
            name = text.split("play",1)
            song = name[1].strip()
            matches = difflib.get_close_matches(song,library,n=1,cutoff=0.4)
            if matches:
                matched_file = matches[0]
                agent = pyttsx3.init()
                agent.say(f"playing {matched_file}")
                agent.runAndWait()
                os.startfile(os.path.join(path,matched_file))
                del agent
            else:
                agent = pyttsx3.init()
                agent.say("sorry i couldn't find the song")
                agent.runAndWait()
                del agent
        #to exit the program
        elif any(keyword in text for keyword in exit_commands):
            agent = pyttsx3.init()
            agent.say("glad to help you today , goodbye")
            agent.runAndWait()
            del agent
            exit()
    #errors area
    except Exception as e:
        print(f"System Error: {e}")
        agent = pyttsx3.init()
        agent.say("sorry command not defined")
        agent.runAndWait()
        del agent

#important note:
#   i didn't used the def to make a function to talk because i already wrote the code (agent.say())
#   so i know that makes the code bigger without any reason or necessity but chill
#   it's a random project for a 16 years old teenager not openai developers
#   devloper_name: marwan-same 
