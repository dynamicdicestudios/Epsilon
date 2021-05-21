import time, threading, random, playsound
from tkinter import *
import tkinter.scrolledtext as tkst
from Commands import *
from Chatter import chatter_response
from Communication import Communication
from Levenshtein import iterative_levenshtein

def greeting() -> str:
    t = time.localtime()
    current_hour = time.strftime("%H", t)
    if int(current_hour) < 12:
        greeting = "Good morning!"
    elif int(current_hour) >= 12 and int(current_hour) <= 16:
        greeting = "Good afternoon!"
    elif int(current_hour) > 16:
        greeting = "Good evening!"
    else:
        greeting = "Good Night!"

    return greeting

def respond(text: str) -> str:    
    WORDS = ["Open", "System", "Email", "Notes", "Joke", "Time", "Help", "Battery", "Button", "Handsfree"]
    SORRY = "I'm not quite sure what you mean."
    response = ""
    chatter_results = chatter_response(text)
    if WORDS[0].lower() in text:
        response = open_command(text.lower())
    elif WORDS[1].lower() in text:
        response = system_command(text.lower())
    elif WORDS[2].lower() in text.lower():
        response = email_text(text)
    elif str(chatter_results) in WORDS:
        if WORDS[3] == str(chatter_results):
            notes_command('w')
        elif WORDS[4] == str(chatter_results):
            response = jokes_command()
        elif WORDS[5] == str(chatter_results):
            response = time_command()
        elif WORDS[6] == str(chatter_results):
            response = manual()
        elif WORDS[7] == str(chatter_results):
            response = battery_info()
        elif WORDS[8] == str(chatter_results):
            response = buttons_info()
        elif WORDS[9] == str(chatter_results):
            response = handsfree_info()
    else:
        if str(chatter_results) == SORRY:
            try:
                response = wolfram_command(text)
            except:
                response = str(chatter_results)
        else:
            response = str(chatter_results)
        
    return response    

def main():
    cm = Communication()
    window = Tk()
    
    speak = PhotoImage(file = "speaker_icon.png")
    options = PhotoImage(file = "headset_icon.png")
    
    window.title("Epsilon")
    window.resizable(False, False)

    respond("hi")

    greet = greeting()

    cm.voice(greet)

    editArea = tkst.ScrolledText(
        master = window,
        wrap   = WORD,
        width  = window.winfo_width(),
        height = window.winfo_height()
    )

    editArea.insert(END, "Epsilon: " + greet + "\n\n")
    editArea.config(state=DISABLED)

    input_user = StringVar()
    input_field = Entry(window, text=input_user)
    input_field.pack(side=BOTTOM, fill=None, ipadx=15)

    editArea.configure(background='light steel blue')
    input_field.configure(background='light goldenrod')

    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def hands_free():
        cm.voice("Entering hands-free mode.")
        window.withdraw()
        end = False
        while end == False:
            check = cm.recognize_speech_from_mic()
            print(check["transcription"])
            if check["transcription"] and iterative_levenshtein("epsilon", check["transcription"].lower()) <= 3:
                cm.voice("Yes, sir?")
                while True:
                    command = cm.recognize_speech_from_mic()
                    print(command["transcription"])
                    if command["transcription"] or not command["success"]:
                        if "exit" in command["transcription"].lower():
                            end = True
                            break
                        elif "at ease" in command["transcription"].lower():
                            cm.voice("Sure, I'm hear when you need me!")
                            break
                        else:
                            cm.voice(respond(command["transcription"]))
        window.deiconify()

    def listen():
        input_field.config(state=DISABLED)
        playsound.playsound('Sound.mp3', True)
        
        command = cm.recognize_speech_from_mic()
        print(command["transcription"])
        if command["transcription"] or not command["success"]:
            editArea.config(state="normal")
            editArea.insert(END, 'You: %s\n\n' % command["transcription"])
            editArea.config(state=DISABLED)

            answer(command["transcription"])
        else:
            answer("5ytr79i86fyr45rf8")

        input_field.config(state="normal")
            
    def start():
        stt = threading.Thread(target=listen)
        stt.start()

    
    def enter_pressed(event):
        input_get = input_field.get()
        if input_get.isspace():
            return "break"
        
        editArea.config(state="normal")
        editArea.insert(END, 'You: %s\n\n' % input_get)
        editArea.config(state=DISABLED)
        input_user.set('')
            
        thread = threading.Thread(target=answer, args = (input_get,))
        thread.start()
        
        return "break"
        
    def answer(text:str):
        answer = respond(text)
        editArea.config(state=NORMAL)
        editArea.insert(END, 'Epsilon: %s\n\n' % answer)
        editArea.config(state=DISABLED)

        cm.voice(answer)

    input_field.bind("<Return>", enter_pressed)
    
    Button(window, text = '', image = speak, height = 15, width = 25, command=start).place(x=177, y=187)
    Button(window, text = '', image = options, height = 15, width = 18, command=hands_free).place(x=0, y=187)
    
    window.mainloop()
    

main()
