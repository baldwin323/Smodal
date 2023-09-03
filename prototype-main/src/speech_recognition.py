import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Function to convert speech to text
def speech_to_text():
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        # using google speech recognition
        print("Text: "+r.recognize_google(audio_text))
        return r.recognize_google(audio_text)
    except:
         print("Sorry, I did not get that")
         return ""       

def text_to_speech(text_string):
    # Import the required module for text 
    # to speech conversion
    from gtts import gTTS

    # This module is imported so that we can 
    # play the converted audio
    import os

    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=text_string, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named 
    # welcome 
    myobj.save("welcome.mp3")

    # Playing the converted file
    os.system("mpg321 welcome.mp3")