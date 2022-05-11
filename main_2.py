# coding=utf-8
# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import speech_recognition
import pyttsx3 as tts
import time
import numpy
import mraa


class VoiceAssistant:
    """
      ,  , ,
    """
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""


    def setup_assistant_voice(assistant):

        voices = ttsEngine.getProperty("voices")

        if assistant.speech_language == "en":
            assistant.recognition_language = "en-US"
            if assistant.sex == "female":
                # Microsoft Zira Desktop - English (United States)
                ttsEngine.setProperty("voice", voices[1].id)
                ttsEngine.connect()
            else:
                # Microsoft David Desktop - English (United States)
                ttsEngine.setProperty("voice", voices[2].id)
        else:
            assistant.recognition_language = "ru-RU"
            # Microsoft Irina Desktop - Russian
            ttsEngine.setProperty("voice", voices[0].id)


def play_voice_assistant_speech(text_to_speech):
    """
         (  )
        :param text_to_speech: ,
        """
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.


def record_and_recognize_audio():
    """

    """
    with microphone:
        recognized_data = ""

        #
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        #  online-  Google
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="de").lower()

        except speech_recognition.UnknownValueError:
            pass

        #
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data


if __name__ == "__main__":

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone(microphone_ID=1)

    #
    ttsEngine = tts.init()

    #
    assistant = VoiceAssistant()
    assistant.name = "Alice"
    assistant.sex = "female"
    assistant.speech_language = "ru"

    #
    assistant.setup_assistant_voice()
    voice_input = "Maschine 1 Bauteil nicht greifbar. Bitte manuell greifen"
    print(voice_input)
    voice_input = voice_input.split(" ")
    for word in voice_input:
        if word == "":
            pass
        else:
            play_voice_assistant_speech(word)

    while True:
        #
        #
        voice_input = record_and_recognize_audio()
        # os.remove("microphone-results.wav")
        print(voice_input)

        #      ()

        voice_input = voice_input.split(" ")
        voice_output = " "
        maschinenID = 0
        for word in voice_input:
            if word == "start" or word == "starten":
                voice_output = "Maschine startet"

            elif word == "ein":
                maschinenID = 1
            elif word == "status":
                voice_output = "Maschine" + str(maschinenID) + "läuft und hat keinen Fehler"
            elif word == "eingriff":
                s = mraa.Aio(A3)
                x = m.I2c(0)
                x.adress(0x53)

                x.writeReg(0x2D, 8)
                time.sleep(0.01)
                x.writeReg(0x1E, 1)
                time.sleep(0.01)
                x.writeReg(0x1F, -2)
                time.sleep(0.01)
                x.writeReg(0x20, -9)
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

                    roll = numpy.arctan(y_out/sqrt(numpy.power(x_out, 2)+numpy.power(z_out, 2)))*180/pi()
                    pitch = numpy.arctan(-1*x_out/sqrt(numpy.power(y_out, 2)+numpy.power(z_out, 2)))*180/pi()

                    roll_F = 0.5*roll_F+0.5*roll
                    pitch_F = 0.5 * pitch_F + 0.5 * pitch
                    x_out_F = 0.5 * x_out_F + 0.5 * x_out
                    y_out_F = 0.5 * y_out_F + 0.5 * y_out
                    z_out_F = 0.5 * z_out_F + 0.5 * z_out
                    sensor_F = 0.5 * sensor_F + 0.5 * sensor

                    print("Roll:" + str(roll_F) + " pitch: " + str(pitch_F) + " x_out: " + str(x_out_F) + " y_out: " + str(y_out_F) + " z_out: " + str(z_out_F) + "Sensor F: " + str(sensor_F)))
                    time.sleep(0.1)

            else:
                pass

        voice_output = voice_output.split(" ")
        for word in voice_output:
            if word == "":
                pass
            else:
                play_voice_assistant_speech(word)
