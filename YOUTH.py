import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import cv2
import requests
import wikipedia
import pyjokes 
import time
import pywhatkit as kit
import socket
import urllib.request
import pyautogui
import json
from pywikihow import search_wikihow
import sys
from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
# import smtplib


flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
engine=pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold =1
        audio = r.listen(source)
        
    try:
      print("recognizing ... ")
      query=r.recognize_google(audio,language="en-in")
      print(f"User said: {query}\n")
    except Exception as e:
        speak(f"something wrong {e}")
        speak("say that again")
        return None
    return query      

def wish():
    hour=int(datetime.datetime.now().hour)
    if hour >=0 and hour<12:
        speak("Good morning sir ,")
    elif hour>=12 and hour<18:
        speak("Good afternoon boss")
    else:
        speak("good evening Boss ")
    speak("i am Youth, how can i help you ?")

def sys_task(query):
    if "shutdown system" in query:
        os.system("shutdown /s /t 5")
    elif "restart system" in query:
        os.system("shutdown /r /t 5")
    elif 'system sleep' in query:
        os.system("Rundll32.exe Powrprof.dll,SetSuspendState Sleep")

def news():
    query_params = {
      "source": "bbc-news",
      "sortBy": "top",
      "apiKey": "8335639d50c24caeb24d19e86dc879b5"
    }
    main_url = " https://newsapi.org/v1/articles"
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()
    article = open_bbc_page["articles"]
    results = []
     
    for ar in article:
        results.append(ar["title"])
         
    for i in range(len(results)):
         
        print(i + 1, results[i])
    from win32com.client import Dispatch
    speak = Dispatch("SAPI.Spvoice")
    speak.Speak(results)                 
 
def location_track():       
    speak("sir wait, let me check ")
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        with urllib.request.urlopen("https://geolocation-db.com/json") as url:
            data = json.loads(url.read().decode())
            country=data['country_name']
            city =data["city"]
            speak(f"sir a i am not sure but you are in {city},  in {country}")

    except Exception as e:
        speak("sorry sir i am not able to find loacation due to network issue")
        print(e)
    
def tkscreenshot():
    speak("sir, tell me the name for the screenshot file")
    name=takeCommand().lower()
    speak("sir, please hold for few second , i am taking screen shot ")
    time.sleep(3)
    img=pyautogui.screenshot()
    img.save(f"{name}.png")
    speak("sir ,it's done screenshot is saved saved in default screenshot folder.")

    
    
    

class mainT(QThread):
    def __init__(self):
        super(mainT,self).__init__()
       
    def run(self):
        wish()
        self.Operation()

    def Operation(self):
     
     while True:
        try: 
         if 1:
            self.query=takeCommand()
            
                
            if "time" in self.query:
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                speak(f"Sir time is {hour} hour {min} minutes")
                
            elif "how to" in self.query:
                try:
                    speak("searching ")
                    maxr=1
                    how_to=search_wikihow(self.query,maxr)
                    assert len(how_to)==1
                    speak(how_to[0].summary)
                except:
                    speak("some problem is occured , plase say that again ...")
                
            
            elif "open camera" in self.query: 
                speak("opening camera")       
                cap=cv2.VideoCapture(0)
                while True:
                    ret,img=cap.read()
                    cv2.imshow('webcam',img)
                    k=cv2.waitKey(50)
                    if k == 27:
                     break
                cap.release()
                cv2.destroyAllWindows()
                
            elif "ip address" in self.query.lower():
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                speak(f"Your IP address is: {ip_address}")
                
            elif "wikipedia" in self.query.lower():
                try:
                    speak("searching on wikipedia ")
                    results = wikipedia.summary(self.query, sentences=2)
                    speak(f"According to Wikipedia {results}")
                except Exception:
                    speak("sorry sir , ")
            
            elif "play" in self.query.lower():
                # speak("what you want to play")
                # self.query=takeCommand()
                kit.playonyt(self.query)
                
            elif "joke" in self.query.lower():
                joke=pyjokes.get_joke()
                speak(f"{joke}")
            
            elif "news" in self.query:
                news()
            
            elif "location" in self.query:
                location_track()
                
            elif "shutdown system" in self.query or "restart system" in self.query or "system sleep" in self.query:
                sys_task(self.query)
            
            elif "take a screenshot" in self.query:
                tkscreenshot()
            
            elif "shut up" in self.query or "now you can sleep" in self.query or "bye" in self.query:
                speak("ok")
                if "bye" in self.query:
                    speak("bye sir ...")
                exit()
            
            else:
                if "open" in self.query:
                    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],["gemini","https://gemini.google.com/app"],["whatsapp","https://web.whatsapp.com"]]
                    for site in sites:
                        if f"Open {site[0]}".lower() in self.query.lower():
                            speak(f"Opening {site[0]} sir...")
                            webbrowser.open(site[1])
                    
                    apps = [["code", "C:\\Users\\prabh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"] , ["chrome","C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"] ,["command","C:\\WINDOWS\\system32\\cmd.exe"]]
                    for app in apps:
                        if f"Open {app[0]}".lower() in self.query.lower():
                         speak(f"Opening {app[0]} sir...")
                         os.startfile(app[1])
                
                elif "youth" in self.query:
                    tells = [["hello youth"]]
                    for tell in tells:
                        if f"{tell[0]}".lower() in self.query.lower():
                         speak(f"hello  sir...")
                        elif "hey youth" in self.query:
                            speak("yes sir , how can i help you .")                        
                     
                else:
                    speak("sorry sir , i did not understand .")
                    

        except Exception as e:
            print(f"sorry sir ,{e} was occures")
            
                    
                
FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"./scifi.ui"))


class Main(QMainWindow,FROM_MAIN):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1920,1080)
        self.label_7 = QLabel
        self.exitB.setStyleSheet("background-image:url(./lib/exit - Copy.png);\n"
        "border:none;")
        self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)
        Dspeak = mainT()
        self.label_7 = QMovie("./lib/gifloader.gif", QByteArray(), self)
        self.label_7.setCacheMode(QMovie.CacheAll)
        self.label_4.setMovie(self.label_7)
        self.label_7.start()

        self.ts = time.strftime("%A, %d %B")

        Dspeak.start()
        self.label.setPixmap(QPixmap("./lib/tuse.png"))
        self.label_5.setText("<font size=8 color='white'>"+self.ts+"</font>")
        self.label_5.setFont(QFont(QFont('Acens',8)))


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())