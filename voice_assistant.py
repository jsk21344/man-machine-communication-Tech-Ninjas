import pyttsx3 as tts
import speech_recognition
from app import debug


class VoiceAssistant:
    def init(self):
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        self.ttsEngine = tts.init()

        self.setup()

    def setup(self):
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
