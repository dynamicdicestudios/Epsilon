import speech_recognition as sr
import os, time, playsound, datetime, pyttsx3

from gtts import gTTS

class Communication():

    def __init__(self):
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
    
    def recognize_speech_from_mic(self):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating w\hether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """

        """if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")"""

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        
        try:
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response
    
    def voice(self, words):
        try:
            speak = gTTS(text = words, lang ='en-uk') 
            # saving the audio file given by google text to speech 
            date = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            file = "voice"+date+".mp3"
            speak.save(file) 
              
            # playsound package is used to play the same file. 
            playsound.playsound(file, True)  
            os.remove(file)
        except:
            engine = pyttsx3.init()
            engine.setProperty('volume',1.0)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[2].id)
            engine.say(words)
            engine.runAndWait()
