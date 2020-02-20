import random, time, os, pygame.mixer, subprocess, string, forecastio

from Meteo import *

from tkinter import * 

from joke.jokes import *

from Communication import Communication

def music_command():
    pass

def jokes_command():
    cm = Communication()
    from random import choice
    try:
        funny = choice([geek, icanhazdad, icndb])()
    except:
        return "You are not connected to any Wifi source"
    
    while "â" in funny:
        funny = funny.replace("â", "'")
        
    return funny
    
def weather_command():
    api_key = "a7fd1a0c2e6b92fcd9ead78f712103a8"
    lat = 43.651070
    lng = -79.347015
    try:
        forecast = forecastio.load_forecast(api_key, lat, lng)
    except:
        return "You are not connected to any Wifi source"
    hourly = forecast.hourly()
    daily = forecast.daily()
    
    #hourly.update()
    
    status = hourly.data[0].d['summary']
    current = hourly.data[0].d['temperature']
    current = round(current)
    
    temp_min = str(daily.data[0].d)
    #temp = temp_min + "/" + temp_max
    
    window(current, status)
    return str(current)+"°C" 
    
def manual():
    cm = Communication()
    explain = ("I am a Windows 8.1 helper that was coded in Python."
               "After pressing the speech button, wait for the beep."
               "Here's a list of what I can do!:")
    instructions =("I can open programs."
               "shutdown or hibernate your device."
               "tell jokes and the weather"
               "and take notes. I hope I may be of assistance!")
    try:
        cm.voice(explain)
        cm.voice(instructions)
    except:
        pass

def notes_command(mode, space=""):
    
    cm = Communication()
    def end():
        cm.voice(finish)
        while(True):
            #Beep sound to notify the user when to speak
            pygame.mixer.music.load('Sound.mp3')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
            time.sleep(1)
            pygame.mixer.music.stop()
            
            command = cm.recognize_speech_from_mic()
            if command["transcription"]:
                break
            if not command["success"]:
                break
            cm.voice("I didn't catch that. What did you say?\n")

        if "yes" in command["transcription"]:
            cm.voice("Very well! Appending punctuation!")
            punctuation()
        elif "no" in command["transcription"]:
            notes_command('a', "\n")
        else:
            cm.voice("Sorry, that's not a command.")
            end()

    def punctuation():
        readfile = open('note.txt', 'r')
        writefile = open('note.txt', 'a')

        for line in readfile:
            if line.find("period") != -1:
                writefile.replace("period", ". ")
            if line.find("comma") != -1:
                writefile.replace("comma", ", ")
            if line.find("exclamation mark") != -1:
                writefile.replace("exclamation mark", "! ")
            if line.find("question mark") != -1:
                writefile.replace("question mark", "? ")
            if line.find("newline") != -1:
                writefile.replace("newline", "\n")
            """#rtn = re.split('([.!?] *)', line)
            rtn = ([line[i:i+1] for i in range(0, len(line), len(line))])
            #final = ''.join([i.capitalize() for i in rtn])
            writefile.replace(rtn, rtn.capitalize())"""
    
    notes = open('note.txt', mode)
    
    start = "Ready when you are!"
    finish = "Will that be all?"
    
    cm.voice(start)
    
    while(True):
        #Beep sound to notify the user when to speak
        pygame.mixer.music.load('Sound.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()
        time.sleep(1)
        pygame.mixer.music.stop()
        
        command = cm.recognize_speech_from_mic()
        if command["transcription"]:
            break
        if not command["success"]:
            break
        cm.voice("I didn't catch that. What did you say?\n")

    notes.write(space + "{}".format(command["transcription"].capitalize()))
    notes.close()

    end()
    
def system_command(command):
    cm = Communication()
    WORDS = ["Shutdown", "Hibernate"]
    try:
        cm.voice("Goodbye!")
    except:
        pass
    if WORDS[0] in command.title():
        subprocess.call(["shutdown", "/s"])
    elif WORDS[1] in command.title():
        subprocess.call(["shutdown", "/h"])
            
def open_command(command):
    cm = Communication()
    # set the list of programs that can be opened
    WORDS = ["Notepad", "Google Chrome", "Microsoft Word", "Microsoft Powerpoint", "Microsoft Excel"]

    # determine if command is correct and if any attempts remain
    for word in WORDS:
        if word in command.title(): 
            command_is_correct = True
            break

    if command_is_correct:
        if WORDS[0] in command.title():
            try:
                cm.voice("opening notepad!!")#says that
            except:
                pass
            os.startfile('notepad.exe')#starts notepad
            return "Opening Notepad"
        elif WORDS[1] in command.title():
            try:
                cm.voice("opening google chrome!!")
            except:
                pass
            os.startfile("chrome.exe")
            return "Opening Google Chrome"
        elif WORDS[2] in command.title():
            try:
                cm.voice("opening microsoft word!!")
            except:
                pass
            os.startfile("winword.exe")
        elif WORDS[3] in command.title():
            try:
                cm.voice("opening microsoft powerpoint!!")
            except:
                pass
            os.startfile("powerpnt.exe")
        elif WORDS[4] in command.title():
            try:
                cm.voice("opening microsoft excel!!")
            except:
                pass
            os.startfile("excel.exe")
    else:
        try:
            cm.voice("Sorry, that's not a command.")
        except:
            return "Sorry, that's not a command."
