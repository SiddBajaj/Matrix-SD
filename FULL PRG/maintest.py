import os
import random
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import subprocess
from config import YOUR_API_KEY
import google.generativeai as genai
import importlib
import sys
from time import sleep

driver = None
directory_path = "D:/MATRIX final submit/gemini/" 


def check_and_install_libraries(required_libraries):
    missing_libraries = []
    for library in required_libraries:
        try:
            importlib.import_module(library)
        except ImportError:
            missing_libraries.append(library)

    if missing_libraries:
        print(f"The following libraries are required but not installed: {', '.join(missing_libraries)}")
        try:
            subprocess.run(["pip", "install"] + missing_libraries, check=True)
            print("Successfully installed missing libraries.")
            return True
        except subprocess.CalledProcessError:
            print("Error installing libraries using pip. Please install them manually.")
            return False
    else:
        return True


# List of required libraries for the code
required_libraries = [
    "speech_recognition",
    "pyttsx3",
    "webbrowser",
    "datetime",
    "os",
    "random",
    "config",
    "google.generativeai"
]

if not check_and_install_libraries(required_libraries):
    print("Failed to install required libraries. Please install them manually and restart the script.")
    sys.exit(1)


def remove_special_chars(text):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _~`!$%^,.+={[]}|<>?()\\-:/'")
    return ''.join([char for char in text if char in allowed_chars or char.isspace()])


def say(text):
    engine = pyttsx3.init()
    Id = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enUS_MarkM'
    engine.setProperty('voice', Id)
    engine.setProperty('rate', 175)  # Set the speech rate (default is usually around 200)
    filtered_text = remove_special_chars(text)  # Remove special characters
    print(f"\n==> Matrix AI: {filtered_text}")
    engine.say(text=filtered_text)
    engine.runAndWait()
    return filtered_text


def speak(text):
    engine = pyttsx3.init()
    Id = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    engine.setProperty('voice', Id)
    engine.setProperty('rate', 178)  # Set the speech rate (default is usually around 200)
    print("")
    engine.say(text=text)
    engine.runAndWait()




def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=1, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            return ""

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"\n==> Aarav: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def play_random_music():
    music_dir = "C:/Users/aarav/Music"  # Replace with your actual music directory
    music_files = [f for f in os.listdir(music_dir) if os.path.isfile(os.path.join(music_dir, f))]

    if not music_files:
        print("No music files found in the specified directory.")
        return

    random_music_file = random.choice(music_files)
    music_path = os.path.join(music_dir, random_music_file)

    try:
        os.startfile(music_path)
    except Exception as e:
        print(f"Error playing music: {e}")


def ai(prompt):
    genai.configure(api_key=YOUR_API_KEY)

    generation_config = {
        "temperature": 1.0, 
        "top_p": 0.95,  
        "max_output_tokens": 8192, 
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    response = convo.last.text
    first_sentence = response.split(". ")[0]
    query_words = prompt.lower().split()
    if any(word in ["who", "what", "why", "explain"] for word in query_words):
        random_prompts = [
            "Let me explain that for you:",
            "Here's what I can tell you:",
            "Alright, here are the details:",
            "Sure, let me share some information:",
        ]
    elif any(word in ["how", "steps", "process"] for word in query_words):
        random_prompts = [
            "Here's how you can do that:",
            "Let me guide you through the process:",
            "Okay, follow these steps:",
            "Sure, the way to do that is:",
        ]
    else:
        random_prompts = [
            "Here you go:",
            "Let me tell you about that:",
            "Alright, here's what I know:",
            "Sure, let me share some information:",
        ]
    random_prompt = random.choice(random_prompts)
    say(f"{random_prompt} \n\n {first_sentence}.")
    print(convo.last.text)
    random_prompt = random.choice(random_prompts)
    base_filename = "prompt "
    file_extension = ".txt"
    target_dir = directory_path
    counter = 1
    filename = os.path.join(target_dir, f"{base_filename}{counter}{file_extension}")
    while os.path.exists(filename):
        counter += 1
        filename = os.path.join(target_dir, f"{base_filename}{counter}{file_extension}")

    with open(filename, "w") as f:
        f.write(f"Sir, {random_prompt} \n\n {convo.last.text}.")
        say(f"\n\n\nPrompt Result saved as : {base_filename}{counter}{file_extension}")


def wakeup():
    while True:
        print("Say 'Wake Up' or 'Activate' to Activate Matrix.")
        wake_query = takecommand()
        if "wake up" in wake_query.lower() or "activate" in wake_query.lower():
            speak("Activating Matrix, Sir.")
            say("Hello Aarav Sir, I am Matrix!")
            main_loop()
            break


def main_loop():
    while True:
        query = takecommand()
        sites = [
            ["youtube", "youtube.com"],
            ["wikipedia", "wikipedia.org"],
            ["google", "google.co.in"],
            ["whatsapp", "web.whatsapp.com"],
            ["vtop", "vtop.vit.ac.in"],
            ["v top", "vtop.vit.ac.in"],
            ["vit website", "vtop.vit.ac.in"],
        ]
        keywords = ["how",
                    "steps",
                    "process",
                    "who",
                    "why",
                    "explain",
                    "tell me",
                    "who is",
                    "why is",
                    "explain",
                    "when",
                    "where",
                    "what",
                    "how to",
                    "how do i"
                    ]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening, {site[0]} sir")
                webbrowser.open(site[1])
        if "the time" in query:
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute
            if hour >= 12:
                meridian = "PM"
                hour = hour - 12
            else:
                meridian = "AM"
            formatted_time = f"{hour:02d}:{minute:02d} {meridian}"
            say(f"Sir, the time is {formatted_time}")
        elif "play random music".lower() in query.lower():
            play_random_music()
        elif any(keyword.lower() in query.lower() for keyword in keywords):
            ai(prompt=query)
        elif "open prompt" in query.lower():
            file_number = query.split("open prompt", 1)[-1].strip()
            file_name = f"prompt {file_number}.txt"
            full_file_path = os.path.join(directory_path, file_name)
            try:
                subprocess.Popen(["notepad.exe", full_file_path])
                say("Opening the file, sir")
            except:
                return ""
        elif any(word in query.lower() for word in
                  ["matrix deactivate", "deactivate matrix", "shutdown matrix", "matrix shutdown", "kill matrix", ]):
            goodbye_messages = [
                "Deactivating Matrix, Goodbye!",
                "Matrix offline. Farewell!",
                "Until next time, Matrix is offline!",
                "Goodbye! Matrix signing off.",
                "Matrix deactivated. See you later!",
                "Farewell! Matrix going offline."
            ]
            random_goodbye = random.choice(goodbye_messages)
            say(random_goodbye)
            break


if __name__ == '__main__':
    wakeup()
    main_loop()
