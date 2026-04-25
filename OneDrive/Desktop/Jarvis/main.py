import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclibrary
from thefuzz import process
#pip install pocktsphinx

# Initialize engines once
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c_lower = c.lower()
    
    if "open google" in c_lower:
        webbrowser.open("https://google.com")
    elif "open youtube" in c_lower:
        webbrowser.open("https://youtube.com")  
    elif "open instagram" in c_lower:
        webbrowser.open("https://instagram.com")  
    elif "open facebook" in c_lower:
        webbrowser.open("https://facebook.com")  
    elif "open linkedin" in c_lower:
        webbrowser.open("https://linkedin.com") 
    elif "open trade room" in c_lower:
        webbrowser.open("https://www.youtube.com/@thetraderoomsss")
    elif c_lower.startswith("play"):
        from thefuzz import process
        song_input = " ".join(c_lower.split(" ")[1:]).strip()
        song_list = list(musiclibrary.music.keys())
        
        result = process.extractOne(song_input, song_list)
        if result:
            best_match, score = result[0], result[1]
            if score > 50:
                link = musiclibrary.music[best_match]
                # TO PLAY SONG FROM PAUSE (Appends autoplay to the URL)
                webbrowser.open(link + "&autoplay=1")
            else:
                print("No match found in library.") 
        else:
            print("Library is empty or command not recognized.")

if __name__ == "__main__":
    speak("Initializing Alexa......")
    
    while True:
        # Listen for the wake word "Alexa"
        # obtain audio from the microphone
        
        try:
            with sr.Microphone() as source:
                print("Recognizing.....")
                # Adjust for noise to improve wake-word accuracy
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Say Listening")
                
                # recognize speech using Sphinx/google
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                
                # Debugging: See what the bot heard
                print(f"Heard: {word}")

                if word.lower() == "alexa":
                    speak("Yes")
                    
                    # Listen to command 
                    with sr.Microphone() as source:
                        print("Alexa Active...")
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        
                        processCommand(command)
              
        except sr.UnknownValueError:
            # This handles cases where the mic hears noise but no speech
            pass 
        except Exception as e:
            print("Error; {0}".format(e))