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
    
    return "break"
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
