import time
from tkinter import *
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
    cm = Communication()
    
    WORDS = ["Open", "System", "Notes", "Manual", "Weather", "Joke"]
    SORRY = "Sorry, I can't do that."

    if WORDS[0] in text:
        open_command(text)
    elif WORDS[1] in text:
        system_command(text)
    elif WORDS[2] in text:
        notes_command('w')
    elif WORDS[4] in text:
        weather_command()
    elif WORDS[5] in text:
        response = jokes_command()
    else:
        response = SORRY
        
    return response
    
def main():
    window = Tk()
    cm = Communication()

    messages = Text(window)
    messages.pack()

    greet = greeting()

    cm.voice(greet)

    messages.insert(INSERT, "Epsilon: " + greet + "\n\n")
    messages.config(state=DISABLED)

    input_user = StringVar()
    input_field = Entry(window, text=input_user)
    input_field.pack(side=BOTTOM, fill=X)

    def enter_pressed(event):
        input_get = input_field.get()
        if input_get.isspace():
            return "break"
        
        messages.config(state="normal")
        messages.insert(INSERT, 'You: %s\n\n' % input_get)
        messages.config(state=DISABLED)
        input_user.set('')
        
        epsilon(input_get)
        
        return "break"
    
    def epsilon(text):
        response = respond(text)
        messages.config(state="normal")
        messages.insert(INSERT, 'Epsilon: %s\n\n' % response)
        messages.config(state=DISABLED)

        cm.voice(response)

    frame = Frame(window)  
    input_field.bind("<Return>", enter_pressed)
    frame.pack()

    window.mainloop()

main()
