import os
import re
import eel
import time
import psutil
import struct
import pyaudio
import smtplib 
import sqlite3
import requests
import speedtest
import pyautogui
import subprocess
import webbrowser
import pvporcupine
from pipes import quote
import pywhatkit as kit
from fuzzywuzzy import fuzz
from hugchat import hugchat
from datetime import datetime
from selenium import webdriver
from playsound import playsound
from engine.command import speak
from googletrans import Translator
from sketchpy import library as lib
from email.message import EmailMessage
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from engine.helper import extract_yt_term, remove_words
from selenium.webdriver.support import expected_conditions as EC
from engine.config import ASSISTANT_NAME, OPENWEATHER_APP_ID, NEWS_API_KEY, TMDB_API_KEY, EMAIL, PASSWORD




# Database Connection 
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Playing JARVIS sound 
@eel.expose
def playAssistantSound():
    '''Plays assistant's sound'''

    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

# URL, Sys App Automation
def openCommand(query):
    '''Opens user's demanded application or website 
    directly or by extracting its path from the database - jarvis.db

    NOTE - jarvis.db should be created before hand with the mentioned tables
    and entries of desired destination should be pre-entered in to tables'''

    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak(f'Opening {query}')
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak(f'Opening {query}')
                    webbrowser.open(results[0][0])

                else:
                    speak(f'Opening {query}')
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong while opening the application")

# YT Automation
def PlayYoutube(query):
    '''Search YouTube by extracting search term from user's command'''

    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube, sir")
    kit.playonyt(search_term)

# Hotword detection 'JARVIS' using pvporcupine==1.9.5
def hotword():
    '''It runs cont. in the backgorund (by multithreading) 
    detects hot word(like jarvis) spoken by the user.
    automatically press win+j to trigger siriWave for communication  '''

    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio() # init pyAudio
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length) # starting audio stream
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted or not (in our case 'jarvis')
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key: win+j automatically
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# Whatsapp Automation
def findContact(query):
    '''Find desired contacts in database - jarvis.db
    if found : returns mobile number, email, name
    else: returns 0, 0, 0'''

    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'an', 'to', 'voice', 'phone', 'call', 'email', 'mail', 'gmail', 'send', 'message', 'whatsapp', 'video', 'vc', 'open', 'and', 'please']
    query = remove_words(query, words_to_remove)  # Fetch the name only from the entire statement

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no, email FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchone()  # Use fetchone() as we expect only one result
        if results:
            mobile_number_str = str(results[0])  # Convert mobile number to string
            email_str = results[1]  # Fetch email
            if not mobile_number_str.startswith('+91'):
                # Append country code at the start (if not present)
                mobile_number_str = '+91' + mobile_number_str
            return mobile_number_str, email_str, query
        else:
            speak('not exist in contacts')
            return 0, 0, 0
    except Exception as e:
        speak(f'Error: {e}')
        return 0, 0, 0

def whatsApp(mobile_no, message, flag, name):
    '''Automate whatsApp.exe to perform tasks 
    like sending message,video calling, voice calling
    mobile_no : string contact no
    message : user's command
    flag : tasks to perform(message, phone call, video call)
    name : contact name'''

    if flag == 'message':
        target_tab = 12
        jarvis_message = f'message send successfully to {name}'

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = f'calling to {name}'

    else:
        target_tab = 6
        message = ''
        jarvis_message = f'starting video call with {name}'

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    # Automating the process 
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# Chat Bot Feature - LLM model Integration
def chatBot(query):
    user_input=query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# Time in AM/PM format 
def time_am_pm():
    '''return time in 12hrs format'''
    dt_obj = datetime.now()
    ts_am_pm = dt_obj.strftime('%I:%M %p')
    return ts_am_pm

# Date in textual format 
def format_date():
    '''if the date is 07/05/2024
    output yield : 7th May 2024'''
    
    # Get today's date
    today = datetime.now()

    # Format the date as "day month year"
    formated_date = today.strftime("%e %B %Y")

    # Add ordinal suffix to the day
    day = today.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    formated_date = formated_date.replace(str(day), str(day) + suffix)

    return formated_date

# Calendar day
def calendar_day():
        day = datetime.today().weekday() + 1
        Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',4: 'Thursday', 5: 'Friday', 6: 'Saturday',7: 'Sunday'}
        if day in Day_dict.keys():
            day_of_the_week = Day_dict[day]
        
        return day_of_the_week

