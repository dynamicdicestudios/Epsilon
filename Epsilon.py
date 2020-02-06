import random, time, os, pygame.mixer

#hides the pygame message to disable any usage
#of the console whatsoever
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from tkinter import * 

from Commands import *

from Communication import Communication

def main():
    root = Tk()
    cm = Communication()
    
    root.title("Epsilon")
    root.geometry("400x290+290+100")

    Logo=PhotoImage(file="back.png")
    LogoCanvas=Canvas(root,height=1170, width=700)
    LogoCanvas.create_image(200,120,image=Logo)
    LogoCanvas.pack()
    
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

    cm.voice(greeting)
        
    def window():
        Button(root, text='Quit', width = 5,command=root.destroy).place(x=20,y=250)
        Button(root, text='Speak',width=10, command=listen).place(x=170,y=250)
        Button(root, text='Help',width=5, command=manual).place(x=340,y=250)

        root.mainloop()
    window()
    
def listen():

    cm = Communication()
    
    WORDS = ["Open","System","Notes", "Manual", "Weather", "Joke"]
    misunderstand = "I didn't catch that. What did you say?"
    sorry = "Sorry, I can't do that."

    command_is_correct = False

    def model(text):
        cm = Communication()
        # This function will pass your text to the machine learning model
        # and return the top result with the highest confidence
        def classify(text):
            key = "653eced0-1840-11ea-97a0-956abe0146c6b32257f5-24cc-4bfa-b944-21223a9adadc"
            url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

            response = requests.get(url, params={ "data" : text })

            if response.ok:
                responseData = response.json()
                topMatch = responseData[0]
                return topMatch
            else:
                response.raise_for_status()


        # CHANGE THIS to something you want your machine learning model to classify
        demo = classify(text)

        label = demo["class_name"]
        return label

    

    while(True):
        #Beep sound to notify the user when to speak
        pygame.mixer.music.load('Sound.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()
        time.sleep(1)
        pygame.mixer.music.stop()

        command = cm.recognize_speech_from_mic()
        error = "ERROR: {}".format(command["error"])
        speech = "You said: {}".format(command["transcription"])
        if command["transcription"]:
            break
        if not command["success"]:
            break
        cm.voice(misunderstand)

    # if there was an error, stop the game
    if command["error"]:
        cm.voice(error)

    # show the user the transcription
    #cm.voice(speech)
    
    if WORDS[0] in command["transcription"]:
        open_command(command["transcription"])
    elif WORDS[1] in command["transcription"]:
        system_command(command["transcription"])
    elif WORDS[3] in command["transcription"]:
        notes_command('w')
    elif WORDS[4] in command["transcription"]:
        weather_command()
    elif WORDS[5] in command["transcription"]:
        jokes_command()
    else:
        cm.voice(sorry)
        listen()
        
main()
