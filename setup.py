from cx_Freeze import setup, Executable

base = None    

executables = [Executable("Epsilon.py", base=base)]

packages = ["idna", "random", "time", "os",
            "playsound", "subprocess", "string",
            "wolframalpha", "psutil", "multiprocessing", "Files", 
            "joke", "Communication", "threading", "Chatter", "speech_recognition",
            "datetime", "pyttsx3", "chatterbot", "chatterbot.trainers",
            "chatterbot.conversation", "warnings", "nltk"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Epsilon",
    options = options,
    version = "1.0.0",
    description = 'Windows 8.1 Virtual Assistant',
    executables = executables
)
