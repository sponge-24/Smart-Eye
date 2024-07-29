import os
import cv2
from dotenv import load_dotenv
import RPi.GPIO as GPIO
from gtts import gTTS
from translate import Translator
from io import BytesIO
import pygame
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from datetime import datetime

load_dotenv()

key = os.environ.get('API_KEY')
endpoint = os.environ.get('END_POINT')
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

description = ""

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize Pygame mixer
pygame.mixer.init()

def get_greeting():
    current_hour = datetime.now().hour
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p")
    
    if 6 <= current_hour < 12:
        return f"Good morning! Today is {current_date} and the time is {current_time}."
    elif 12 <= current_hour < 18:
        return f"Good afternoon! Today is {current_date} and the time is {current_time}."
    else:
        return f"Good evening! Today is {current_date} and the time is {current_time}."
    
def greet_user():
    greeting = get_greeting()
    tts = gTTS(greeting, lang='en')
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    pygame.mixer.music.load(audio_buffer)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def capture():
        capture=cv2.VideoCapture(0)
        ret,frame=capture.read()
        frame=cv2.flip(frame,1)
        cv2.imwrite("image.jpg",frame)

def english():
    capture()
    file_path = "image.jpg"

    with open(file_path, "rb") as image_stream:
        analysis = client.describe_image_in_stream(image_stream)
        for caption in analysis.captions:
            description = caption.text
            print(caption.text)

    strObj = description
    tts = gTTS(strObj, lang='en')
    
    # Create an in-memory file-like object to store the audio data
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    pygame.mixer.music.load(audio_buffer)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def tamil():
    capture()
    file_path = "image.jpg"
    language = "en"
    max_descriptions = 3

    with open(file_path, "rb") as image_stream:
        analysis = client.describe_image_in_stream(image_stream, max_descriptions, language)
        for caption in analysis.captions:
            description = caption.text
            print(caption.text)

    translator= Translator(to_lang='ta')
    description = translator.translate(description)
    print(description)
    tts = gTTS(description, lang='ta')
    
    # Create an in-memory file-like object to store the audio data
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    pygame.mixer.music.load(audio_buffer)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def telugu():
    capture()
    file_path = "image.jpg"
    language = "en"
    max_descriptions = 3

    with open(file_path, "rb") as image_stream:
        analysis = client.describe_image_in_stream(image_stream, max_descriptions, language)
        for caption in analysis.captions:
            description = caption.text
            print(caption.text)

    translator= Translator(to_lang='te')
    description = translator.translate(description)
    print(description)
    tts = gTTS(description, lang='te')
    
    # Create an in-memory file-like object to store the audio data
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    pygame.mixer.music.load(audio_buffer)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def hindi():
    capture()
    file_path = "image.jpg"
    language = "en"
    max_descriptions = 3

    with open(file_path, "rb") as image_stream:
        analysis = client.describe_image_in_stream(image_stream, max_descriptions, language)
        for caption in analysis.captions:
            description = caption.text
            print(caption.text)

    translator= Translator(to_lang='hi')
    description = translator.translate(description)
    print(description)
    tts = gTTS(description, lang='hi')
    
    # Create an in-memory file-like object to store the audio data
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    pygame.mixer.music.load(audio_buffer)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

greet_user()
while True:
    input_state_0 = GPIO.input(23)
    input_state_1 = GPIO.input(24)
    input_state_2 = GPIO.input(22)
    input_state_3 = GPIO.input(27)
    if input_state_0 == False:
        english()
    if input_state_1 == False:
        tamil()
    if input_state_2 == False:
        telugu()
    if input_state_3 == False:
        hindi()
