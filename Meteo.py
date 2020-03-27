import time
from tkinter import *

def window(current, status):
    
    root = Toplevel()
    root.title("Weather")
    root.geometry("400x200+290+100")

    if "Clear" in status:
        t = time.localtime()
        current_hour = time.strftime("%H", t)
        if int(current_hour) < 18:
            Logo=PhotoImage(file="clear_day.png")
        else:
            Logo=PhotoImage(file="clear_night.PNG")
    elif "Fog" in status:
        Logo=PhotoImage(file="mist.png")
    elif "Rain" in status:
        Logo=PhotoImage(file="rain.png")
    elif "Cloud" in status:
        Logo=PhotoImage(file="clouds.png")
    elif "Snow" in status:
        Logo=PhotoImage(file="snow.png")
    elif "Overcast" in status:
        Logo=PhotoImage(file="overcast.png")
    elif "Drizzle" in status:
        Logo=PhotoImage(file="drizzle.png")
    elif "Windy" in status:
        Logo=PhotoImage(file="windy.png")    
    else:
        Logo = None
    
    LogoCanvas=Canvas(root,height=1170, width=700)
    LogoCanvas.create_image(200,120,image=Logo)
    LogoCanvas.pack()

    LogoCanvas.create_text(50,40,text=str(current)+"°C", font=("time new roman",30))
    LogoCanvas.create_text(50,80,text="Toronto", font=("time new roman",15))
    LogoCanvas.create_text(70,100,text=status, font=("time new roman",15))
    #LogoCanvas.create_text(50,130,text="Today \n" + temp, font=("time new roman",10))
    root.mainloop()

