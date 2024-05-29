
## Title
**J.A.R.V.I.S** - JUST A RATHER VERY INTELLIGENT SYSTEM inspired by Tony Stark's IRONMAN from the MCU
# Description

In this project I've created a virtual desktop voice assistant 'JARVIS', which has been creatd by using **python** as the scripting language. **HTML**, **CSS**, **jS** as the front-end part. And **SqLite3** as the database.

Currently I've implemented:
```
1. User Login using face recognition
2. Advance GUI using HTML, CSS & jS
3. Provided 25+ features to JARVIS.
```


## Features

    1.	Face Recognition for authentication
    2.	WhatsApp automation
    3.	Email generation & sending
    4.	System app opening & closing automation
    5.	Website opening and closing automation
    6.	YouTube Search automation
    7.	Wikipedia search
    8.	Translation
    9.	Media playback (using web automation)
    10.	Weather forecast
    11.	Trending movies suggestion
    12.	Current headlines
    13.	Take note & remember it
    14.	Take screenshot 
    15.	LLM model integration
    16.	Drawing using turtle
    17.	Internet speed check
    18.	Computer performance stats
    19.	Current day & date
    20.	Current time

## Visuals

## UI
![Hood](https://photos.app.goo.gl/YxyfRBiKsKg6cLYq9)

## Project Directory Structure 🌲

```
├── .env
├── .gitignore
├── engine
│   ├── command.py
│   ├── config.py
│   ├── cookies.json
│   ├── db.py
│   ├── features.py
│   └── helper.py
├── jarvis.db
├── main.py
├── requirements.txt
├── run.py
├── run_with_login.py
├── tree.py
├── user_authentication
│   ├── face_recognition.py
│   ├── haarcascade_frontalface_default.xml
│   ├── model trainer.py
│   ├── sample generator.py
│   ├── samples
│   │   └── face.1.1.jpg
│   └── trainer
│       └── trainer.yml
└── www
    ├── assets
    │   ├── audio
    │   │   └── start_sound.mp3
    │   ├── img
    │   │   ├── ironman.ico
    │   │   └── jarvis logo.ico
    │   └── vendore
    │       └── textillate
    │           ├── animate.css
    │           ├── jquery.fittext.js
    │           ├── jquery.lettering.js
    │           └── style.css
    ├── controller.js
    ├── index.html
    ├── main.js
    ├── script.js
    └── style.css

```
## API Keys 🔑

    1. Open Weather: https://openweathermap.org/
    2. NEWS API: https://newsapi.org/
    3. The Movies Database(TMDB) : https://www.themoviedb.org/
## Installation 💻

- You need to first ```fork``` this repository and ```clone``` the repository to your local system 

    ```
    $ git clone https://github.com/<your-github-username>/J.A.R.V.I.S.git
    ```
- Create a ```virtual enviroment```, for convinence i'm naming the env as ```envjarvis```
    ```
    $ python –m venv envjarvis
    ```

- Make sure to install all the required python modules mentioned above or you can simply install them by 

    ```
    $ pip install -r requirements.txt
    ```

- Create an ```enviroment variable``` .env file in the root directory

    ```
    ASSISTANT_NAME = "Jarvis"
    EMAIL = "None"
    PASSWORD = "None"
    OPENWEATHER_APP_ID = "None"
    NEWS_API_KEY = "None"
    TMDB_API_KEY = "None"
    ```
    NOTE: Replace None with your credentials

- Inegrate Hugging Face cookies for login
    ```
    1. Create an account on https://huggingface.co/
    2. Install Cookie-Editor chrome extension in your edge browser
    3. Login in to Hugging Face 
    4. Copy login cookies
    5. Create a cookie.json inside 'engine' folder
    6. Paste login cookies into cookies.json

    ```
- Training model for face recognition
    ```
    Go to user_authentication folder:
        Taking Facial Samples-
            - Run sample generator.py 
            - Assign unique ID for each person starting from 1
            - Look at the webcam for face samples 
        
        Training Model-
            - Run model trainer.py
            - It generates trainer.yml under trainer folder 
        
    ```