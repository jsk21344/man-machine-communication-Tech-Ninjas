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
global eingriff  # ist im eingriff?
global movement  # hand movement from 'eingriff'
global error

movement = [-100, 45, 30, 0]
maschineID = 0
error = False

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
        global eingriff
        global movement

        eingriff = True

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
        with app.app_context():
            while eingriff:
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
                # [transZ, rotZ, rotX, rotY]
                movement = [-100, pitch_F, roll_F, 0]
                turbo.push(turbo.replace(
                    render_template('index.html'), 'cube'))
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
        global assistant

        maschineID = id
        assistant.speak("Maschine " + str(maschineID) + " ausgewählt")

    def start(self):
        global assistant

        assistant.speak("Maschine startet")

    def stopp(self):
        global eingriff
        global assistant

        eingriff = False
        assistant.speak("Stopp Eingriff")

    def check_error(self):
        global error
        global assistant

        error = False
        assistant.speak("Fehler wurde behoben")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/error')
def throw_error():
    global error

    error = True
    assistant.speak(
        "Maschine 1 Error. Bauteil nicht greifbar. Bitte manuell greifen")


@app.context_processor
def inject_load():
    global movement
    return {'transZ': movement[0], 'rotZ': movement[1], 'rotX': movement[2], 'rotY': movement[3]}


@app.before_first_request
def before_first_request():
    threading.Thread(target=main_init).start()


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
                threading.Thread(target=operations.eingriff).start()
            elif word == "stopp":
                operations.stopp()
                operations.check_error()
            else:
                pass


def main_init():
    global assistant
    global operations

    assistant = VoiceAssistant()
    assistant.init()
    operations = Operations()

    main_start_assistant()
