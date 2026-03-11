import datetime
import json
import os
import random as rm
import re
import smtplib
import time
import webbrowser
from typing import List

import psutil
import pyttsx3
import requests
import speech_recognition as sr
import wikipedia
from playsound import playsound


NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
SENDER_EMAIL = os.getenv("JARVIS_EMAIL", "")
SENDER_PASSWORD = os.getenv("JARVIS_EMAIL_PASSWORD", "")
FLIP_SOUND_PATH = os.getenv("JARVIS_FLIP_SOUND", "")


def setup_engine() -> pyttsx3.Engine:
    """Initialize speech engine and choose a default voice."""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 180)
    return engine


engine = setup_engine()


def speak(audio: str) -> None:
    engine.say(audio)
    engine.runAndWait()


# This function checks the cpu usage and returns true if the usage is less than 75%.
def check_cpu_usage() -> bool:
    usage = psutil.cpu_percent(interval=1)
    return usage < 75


def send_email(to: str, content: str) -> bool:
    """Send an email using Gmail SMTP credentials from env variables."""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        speak("Email is not configured yet. Please set email credentials in environment variables.")
        return False

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to, content)
    return True


# This function reads the newspaper headlines
def read_news() -> None:
    if not NEWS_API_KEY:
        speak("News API key is missing. Please add NEWS_API_KEY environment variable.")
        return

    speak("Today's business headlines are")
    url = (
        "https://newsapi.org/v2/top-headlines?country=us"
        f"&category=business&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        news = json.loads(response.text)
        articles = news.get("articles", [])

        if not articles:
            speak("Sorry, I could not find headlines right now.")
            return

        for article in articles[:10]:
            title = article.get("title")
            if title:
                speak(title)
                speak("Next headline")
                time.sleep(0.5)
    except requests.RequestException:
        speak("Unable to fetch the news right now.")


def flip_coin() -> None:
    coin = rm.choice(["heads", "tails"])
    if FLIP_SOUND_PATH and os.path.exists(FLIP_SOUND_PATH):
        playsound(FLIP_SOUND_PATH)
    speak(f"It is {coin}")


def wish_me() -> None:
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Please tell me how may I help you")


# This function extracts all numbers from a string
def find_number(string: str) -> List[int]:
    temp = re.findall(r"\d+", string)
    return list(map(int, temp))


def take_command() -> str:
    """Take microphone input from user and return string output."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
        return query
    except Exception:
        print("Say that again please...")
        return ""


def handle_query(query: str) -> bool:
    """Process one user command. Returns False when assistant should stop."""
    query = query.lower().strip()
    if not query:
        return True

    if "wikipedia" in query:
        speak("Searching Wikipedia")
        topic = query.replace("wikipedia", "").strip()
        if topic:
            try:
                results = wikipedia.summary(topic, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception:
                speak("Sorry, I could not find that on Wikipedia.")
        else:
            speak("Please tell me what to search on Wikipedia.")

    elif "open youtube" in query:
        webbrowser.open("https://youtube.com")

    elif "open google" in query:
        webbrowser.open("https://google.com")

    elif "open hackerrank" in query:
        webbrowser.open("https://hackerrank.com")

    elif "open stackoverflow" in query:
        webbrowser.open("https://stackoverflow.com")

    elif "open gmail" in query:
        webbrowser.open("https://gmail.com")

    elif "send email" in query:
        try:
            speak("Who should I send it to?")
            to = take_command()
            speak("What should I say?")
            content = take_command()
            if to and content and send_email(to, content):
                speak("Your email has been sent")
            else:
                speak("I could not send the email")
        except Exception:
            print("Sorry, I could not send email")

    elif "the time" in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")
        print(f"The time is {str_time}")

    elif "open vs code" in query:
        code_path = "C:\\Users\\saket\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        if os.path.exists(code_path):
            os.startfile(code_path)
        else:
            speak("Visual Studio Code path is not configured on this machine.")

    elif "check cpu usage" in query:
        if check_cpu_usage():
            speak("Everything is fine. CPU usage is less than 75 percent")
        else:
            speak("CPU usage is more than 75 percent")

    elif "today's headlines" in query or "todays headlines" in query:
        read_news()

    elif "add" in query:
        numbers = find_number(query)
        if numbers:
            speak(f"The result is {sum(numbers)}")
        else:
            speak("Please provide numbers to add")

    elif "wait" in query:
        durations = find_number(query)
        total_wait = sum(durations)
        if total_wait > 0:
            speak(f"Waiting for {total_wait} seconds")
            time.sleep(total_wait)
        else:
            speak("Please tell me the wait time in seconds")

    elif any(phrase in query for phrase in ["quit", "exit", "jarvis shutdown"]):
        speak("Shutting down. Goodbye")
        return False

    elif any(phrase in query for phrase in ["toss a coin", "flip a coin"]):
        flip_coin()

    return True


def main() -> None:
    wish_me()
    while True:
        if not handle_query(take_command()):
            break


if __name__ == "__main__":
    main()
