import random
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time

from operations import Operations
from voice_assistant import VoiceAssistant


app = Flask(__name__)
turbo = Turbo(app)

global assistant
global operations

global maschineID
global debug

maschineID = 0
debug = False


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
    assistant = VoiceAssistant()
    assistant.init()
    voice_input = "Maschine 1 Bauteil nicht greifbar. Bitte manuell greifen"

    assistant.speak(voice_input)
    operations = Operations()

    main_start_assistant()
