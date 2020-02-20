import time, threading
from tkinter import *
from Commands import *
from Communication import Communication

def greeting():
    t = time.localtime()
    current_hour = time.strftime("%H", t)
    if int(current_hour) < 12:
        greeting = "Good Morning! I'm Epsilon!"
    elif int(current_hour) >= 12 and int(current_hour) < 16:
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
        open_command(text)
    elif WORDS[1].lower() in text:
        system_command(text)
    elif WORDS[2].lower() in text:
        notes_command('w')
    elif WORDS[4].lower() in text:
        response = weather_command()
    elif WORDS[5].lower() in text:
        response = jokes_command()
    else:
        response = SORRY
        
    return response
    
def main():
    window = Tk()
    cm = Communication()

    window.title("Epsilon")

    messages = Text(window)
    messages.pack()

    greet = greeting()
    try:
        cm.voice(greet)
    except:
        pass
    
    messages.insert(INSERT, "Epsilon: " + greet + "\n\n")
    messages.config(state=DISABLED)

    input_user = StringVar()
    input_field = Entry(window, text=input_user)
    input_field.pack(side=BOTTOM, fill=X)
    
    window.configure(background='light grey')
    messages.configure(background='light steel blue')
    input_field.configure(background='light goldenrod')

    def enter_pressed(event):
        input_get = input_field.get()
        if input_get.isspace():
            return "break"
        
        messages.config(state=NORMAL)
        messages.insert(INSERT, 'You: %s\n\n' % input_get)
        messages.config(state=DISABLED)
        input_user.set('')
        window.update()
        
        if "weather" in input_get.lower() or "open" in input_get.lower():
            epsilon(input_get)
        else:    
            thread = threading.Thread(target=epsilon, args = (input_get,))
            thread.start()
        
        return "break"
    
    def epsilon(text):
        answer = respond(text)
        if answer.isspace():
            pass
        else:
            messages.config(state=NORMAL)
            messages.insert(INSERT, 'Epsilon: %s\n\n' % answer)
            messages.config(state=DISABLED)
            try:
                cm.voice(answer)
            except:
                pass

    frame = Frame(window)  
    input_field.bind("<Return>", enter_pressed)
    frame.pack()

    window.mainloop()

main()
