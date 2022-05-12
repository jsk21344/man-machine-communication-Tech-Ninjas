import pyttsx3 as tts
import speech_recognition


class VoiceAssistant:
    ttsEngine
    recognizer
    microphone

    def init():
        global ttsEngine
        global recognizer
        global microphone

        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()
        ttsEngine = tts.init()

        VoiceAssistant.setup()

    def setup(assistant):
        global debug
        voices = ttsEngine.getProperty("voices")
        assistant.recognition_language = "de-DE"
        ttsEngine.setProperty("voice", voices[8].id)
        ttsEngine.setProperty("rate", 150)
        if debug:
            for voice in voices:
                print(str(voice.id))
            print(str(voices[8].id))

    def speak(text_to_speech):
        print(str(text_to_speech))
        ttsEngine.say(str(text_to_speech))
        ttsEngine.runAndWait()

    def listen():
        with microphone:
            recognized_data = ""

            recognizer.adjust_for_ambient_noise(microphone, duration=2)

            try:
                print("Listening...")
                audio = recognizer.listen(microphone, 5, 5)

            except speech_recognition.WaitTimeoutError:
                print("Can you check if your microphone is on, please?")
                return

            try:
                print("Started recognition...")
                recognized_data = recognizer.recognize_google(
                    audio, language="de").lower()

            except speech_recognition.UnknownValueError:
                pass

            except speech_recognition.RequestError:
                print("Check your Internet Connection, please")

            return recognized_data
