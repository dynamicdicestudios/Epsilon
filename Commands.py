import random, time, os, playsound, subprocess, string, smtplib, ssl
import wolframalpha, psutil
#import forecastio
from multiprocessing.pool import ThreadPool

#from Meteo import *

from Files import *

from tkinter import * 

from joke.jokes import *

from Communication import Communication

def punctuation(text):
    text = text.replace(" exclamation mark", "!")
    text = text.replace(" question mark", "?")
    text = text.replace(" period", ".")
    text = text.replace(" dot", ".")
    text = text.replace(" underscore", "_")
    text = text.replace(" newline", "\n")
    text = text.replace(" tab", "\t")

    return text

def email_text(request):
    request = punctuation(request)
    print(request)
    command = request.split(" ")
    
    address = "@gmail.com"
    student_address = "@student.tdsb.on.ca"
    teacher_address = "@tdsb.on.ca"

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "mattheglas@gmail.com"  # Enter your address
    password = "Poptropica30"
    
    if "student" in command[1].lower():
        receiver = "".join(command[2:command.index("message")])
        receiver_email = receiver + student_address  # Enter receiver address
    else:
        receiver = "".join(command[1:command.index("message")])
        receiver_email = receiver + address  # Enter receiver address
        print(receiver_email)
    
    message = " ".join(command[command.index("message")+1:])
    print(message)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except:
        return "Sorry sir, an error occured."

    return "Message sent!"

def handsfree_info():
    return ("After pressing the button on the left, the GUI will disappear. "
            "Whenever you have a request, say 'Epsilon' and wait for me to "
            "say 'Yes sir?' and I will listen to your request. When you wish "
            "to exit hands-free mode, say 'exit' after I say 'Yes sir?'."
            "Note: any requests made during hands-free mode will not show up "
            "on the GUI.")

def buttons_info():
    return ("The button on the left activates hands-free mode. "
            "This allows you to use me without the GUI. "
            "Simply say Epsilon and wait for me to say 'Yes sir?' "
            "and I will listen to your request. "
            "The button on the right is speaking mode. "
            "This allows you to verbally declare your request, after the beep, "
            "and temporarily disables the input field.")

def battery_info():
    battery = psutil.sensors_battery()
    if battery.power_plugged:
        return str(battery.percent) + " percent remaining and charging."
    else:
        return str(battery.percent) + " percent remaining and not charging."

def time_command():
    t = time.localtime()
    return time.strftime("%H:%M", t)

def wolfram_command(request):
    client = wolframalpha.Client('PK4488-PYV5K4RK5G')

    res = client.query(request)
    output = next(res.results).text
    return output
        
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
    
"""
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
    return "It is currently " + current + "°C and " + status.lower() 
"""

def manual():
    cm = Communication()
    explain = ("I am a Windows 8.1 helper that was coded in Python. "
               "Here's a list of what I can do!: ")
    instructions =("I can open programs, "
                   "shutdown or hibernate your device, "
                   "tell jokes, take notes "
                   "and provide you with (almost) any information. "
                   "I hope I may be of assistance!")
    return explain + instructions

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
    pool = ThreadPool(processes=1)
    
    sorry = "Sorry, I can't seem to find that program."
    program = ""

    async_result = pool.apply_async(exe_finder)
    s, t = async_result.get()

    words = command.split(" ")
    for word in words:
        if word.endswith(".exe"):
            program = word
    
    if program in s:
        os.startfile(program)
        return "Starting " + program
    elif program in t:
        os.startfile(program)
        return "Starting " + program
    else:
        return sorry
