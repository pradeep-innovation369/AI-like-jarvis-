import pyttsx3
import requests
import pywhatkit as kit
import speech_recognition as sr
import subprocess as sp
import pyautogui
from googletrans import Translator
import os
import wikipedia
import datetime
from langdetect import detect
from datetime import datetime
from random import choice
import time
import psutil
import pyautogui
from googlesearch import search

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

USER = ('USER')
listening = True

# Add password verification before starting the AI

def speak(text):
    engine.say(text)
    engine.runAndWait()

def play_music_from_google(song_name):
    speak(f"Searching and playing {song_name} on YouTube...")
    kit.playonyt(song_name)  # This plays the first YouTube search result for the song

def handle_music_commands(query):
    song_name = query.replace("play", "").strip()  # Clean the query to remove 'play' word

    if song_name:
        play_music_from_google(song_name)
    else:
        speak("Please tell me the name of the song you'd like to play.")
def get_word_meaning(word):
    # Use a free API for word meanings
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(api_url)
        data = response.json()

        if 'title' in data and data['title'] == 'No Definitions Found':
            return f"Sorry, I could not find the meaning for the word '{word}'."
        else:
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            return meaning
    except Exception as e:
        return f"An error occurred while fetching the meaning: {e}"
def wikipedia_search(query):
    speak(f"Searching Wikipedia for {query}...")
    print(f"Searching Wikipedia for {query}...")
    try:
        # Searching Wikipedia and getting a summary of the page
        result = wikipedia.summary(query, sentences=3)  # Limit to the first 3 sentences of the result
        print("Wikipedia Result:")
        print(result)  # Print result to terminal
        speak(result)  # Optionally, speak the result
    except wikipedia.exceptions.DisambiguationError as e:
        print("There are multiple results, try being more specific.")
        speak("There are multiple results, try being more specific.")
    except wikipedia.exceptions.HTTPTimeoutError:
        print("Request to Wikipedia timed out.")
        speak("Sorry, there was a timeout while trying to search Wikipedia.")
    except wikipedia.exceptions.RedirectError:
        print("The page has been redirected.")
        speak("The page has been redirected.")
    except wikipedia.exceptions.PageError:
        print("The page does not exist.")
        speak("Sorry, I couldn't find a page with that title.")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I encountered an error while searching Wikipedia.")
