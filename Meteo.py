from tkinter import *

def window(current, status):
    
    root = Toplevel()
    root.title("Weather")
    root.geometry("400x200+290+100")

    if "Clear" in status:
        Logo=PhotoImage(file="clear.png")
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
    else:
        Logo = None

    #current = int(round(current, 0))
    
    LogoCanvas=Canvas(root,height=1170, width=700)
    LogoCanvas.create_image(200,120,image=Logo)
    LogoCanvas.pack()

    LogoCanvas.create_text(50,40,text=str(current)+"°C", font=("time new roman",30))
    LogoCanvas.create_text(50,80,text="Toronto", font=("time new roman",15))
    LogoCanvas.create_text(78,100,text=status, font=("time new roman",15))
    #LogoCanvas.create_text(50,130,text="Today \n" + temp, font=("time new roman",10))
    root.mainloop()
    #root.configure(background='light blue')
