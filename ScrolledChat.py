import time, threading, random, playsound
from tkinter import *
import tkinter.scrolledtext as tkst
from Commands import *
from Communication import Communication

def greeting():
    t = time.localtime()
    current_hour = time.strftime("%H", t)
    if int(current_hour) < 12:
        greeting = "Good Morning! I'm Epsilon!"
    elif int(current_hour) >= 12 and int(current_hour) <= 16:
        greeting = "Good Afternoon! I'm Epsilon!"
    elif int(current_hour) > 16:
        greeting = "Good Evening! I'm Epsilon!"
    else:
        greeting = "Good Night!"

    return greeting

def respond(text):    
    WORDS = ["Open", "System", "Notes", "Weather", "Joke", "Time", "Help", "Work", "Battery", "Button"]
    SORRY = "Sorry, I'm not sure what you mean."
    response = ""
    if WORDS[0].lower() in text.lower():
        response = open_command(text.lower())
    elif WORDS[1].lower() in text.lower():
        response = system_command(text.lower())
    elif WORDS[2].lower() in text.lower():
        notes_command('w')
    elif WORDS[3].lower() in text.lower():
        response = weather_command()
    elif WORDS[4].lower() in text.lower():
        response = jokes_command()
    elif WORDS[5].lower() in text.lower():
        response = time_command()
    elif WORDS[6].lower() in text.lower() or WORDS[7].lower() in text.lower():
        response = manual()
    elif WORDS[8].lower() in text.lower():
        response = battery_info()
    elif WORDS[9].lower() in text.lower():
        response = buttons_info()
    else:
        try:
            response = wolfram_command(text)
        except:
            response = SORRY
        
    return response    

def main():
    cm = Communication()
    window = Tk()
    messages = Text(window)
    
    speak = PhotoImage(file = "speaker_icon.png")
    options = PhotoImage(file = "headset_icon.png")
    
    window.title("Epsilon")

    greet = greeting()

    cm.voice(greet)

    messages.pack(fill='both', expand='yes')
    editArea = tkst.ScrolledText(
        master = messages,
        wrap   = WORD,
        width  = 20,
        height = 10
    )

    editArea.insert(INSERT, "Epsilon: " + greet + "\n\n")
    editArea.config(state=DISABLED)
    messages.config(state=DISABLED)

    input_user = StringVar()
    input_field = Entry(window, text=input_user)
    input_field.pack(side=BOTTOM, fill=None, ipadx=15)

    editArea.configure(background='light steel blue')
    messages.configure(background='light grey')
    input_field.configure(background='light goldenrod')

    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def hands_free():
        window.withdraw()
        while True:
            check = cm.recognize_speech_from_mic()
            if check["transcription"] and "epsilon" in check["transcription"].lower():
                playsound.playsound('Sound.mp3', True)
                command = cm.recognize_speech_from_mic()
                if command["transcription"] or not command["success"]:
                    if "exit" in command["transcription"].lower():
                        break
                    cm.voice(epsilon(requests))
        window.deiconify()
    def listen():
        misunderstand = "I didn't catch that. What did you say?"
        
        input_field.config(state=DISABLED)
        playsound.playsound('Sound.mp3', True)
        
        command = cm.recognize_speech_from_mic()        
        if command["transcription"] or not command["success"]:
            editArea.config(state="normal")
            editArea.insert(INSERT, 'You: %s\n\n' % command["transcription"])
            editArea.config(state=DISABLED)

            input_field.config(state="normal")

            epsilon(command["transcription"])

        elif command["error"]:
            input_field.config(state="normal")
            epsilon(" ")
        """else:
            editArea.config(state="normal")
            editArea.insert(INSERT, 'You: %s\n\n' % misunderstand)
            editArea.config(state=DISABLED)
            cm.voice(misunderstand)"""
            
    def start():
        stt = threading.Thread(target=listen)
        stt.start()

    
    def enter_pressed(event):
        input_get = input_field.get()
        if input_get.isspace():
            return "break"
        
        editArea.config(state="normal")
        editArea.insert(INSERT, 'You: %s\n\n' % input_get)
        editArea.config(state=DISABLED)
        input_user.set('')
        
        if "weather" in input_get.lower():
            epsilon(input_get)
        else:    
            thread = threading.Thread(target=epsilon, args = (input_get,))
            thread.start()
            
            return "break"
        
    def epsilon(text):
        answer = respond(text)
        editArea.config(state=NORMAL)
        editArea.insert(INSERT, 'Epsilon: %s\n\n' % answer)
        editArea.config(state=DISABLED)

        cm.voice(answer)

    input_field.bind("<Return>", enter_pressed)    
    stt = threading.Thread(target=listen)

    
    Button(window, text = '', image = speak, height = 15, width = 25, command=start).place(x=177, y=187)
    Button(window, text = '', image = options, height = 15, width = 18, command=hands_free).place(x=0, y=187)
    
    window.mainloop()

main()
