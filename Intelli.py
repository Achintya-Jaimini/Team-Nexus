
# Cell 1: Imports and Function Definitions
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib
import subprocess

def speak(text):
    subprocess.run(["say", text])

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('dem63871@gmail.com', 'zwvybjfeetnpnwlp')
    server.sendmail("dem63871@gmail.com", to, content)
    server.close()

def wishMe():
    speak("Hi User! May I know your name please?")
    name = input("Your Name: ")
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning" + name + "! How may I help You?")
    elif 12 <= hour < 17:
        speak("Good Afternoon" + name +" ! How may I help You?")
    else:
        speak("Good Evening " + name + "! How may I help You?")


# Cell 2: Take Voice Command Function
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Processing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said:", query)
        return query.lower()
    except sr.UnknownValueError:
        speak("I didn't catch that. Could you please repeat?")
        return takeCommand()
    except sr.RequestError:
        speak("I'm sorry, but I couldn't request results. Please check your internet connection.")
        return "None"


# Cell 3: Wikipedia Search Function
def search_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("Here's what I found on Wikipedia")
        webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")
        speak(results)
    except wikipedia.DisambiguationError as e:
        speak("I found multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError as e:
        speak("I couldn't find any information on that topic.")


# Cell 4: Main Execution
if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand()

        if 'tell me about' in query:
            query = query.replace("tell me about ", "")
            speak('Searching ' + query)
            search_wikipedia(query)

        elif "search" in query:
            q = query.replace("search ", "")
            webbrowser.open("https://www.google.com/search?q=" + q)

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'email' in query:
            try:
                speak("Please Enter the recipient's email address.")
                to = input("Enter Email: ")  # This input statement won't work in Jupyter Notebook
                speak("What should I say?")
                content = takeCommand()
                sendEmail(to, content)
                speak(f"Email has been sent to" + to + " successfully!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email.")

        elif 'play song' in query:
            speak("Which song should I play?")
            song = takeCommand()
            webbrowser.open("https://www.youtube.com/results?search_query=" + song + "play")
            speak("Please select the first item to play the song.")

        elif 'open' in query:
            try:
                app = query.replace("open ", "")
                try:
                    subprocess.run(["open", "-a", app])
                except FileNotFoundError:
                    print(f"The application '{app}' was not found.")
            except Exception as e:
                speak("Sorry, I couldn't open that app.")

        elif 'hello' in query:
            speak("Hello there!")

        elif 'how are you' in query:
            speak("I'm great, thanks for asking!")

        elif 'who are you' in query:
            speak("I am your Genie! A genie with unlimited wishes.")

        elif 'who made you' in query:
            speak("I was made by Achintya and Gauransh. They are geniuses.")

        elif 'bye' or 'thank you' in query:
            speak("Goodbye, see you soon!")
            break