# IP Address 
def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

# Weather Forecast 
def findCityName(query):
    '''This function extracts city name from user's command.
    If not found returns None'''
    # List of words to remove from the command
    words_to_remove = [ASSISTANT_NAME, "weather", "in", "what", "is", "today", "today's", "for", "the", "forecast", "temperature", "climate", "like", "my", "location", "place", "please", "condition", "report", "of"]

    city_name = remove_words(query, words_to_remove) # will fetch the city name 

    # Remove any punctuation marks or trailing spaces
    city_name = city_name.strip("?.,!")

    if len(city_name) == 0:
        return None
    
    return city_name

def get_weather_report(city):
    '''This func uses Openweathermap API to fetch 
    weather foreacast of desired location.
    Extracts and return weather, temp, feels like'''
    
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

# News Report 
def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:3]

# Random joke
def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

# Random advice 
def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']

# Movie Suggestion 
def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5] # 5 movies

# Sending Email 
def send_email(receiver_address, subject, message):
    '''Send email to the receiver address'''
    try:
        # Create an EmailMessage object
        email = EmailMessage()
        
        # Set the recipient's email address
        email['To'] = receiver_address
        
        # Set the subject of the email
        email["Subject"] = subject
        
        # Set the sender's email address
        email['From'] = EMAIL
        
        # Set the content of the email
        email.set_content(message)
        
        # Establish a connection to the Gmail SMTP server
        s = smtplib.SMTP("smtp.gmail.com", 587) # Port : 587
        
        # Start TLS (Transport Layer Security) for security
        s.starttls()
        
        # Login to the email account using the provided EMAIL and PASSWORD
        s.login(EMAIL, PASSWORD)
        
        # Send the email message
        s.send_message(email)
        
        # Close the connection to the SMTP server
        s.close()
        
        # If everything goes well, return True indicating success
        return True
    except Exception as e:
        # If there is any exception, print the error message and return False indicating failure
        print(e)
        return False 


# Drawing using turtle 
def draw(person):
    '''Drawing animation using the turtle module'''
    try:
        if person == 'rdj':
            obj = lib.rdj()
        elif person == 'ironman':
            obj = lib.ironman_ascii()
        elif person == 'tom holland':
            obj = lib.tom_holland()
        elif person == 'vijay':
            obj = lib.vijay()
        elif person == 'bts':
            obj = lib.bts()
        obj.draw()
    except Exception as e:
        print(e)
        
# Computer Performance Stats 
def get_pc_stats():
    '''Returns CPU usage, RAM usage, GPU temp. and usage'''
    
    # CPU Usage 
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_Ghz = psutil.cpu_freq().current / 1000
    
    # RAM Usage 
    mem = psutil.virtual_memory()
    used_mem = mem.used / (1024**3)  # Convert bytes to GB
    total_mem = mem.total / (1024**3)  # Convert bytes to GB
    mem_usage_percentage = mem.percent
    
    # GPU Usage 
    try:
        # NOTE : This will only work for NVIDIA GPUs using nvidia-smi.
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=utilization.gpu,temperature.gpu', '--format=csv,noheader,nounits'])
        gpu_info = output.decode('utf-8').strip().split('\n')
        gpu_usage = int(gpu_info[0].split(',')[0])
        gpu_temp = int(gpu_info[0].split(',')[1])
    except Exception as e:
        gpu_usage = None
        gpu_temp = None
    
    return cpu_usage, cpu_Ghz, used_mem, total_mem, mem_usage_percentage, gpu_usage, gpu_temp

# Translate Lang
def extract_source_and_destination(query):
    """
    Extract source text and destination language from the query.

    Args:
        query (str): The input query.

    Returns:
        tuple: Tuple containing source text and destination language.
    """
    # Define regex pattern to match "translate" followed by the source text and "to" or "in" followed by destination language
    pattern = r"^translate\s+(.*?)\s+(to|in)\s+(\w+)$"

    # Find all matches of the pattern in the query
    match = re.match(pattern, query)

    # Extract source text and destination language
    if match:
        source_text = match.group(1) # \s+(.*?)
        destination_language = match.group(3) # \s+(\w+)
    else:
        source_text = None
        destination_language = None

    return source_text, destination_language

