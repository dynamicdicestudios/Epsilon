import time
from tkinter import *
import tkinter.scrolledtext as tkst

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
        response = SORRY
        
    return response

window = Tk()
messages = Text(window)

window.title("Epsilon")


messages.pack(fill='both', expand='yes')
editArea = tkst.ScrolledText(
    master = messages,
    wrap   = WORD,
    width  = 20,
    height = 10
)
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
    messages.config(state=NORMAL)
    messages.insert(INSERT, 'Epsilon: %s\n\n' % answer)
    messages.config(state=DISABLED)
    try:
        cm.voice(answer)
    except:
        pass
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
