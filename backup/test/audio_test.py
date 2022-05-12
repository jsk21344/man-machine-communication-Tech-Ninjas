# coding=utf-8
# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import speech_recognition
import pyttsx3 as tts


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
    microphone = speech_recognition.Microphone()

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
      play_voice_assistant_speech('hallo')