def translate_text(input_query):
    """
    Translate text from source language to destination language.

    Args:
        input_query (str): The input query containing the text and optionally the destination language.

    Returns:
        str: Translated text.
    """
    translator = Translator()

    # Extract source text and destination language from the input query
    source_text, destination_language = extract_source_and_destination(input_query)

    # Detect the source language of the text
    source_language = translator.detect(source_text).lang

    # Translate the text to the detected source language and auto-adjust destination language
    translated_text = translator.translate(source_text, src=source_language, dest=destination_language)

    return f'{source_text} in {destination_language} is "{translated_text.text}"'

# Internet Speed 
def get_internet_speed():
    st = speedtest.Speedtest()

    # Get best server based on ping
    st.get_best_server()

    # Perform download and upload speed tests
    download_speed = st.download()
    upload_speed = st.upload()

    # Convert the speed from bits per second to megabytes per second
    download_speed_mbps = download_speed / 1e6  # Convert to Megabits
    upload_speed_mbps = upload_speed / 1e6  # Convert to Megabits

    return f'{download_speed_mbps:.2f}', f'{upload_speed_mbps:.2f}'


# Music Playback 
def match_query_with_url(query, title):
    # Extract song name and artist from the query using regular expression
    match = re.match(r'^play\s+(.+?)(?:\s+by\s+(.+))?$', query)
    if match:
        song_name = match.group(1)
        artist_name = match.group(2) if match.group(2) else ""
                    
        # Check if the song name and artist name are present in the title with some fuzziness
        if fuzz.partial_ratio(song_name, title) >= 70:
            return True
    return False



def control_music(driver, action):
    try:
        if 'pause' in action:
            # Find the pause button and click if it's available
            pause_button = driver.find_element(By.XPATH, "//button[@data-testid='playerPause']")
            pause_button.click()
            print("Music paused.")
            speak("Music paused.")
        elif 'resume' in action:
            # Find the play button and click if it's available
            play_button = driver.find_element(By.XPATH, "//button[@data-testid='playerPlay']")
            play_button.click()
            print("Music resumed.")
            speak("Music resumed.")
        elif'previous' in action:
            # Find the previous button and click if it's available
            prev_button = driver.find_element(By.XPATH, "//i[@data-testid='playerPrev']")
            prev_button.click()
            print("Previous song played.")
            speak("Previous song played.")
        elif 'next'in action:
            # Find the next button and click if it's available
            next_button = driver.find_element(By.XPATH, "//i[@data-testid='playerNext']")
            next_button.click()
            print("Next song played.")
            speak("Next song played.")
        # elif 'repeat'in action:
        #     # Find the repeat button and click if it's available
        #     repeat_button = driver.find_element(By.XPATH, "//div[@class='hidden sm:block']//button[@data-testid='playerRepeat']")
        #     repeat_button.click()
        #     print("Repeat toggled.")
        #     speak("Repeat toggled.")

            
    except Exception as e:
        print("Action failed:", e)
        speak("Action failed.")

def play_song(song_query):
    try:
        # Initialize the Chrome WebDriver
        s = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode
        driver = webdriver.Chrome(service=s, options=options)

        # Open a new browser window
        driver.get("https://wynk.in/music/search")

        # Wait for the search input element to become visible and interactable
        search_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/header/section/div[2]/a/div/input')))

        # Once the element is interactable, send keys
        search_field.send_keys(song_query)

        # Print a message indicating that the query has been entered
        print("Search query entered:", song_query)
        # speak("Search query entered.")

        # Wait for the search results to load
        driver.implicitly_wait(10)

        # Find the elements containing the song information
        elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'zapSearch_zapSearchItem')]")

        # Loop through the first five elements and check if the song title matches the query
        for element in elements[:3]:
            song_title = element.get_attribute("title")
            song_url = element.get_attribute("href")

            # Check if the song title matches the query
            if match_query_with_url(song_query, song_title):
                # Print song details
                print("Song Title:", song_title)
                print("Song URL:", song_url)
                speak(f"Now playing {song_title}.")
                # Play the song
                element.click()
                # Add a delay to allow time for the song to start playing
                time.sleep(5)  # You can adjust the delay as needed

                return driver  # Return the driver instance

        return driver  # Return the driver instance if no song found
    
    except Exception as e:
        print("Error occurred while playing the song:", e)
        speak("Error occurred while playing the song.")
        
        
        
        