import pyautogui as auto
import speech_recognition as sr
import win32com.client as voice
import webbrowser
import os
import datetime
import google.generativeai as genai
import logging
import random
import pywhatkit as kit
import requests
import json
import time
import asyncio
import random

def ai(prompt):
    
    
    genai.configure(api_key="AIzaSyD67fjOt_IrXQuTlSF0QzcwFzCCHswrPL4")

    # text = f"AI response for Prompt :{prompt} \n ************* \n\n"
    
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }
    try:
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
    except ValueError as e:
        print("Ai misheard your voice, say again")

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    
    prompt_parts = [prompt]

    response = model.generate_content(prompt_parts)
    print(response.text)
    # say(response.text)
    # text += response.text

    # if not os.path.exists("AI"):
    #     os.mkdir("AI")

    # with open(f"F:/AI/{prompt[0:10]}.txt", "w") as f:
    #     f.write(text)

def chat(query):
    global chat_str
    if 'chat_str' not in globals():
        chat_str = ""
    genai.configure(api_key="AIzaSyD67fjOt_IrXQuTlSF0QzcwFzCCHswrPL4")

    try:
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        query_without_asterisks = query.replace("*", "")
    
        # Check if the query without asterisks is empty
        if not query_without_asterisks.strip():
            say("Please provide a valid query.")
            return

        chat_str += f"{query_without_asterisks}\n"

        prompt = chat_str

        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            # model_name="gemini-1.5-pro",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
            
        prompt = f"Aliyas: {prompt}\nDante: "

        response = model.generate_content(prompt)
        chat_str += f"{response.text}\n"

        if response and response.text:
            # Remove asterisks from the response before speaking
            response_text_without_asterisks = response.text.replace("*", "")
            print(response_text_without_asterisks)
            say(response_text_without_asterisks)
        else:
            print("The response was blocked due to safety concerns.")
            say("Sorry, I cannot provide a response for that due to safety concerns.")

    except ValueError as e:
        print(f"An error occurred: {e}")
    # say(response.text)

def say(text):
    speaker = voice.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)
    
def play_on_youtube(video):
    kit.playonyt(video)

def screenshot():
    kit.take_screenshot()

def search_on_google(query):
    kit.search(query)

async def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.5
        # r.non_speaking_duration = 0.1
        audio = r.listen(source)
        
        
        
        try:
            query = await asyncio.to_thread(r.recognize_google, audio) 
            # query = r.recognize_google(audio) 
            
            print(f"User said: {query}")
            return query
            
        except sr.UnknownValueError:
            # No speech detected
            print("No speech detected.")
            return ""
           
            
        except sr.RequestError as e:
            error_message = f"Recognition connection failed: Please check your internet connection and try again later."
            logging.error(error_message)
            say(error_message)
            return False
        
def play_music(music_folder):

    music_files = os.listdir(music_folder)
    
    music_files = [file for file in music_files if file.endswith('.mp3') or file.endswith('.wav')]

    if music_files:
        music_file = random.choice(music_files)
        music_path = os.path.join(music_folder, music_file)
        os.startfile(music_path)
        return True
    else:
        return False