def get_word_meaning(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(api_url)
        data = response.json()

        if 'title' in data and data['title'] == 'No Definitions Found':
            return f"Sorry, I could not find the meaning for the word '{word}'."
        else:
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            return meaning
    except Exception as e:
        return f"An error occurred while fetching the meaning: {e}"

def detect_language(word):
    return detect(word)

def translate_to_english(word):
    translator = Translator()
    try:
        translated = translator.translate(word, src='auto', dest='en')
        return translated.text
    except Exception as e:
        return "Translation failed."
def open_application_via_start_menu(app_name):
    speak(f"Opening {app_name}.")
    pyautogui.hotkey('win')  # Open the Start Menu
    time.sleep(1)  # Wait for the Start menu to appear
    pyautogui.write(app_name)  # Type the app name
    time.sleep(1)  # Wait for search results to appear
    pyautogui.press('enter')  # Press Enter to open the app
    time.sleep(2)  # Give time for the app to open
def translate_text(text, target_language='en'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        translated_text = translation.text
    except Exception as e:
        print(f"Translation Error: {e}")
        translated_text = "Translation Error"
    return translated_text
def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any"  # 'Any' means it will return any type of joke.
    
    # Parameters to control the joke type
    params = {
        "type": "twopart",  # Two-part joke (setup and delivery)
        "lang": "en",       # Language set to English
    }
    
    # Send the request to JokeAPI
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        joke_data = response.json()
        
        # If it's a two-part joke
        if joke_data["type"] == "twopart":
            setup = joke_data["setup"]
            delivery = joke_data["delivery"]
            return f"{setup} ... {delivery}"
        else:
            # If it's a single-part joke
            return joke_data["joke"]
    else:
        return "Sorry, I couldn't fetch a joke at the moment."

def close_application_via_alt_f4():
    speak("Closing the application.")
    pyautogui.hotkey('alt', 'f4')  # Close the current active window
    time.sleep(1)  # Give it a moment to close

def is_application_running(app_name):
    for proc in psutil.process_iter(['name']):
        if app_name.lower() in proc.info['name'].lower():
            return True
    return False

def speak_time():
    current_time = datetime.now().strftime("%I:%M %p")  # Format: 03:14 PM
    print("Current time is:", current_time)
    engine.say("The current time is " + current_time)
    engine.runAndWait()

NEWS_API_KEY = '

def fetch_news(category):
    valid_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    
    if category not in valid_categories:
        return [f"Invalid category: {category}. Please choose a valid one."]
    
    url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    news_data = response.json()

    if news_data['status'] == 'ok' and len(news_data['articles']) > 0:
        articles = news_data['articles'][:3]  # Fetch only top 3 articles
        news = []
        for article in articles:
            title = article['title']
            description = article['description']
            news.append(f"Title: {title}. Description: {description}")
        return news
    else:
        return ["Sorry, I couldn't fetch any news. Please try again later."]

def speak_date():
    current_date = datetime.now().strftime("%B %d, %Y")  # Format: November 30, 2024
    print("Current date is:", current_date)
    engine.say("The current date is " + current_date)
    engine.runAndWait()

def speak_location():
    try:
        # Use ipinfo.io to get location info
        response = requests.get('https://ipinfo.io')
        data = response.json()

        # Extract location details
        location = data.get('city', 'Unknown City') + ', ' + data.get('region', 'Unknown Region') + ', ' + data.get('country', 'Unknown Country')
        print(f"Current location: {location}")
        
        # Speak the location
        engine.say(f"Your current location is {location}")
        engine.runAndWait()
    except Exception as e:
        print(f"Error retrieving location: {e}")
        engine.say("Sorry, I could not retrieve your location.")
        engine.runAndWait()

def speak_temperature(city):
    try:
        # Get your OpenWeatherMap API key
        api_key = ""  # Replace with your own API key
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"  # Using metric for Celsius
        
        # Make the API request
        response = requests.get(base_url)
        data = response.json()

        # Check if the response contains the weather data
        if data["cod"] == 200:
            temperature = data["main"]["temp"]  # Temperature in Celsius
            weather_description = data["weather"][0]["description"]  # Weather description
            print(f"The temperature in {city} is {temperature}°C with {weather_description}.")
            
            # Speak the temperature
            engine.say(f"The current temperature in {city} is {temperature} degrees Celsius with {weather_description}.")
            engine.runAndWait()
        else:
            engine.say(f"Sorry, I couldn't get the weather data for {city}.")
            engine.runAndWait()
    except Exception as e:
        print(f"Error retrieving temperature: {e}")
        engine.say("Sorry, I couldn't fetch the temperature right now.")
        engine.runAndWait()

def translate_text(text, target_language='en'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        translated_text = translation.text
    except Exception as e:
        print(f"Translation Error: {e}")
        translated_text = "Translation Error"
    return translated_text

def greet_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good morning bro ")
    elif 12 <= hour < 17:
        speak(f"Good afternoon pradeep")
    elif 17 <= hour < 21:
        speak(f"Good evening boss")
    else:
        speak(f"Hello dude ")

def take_command():
    global listening
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)

        if 'wake up' in query:
            speak(choice(["I'm awake and ready to assist you!", "Good to be back!", "Ready when you are!"]))
            listening = True
            greet_me()

        if "news" in query:
            speak("Which category of news would you like to hear? Business, Entertainment, Health, Science, Sports, or Technology?")
            category = take_command().lower()  # Get category input
            news = fetch_news(category)
            if news:
                speak(f"Here are the top 3 news articles in {category}:")
                for article in news:
                    speak(article)
            else:
                speak("Sorry, no news found.")

        elif "sleep" in query:
            speak(choice(["Okay, I'm going to sleep now.", "See you later!", "Rest mode activated."]))
            listening = False

        elif 'stop' in query or 'exit' in query:
            hour = datetime.now().hour
            if 21 <= hour or hour < 6:
                speak("Good night, take care!")
            else:
                speak("Have a good day!")
            exit()

    except Exception as e:
        print(e)
        query = 'None'

    return query

if __name__ == '__main__':
    
        greet_me()
        while True:
            if listening:
                query = take_command()
                if "how are you" in query:
                    speak("I am absolutely fine sir. What about you")
                if "name" in query:
                    speak("I am harar")          
                if 'can you help me' in query:
                    speak("Yes, I'm here to help you.")
                if 'who is your boss ' in query:
                    speak("pradeep is my boss")
                if 'hi' in query:
                    speak("hello , welcome")
                elif 'who created you' in query or "who made you" in query:
                    speak("I was created by Pradeep in his workshop")
                if 'let create new project' in query:
                    speak("Yes, I'm ready.")
                if 'time' in query or 'present time' in query or "what is the time" in query:
                    speak_time()
                if 'date' in query or 'what is the date' in query:
                    speak_date()  # Call the speak_date function when the query is related to the date
                if 'location' in query or 'where i am' in query or 'current location' in query or 'where am i ' in query :
                    speak_location()  # Call the speak_location function when the query is related to the location
                if 'temperature' in query or 'weather' in query or 'what is the temperature' in query:
                    speak("Please tell me the name of your city")
                    city = take_command().lower()  # Capture city name from the user
                    speak_temperature(city)  # Call the speak_temperature function with the captured city name
                if 'change your name' in query:
                    speak("sorry i can't change my name")
                elif'spell you name'in query:
                    speak("H . A . R . A . R" )     
                elif"good evening" in query:
                
                 speak("good evening sir ,on your service")
               
                elif"good morning" in query:
                    speak("good morning sir have a good day")
                elif"good afternoon" in query:
                    speak("good afternoon sir")
                elif"good night" in query:
                    speak("good night sir ,sleep well you can call me any time")
                elif 'iam fine ' in query:
                    speak("good to hear from you sir")
                elif "tell me a joke" in query:
                    joke = get_joke()
                    speak(joke)
                elif 'open' in query:
                    app_name = query.replace('open', '').strip()
                    open_application_via_start_menu(app_name)
                elif "close" in query:
                    close_application_via_alt_f4()
                elif "search" in query:
                    query = query.replace("search", "").strip()  # Remove 'search' from query
                    wikipedia_search(query)
                if "play" in query:
                    handle_music_commands(query)
                elif"mute"in query:
                    pyautogui.press("m")
                elif"unmute"in query:
                    pyautogui.press("m")
                elif"pause"in query:
                    pyautogui.press("k")
                elif"resume"in query:
                    pyautogui.press("k")
                elif "shutdown the system"in query:
                    speak("shutting down") 
                    os.system("shutdown /s /t 1")
                elif "restart the system"in query:
                    speak("restarting") 
                    os.system("shutdown /r /t 1")
                elif "translate" in query:
                 try:
                    print("Speak the text you want to translate:")
                    speak("Speak the text you want to translate:")
                    original_text = take_command()
                    print("Original Text:", original_text)

                    print("Which language would you like to translate to?")
                    speak("Which language would you like to translate to?")
                    target_language = take_command().lower()

                    print("Translating...")
                    translated_text = translate_text(original_text, target_language)
                    print(f"Translated Text ({target_language}):", translated_text)

                    print("Speaking translated text...")
                    speak(translated_text)
                 except Exception:
                    speak('Your translation failed.')
                elif "good bye" in query :
                    speak("you can call me any time ")
                    exit()
                if 'meaning of' in query or 'what is the meaning of' in query:
            # Extract the word after the phrase 'meaning of' or 'what is the meaning of'
                    if 'meaning of' in query:
                       word = query.replace('meaning of', '').strip()
                    elif 'what is the meaning of' in query:
                       word = query.replace('what is the meaning of', '').strip()

                    if word:
                       detected_language = detect_language(word)
                       print(f"Detected language: {detected_language}")
                       speak(f"Detected language: {detected_language}")

                       if detected_language != 'en':
                        word = translate_to_english(word)
                        print(f"Translating '{word}' to English...")
                        speak(f"Translating '{word}' to English...")

                       meaning = get_word_meaning(word)
                       print(f"The meaning of {word} is: {meaning}")
                       speak(f"The meaning of {word} is: {meaning}")
                    else:
                      speak("Please specify the word you want the meaning of.")

                    
