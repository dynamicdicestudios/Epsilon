import random, time, os, playsound, subprocess, string, forecastio

from Meteo import *

from tkinter import * 

from joke.jokes import *

from Communication import Communication

from PyDictionary import PyDictionary

def dictionary(request):
    dictionary=PyDictionary()
    if request[0] == "meaning":
        answer = dictionary.meaning(request[1])
        if answer == None:
            return "I don't know that word."
        else:
            return answer
    elif request[0] == "synonym":
        answer = dictionary.synonym(request[1])
        if answer == None:
            return "There are no synonyms."
        else:
            return answer
    elif request[0] == "antonym":
        answer = dictionary.antonym(request[1])
        if answer == None:
            return "There are no antonyms."
        else:
            return answer
        
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
            playsound.playsound('Sound.mp3')
            
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
        playsound.playsound('Sound.mp3')

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
        return "Goodbye!"
    elif WORDS[1] in command.title():
        subprocess.call(["shutdown", "/h"])
        return "Goodbye!"
            
def open_command(command):
    cm = Communication()
    # set the list of programs that can be opened
    WORDS = ["Notepad", "Google Chrome", "Microsoft Word", "Microsoft Powerpoint", "Microsoft Excel"]
    sorry = "Sorry, I can't seem to find that program."
    program_exists = False
    
    # determine if command is correct and if any attempts remain
    for word in WORDS:
        if word in command.title(): 
            program_exists = True
            break

    if program_exists:
        if WORDS[0] in command.title():
            os.startfile('notepad.exe')#starts notepad
            return "Opened Notepad"
        elif WORDS[1] in command.title():
            os.startfile("chrome.exe")
            return "Opened Google Chrome"
        elif WORDS[2] in command.title():
            os.startfile("winword.exe")
            return "Opened Microsoft Word"
        elif WORDS[3] in command.title():
            os.startfile("powerpnt.exe")
            return "Opened Microsoft Powerpoint"
        elif WORDS[4] in command.title():
            os.startfile("excel.exe")
            return "Opened Microsoft Excel"
    else:
        program = ""
        command = command.split(" ")
        for i in range(len(command)):
            if ".exe" in command[i]:
                program = word[i]
                break
        try:
            os.startfile(program)
            return "Opened " + program
        except:
            return sorry
