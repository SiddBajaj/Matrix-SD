import os
import random
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime

def say(text):
    """Converts text to speech and outputs it."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    print(f"\n==> Matrix AI: {text}")

def takecommand():
    """Listens to user voice input and converts it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"\n==> User: {query}")
        return query.lower()
    except:
        return ""

def play_random_music():
    """Plays a random music file from a specified directory."""
    music_dir = "C:/Users/aarav/Music"  
    music_files = [f for f in os.listdir(music_dir) if os.path.isfile(os.path.join(music_dir, f))]

    if not music_files:
        say("No music files found in the specified directory.")
        return

    random_music_file = random.choice(music_files)
    music_path = os.path.join(music_dir, random_music_file)

    try:
        os.startfile(music_path)
        say(f"Playing music: {random_music_file}")
    except Exception as e:
        say(f"Error playing music: {e}")

def main_loop():
    """Handles user commands and executes corresponding actions."""
    while True:
        query = takecommand()

        # Open websites
        sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "wikipedia": "https://www.wikipedia.org"
        }
        for site in sites:
            if f"open {site}" in query:
                say(f"Opening {site}")
                webbrowser.open(sites[site])
                return
       
        # Get the time
        if "the time" in query:
            now = datetime.datetime.now()
            formatted_time = now.strftime("%I:%M %p")
            say(f"Sir, the time is {formatted_time}")

        # Play random music
        elif "play music" in query:
            play_random_music()

        # Shutdown Assistant
        elif any(word in query for word in ["shutdown matrix", "matrix off", "exit", "quit"]):
            say("Matrix shutting down. Goodbye!")
            break

def wakeup():
    """Activates the assistant when the wake-up phrase is detected."""
    while True:
        print("Say 'Wake Up' to Activate Matrix.")
        wake_query = takecommand()

        if "wake up" in wake_query or "activate" in wake_query:
            say("Activating Matrix, Sir.")
            main_loop()
            break

if __name__ == '__main__':
    wakeup()
