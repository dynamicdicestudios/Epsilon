import time, threading, random
from tkinter import *
import tkinter.scrolledtext as tkst
from Commands import *
from Communication import Communication

def greeting():
    t = time.localtime()
    current_hour = time.strftime("%H", t)
    if int(current_hour) < 12:
        greeting = "Good Morning! I'm Epsilon!"
    elif int(current_hour) > 12 and int(current_hour) < 16:
        greeting = "Good Afternoon! I'm Epsilon!"
    elif int(current_hour) > 16:
        greeting = "Good Evening! I'm Epsilon!"
    else:
        greeting = "Good Night!"

    return greeting

def respond(text):    
    WORDS = ["Open", "System", "Notes", "Manual", "Weather", "Joke"]
    SORRY = "Sorry, I'm not sure what you mean."
    response = ""
    if WORDS[0].lower() in text:
        response = open_command(text)
    elif WORDS[1].lower() in text:
        response = system_command(text)
    elif WORDS[2].lower() in text:
        notes_command('w')
    elif WORDS[4].lower() in text:
        response = weather_command()
    elif WORDS[5].lower() in text:
        response = jokes_command()
    else:
        try:
            response = wolfram(text)
        except:
            response = SORRY
        
    return response
def main():
    cm = Communication()
    window = Tk()
    messages = Text(window)

    window.title("Epsilon")

    greet = greeting()
    try:
        cm.voice(greet)
    except:
        pass

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
        try:
            for ans in answer.values():
                cm.voice(ans[random.randint(0, len(answer.values()))])
                break
        except:
            cm.voice(answer)

    input_user = StringVar()
    input_field = Entry(window, text=input_user)
    input_field.pack(side=BOTTOM, fill=X)

    editArea.configure(background='light steel blue')
    messages.configure(background='light grey')
    input_field.configure(background='light goldenrod')

    input_field.bind("<Return>", enter_pressed)

    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=BOTH, expand=True)
    window.mainloop()

main()
