import random
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time

# operations
import time
import math
import mraa

# assistant
import pyttsx3 as tts
import speech_recognition


app = Flask(__name__)
turbo = Turbo(app)

global assistant
global operations

global maschineID
global debug

maschineID = 0
debug = False


class VoiceAssistant:
    def init(self):
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        self.ttsEngine = tts.init()

        self.setup()

    def setup(self):
        global debug

        voices = self.ttsEngine.getProperty("voices")
        self.ttsEngine.setProperty("voice", voices[8].id)
        self.ttsEngine.setProperty("rate", 150)
        if debug:
            for voice in voices:
                print(str(voice.id))
            print(str(voices[8].id))

    def speak(self, text_to_speech):
        print(str(text_to_speech))
        self.ttsEngine.say(str(text_to_speech))
        self.ttsEngine.runAndWait()

    def listen(self):
        with self.microphone:
            recognized_data = ""

            self.recognizer.adjust_for_ambient_noise(
                self.microphone, duration=2)

            try:
                print("Listening...")
                audio = self.recognizer.listen(self.microphone, 5, 5)

            except speech_recognition.WaitTimeoutError:
                print("Can you check if your microphone is on, please?")
                return

            try:
                print("Started recognition...")
                recognized_data = self.recognizer.recognize_google(
                    audio, language="de").lower()

            except speech_recognition.UnknownValueError:
                pass

            except speech_recognition.RequestError:
                print("Check your Internet Connection, please")

            print("Listened: " + recognized_data)
            return recognized_data


class Operations:
    def eingriff(self):
        s = mraa.Aio(3)
        x = mraa.I2c(0)
        x.address(0x53)

        x.writeReg(0x2D, 8)
        time.sleep(0.01)
        x.writeReg(0x1E, 1)
        time.sleep(0.01)
        x.writeReg(0x1F, 130)
        time.sleep(0.01)
        x.writeReg(0x20, 137)
        time.sleep(0.01)

        sensor_F = 0
        x_out_F = 0
        y_out_F = 0
        z_out_F = 0
        pitch_F = 0
        roll_F = 0

        while True:
            x_out = (x.readReg(0x32) | x.readReg(0x33) << 8)
            x_out = x_out / 25.6
            y_out = (x.readReg(0x34) | x.readReg(0x35) << 8)
            y_out = y_out / 25.6
            z_out = (x.readReg(0x36) | x.readReg(0x37) << 8)
            z_out = z_out / 25.6
            sensor = s.read()

            roll = math.atan(
                y_out/math.sqrt(x_out**2+z_out**2))*180/math.pi
            pitch = math.atan(-1*x_out /
                              math.sqrt(y_out**2+z_out**2))*180/math.pi

            roll_F = 0.5*roll_F+0.5*roll
            pitch_F = 0.5 * pitch_F + 0.5 * pitch
            x_out_F = 0.5 * x_out_F + 0.5 * x_out
            y_out_F = 0.5 * y_out_F + 0.5 * y_out
            z_out_F = 0.5 * z_out_F + 0.5 * z_out
            sensor_F = 0.5 * sensor_F + 0.5 * sensor

            print("Roll:" + str(roll_F) + " pitch: " + str(pitch_F) + " x_out: " + str(x_out_F) +
                  " y_out: " + str(y_out_F) + " z_out: " + str(z_out_F) + "Sensor F: " + str(sensor_F))
            time.sleep(0.1)

    def status(self):
        global assistant
        global maschineID

        if(maschineID == 0):
            assistant.speak("Keine Maschine ausgewählt")
        else:
            assistant.speak("Maschine" + str(maschineID) +
                            "läuft und hat keinen Fehler")

    def select_machine(self, id):
        global maschineID

        maschineID = id

    def start(self):
        global assistant

        assistant.speak("Maschine startet")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page2')
def page2():
    return render_template('page2.html')


@app.context_processor
def inject_load():
    load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {'load1': load[0], 'load5': load[1], 'load15': load[2]}


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()
    threading.Thread(target=main_init).start()


def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))


def main_start_assistant():
    global assistant
    global operations

    while True:
        voice_input = assistant.listen()
        voice_input = voice_input.split(" ")

        for word in voice_input:
            if word == "start" or word == "starten":
                operations.start()
            elif word == "ein" or word == "eins" or word == "1":
                operations.select_machine(1)
            elif word == "status":
                operations.status()
            elif word == "eingriff":
                operations.eingriff()
            else:
                pass


def main_init():
    global assistant
    global operations

    assistant = VoiceAssistant()
    assistant.init()
    assistant.speak("Maschine 1 Bauteil nicht greifbar. Bitte manuell greifen")
    operations = Operations()

    main_start_assistant()