async def weather(api_key, query):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        country = data['sys']['country']

        weather_info = (
            f"Weather in {query}, {country}:\n"
            f"Description: {weather_description}\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

        print(weather_info)  # Print weather info to console
        say("here's the weather reports sir")
        say(weather_info)    # Speak weather info
        say("do you want anything else?")
        
    else:
        error_message = "Failed to fetch weather information."
        print(error_message)  # Print error message to console
        say(error_message)    # Speak error message
api_key = "a72621f1af436dc2df8bf9c917c8f1c7"


async def News(query):
    
    today = time.strftime("%Y-%M-%D")

    url = f"https://newsapi.org/v2/everything?q={query}&from={today}&sortBy=publishedAt&apiKey=7372e7bba2a04aea97e51090acc7a08d"
    r = requests.get(url)
    
    news = json.loads(r.text)
    if 'articles' in news:
        for article in news['articles']:
            print(article.get("source", {}).get("name"))
            print(article.get("title"))
            print(article.get("description"))
            print(article.get("content"))
            print("____________________________________________________________________________________________________________")
    
    else:
        print(f"Failed to fetch news. Status code: {r.status_code}")
        print(r.text)
        
async def functions():
    task = asyncio.create_task(News(query))

    await asyncio.gather(task)

def open_website(query):
    website_name = query.replace("open ", "").strip().lower()
    url = f"https://{website_name}.com"
    webbrowser.open(url)


if __name__ == "__main__":
        
    say("welcomeback,sir!, How may I assist you today?")
    
    while True:
        
        print("Listening...")
        query = asyncio.run(takecommand())
        
        # query = takecommand()
        if not query:
            continue
        action_executed = False

        if query.lower().startswith("open"):
                site_name = query.replace("open ", "").strip().lower()

                open_website(query)  
                say(f"opening {site_name.capitalize()}, sir")
                continue

        elif query.lower().startswith("close "):
            # Get the list of open window titles
            open_windows = auto.getAllTitles()
            site_name = query.replace("close ", "").strip().lower()
            # Check if the site's name is present in any of the open window titles
            site_window_open = any(site_name in window_title.lower() for window_title in open_windows)
            if site_window_open:
                say(f"closing {site_name.capitalize()} Sir...")
                auto.hotkey('ctrl', 'f4')
            else:
                say(f"Sorry, but I don't see {site_name.capitalize()} open.")
            action_executed = True
            continue

        # sites = [
        #     ["YouTube", "https://youtube.com"],
        #     ["spotify", "https://spotify.com"],
        #     ["google", "https://google.com"],
        #     ["wikipedia", "https://www.wikipedia.org"],
        #     ["my Drive", "https://drive.google.com/drive/my-drive"]
        # ]
        
        # for site in sites:
        #     if f"open {site[0]}".lower() in query.lower():
        #         say(f"opening {site[0]} Sir...")
        #         webbrowser.open(site[1])
        #         action_executed = True
        #         break
       

        #     elif f"close {site[0]}".lower() in query.lower():
        #         # Get the list of open window titles
        #         open_windows = auto.getAllTitles()
        #         site_name = site[0].lower()
        #         # Check if the site's name is present in any of the open window titles
        #         site_window_open = any(site_name in window_title.lower() for window_title in open_windows)
        #         if site_window_open:
        #             say(f"closing {site[0]} Sir...")
        #             auto.hotkey('ctrl', 'f4')

        #         else:
        #             say(f"Sorry, but I don't see {site[0]} open.")
        #         action_executed = True
        #         break
           
        elif "pause video" in query.lower():
            open_windows = auto.getAllTitles()
            site_name = "youtube"
            site_window_open = any(site_name in window_title.lower() for window_title in open_windows)
            if site_window_open:
                say("pausing video sir")
                auto.hotkey("k")
            else:
                say("There is no YouTube video to pause.")
            action_executed = True
            continue
        
        elif "play video" in query.lower():
            open_windows = auto.getAllTitles()
            site_name = "youtube"
            site_window_open = any(site_name in window_title.lower() for window_title in open_windows)
            if site_window_open:
                say("playing video sir")
                auto.hotkey("k")
            else:
                say("There is no YouTube video to play.")
            action_executed = True
            continue

        if not action_executed:

            if "hey dante" == query.lower():
                say("hey sir! How can I help you today")
                continue

            elif "open music" in query:
                musicpath = "F:/MUZÏK"
                say("opening music sir!")
                os.startfile(musicpath)
                continue
            
            elif 'search youtube' in query.lower():
                say('What do you want to play on Youtube, sir?')
                video_query = asyncio.run(takecommand()).lower()
                
                play_on_youtube(video_query)
                continue

            elif 'search on google' in query.lower():
                say('What do you want to search on Google, sir?')
                search_query = asyncio.run(takecommand()).lower()
                search_on_google(search_query)
                continue

            elif 'news' in query.lower():
                say("what news would you like to hear")
                query =asyncio.run(takecommand()).lower()
                
                asyncio.run(functions())
                continue
            
            elif 'weather' in query.lower():
                say("Which city's weather do you need, sir?")
                query =asyncio.run(takecommand()).lower()
                asyncio.run(weather(api_key, query))
                
                continue
        
            elif 'minimize' in query.lower() or 'minimise' in query.lower():
                
                auto.hotkey('win', 'm')
                say('minimizing the current window sir')
                continue
                
            elif "play music" in query.lower() or "play some music" in query.lower():
                music_folder = "F:/MUZÏK"
                say("Playing music, sir!")
                play_music(music_folder)
                continue
            
            if "stop music" in query.lower() or "close music" in query.lower():

               # Get the list of open window titles
                music_open_windows = auto.getAllTitles()

                # Check if the music player's name is present in any of the open window titles
                music_player_name = "media player".lower()

                music_player_window_open = any(music_player_name in window_title.lower() for window_title in music_open_windows)

                if music_player_window_open:
                    # Close the music player
                    say("stopping music, sir!")
                    auto.hotkey('alt', 'f4')
                
                else:

                    say("Sorry, but I don't see the music player open.")

                continue

            elif "screenshot" in query.lower() or " screen shot" in query.lower() or "take a screenshot" in query.lower():
                say("taking screenshot, sir")
                screenshot()
                continue

            elif "introduce yourself" in query.lower() or "who are you" in query.lower() or "what's your name" in query.lower():
                lst = ["hello! My name is Dante, and I am an AI assistant trained by Aliyas. I can accomplish simple things because I'm still in the development phase.", "hey, im Dante", "Dante here", "sir did you forget you made me"]
                # say("hello! My name is Dante, and I am an AI assistant trained by Aliyas. I can accomplish simple things because I'm still in the development phase.")
                say(random.choice(lst))
                continue


            elif "the time" in query:
                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%I:%M:%S %p")
                say(f"The time is {formatted_time}")
                continue

            elif "Artificial intelligence".lower() in query.lower():
                ai(prompt=query)
                continue

            elif "shutdown" in query.lower() or "shut down" in query.lower():
                say("Shutting down, have a good day ali")
                break
            
            elif "dante stop".lower() in query.lower():
                exit()
            
                
            elif "reset chat".lower() in query.lower():
                chat_str = ""

            else:                    
                chat(query)