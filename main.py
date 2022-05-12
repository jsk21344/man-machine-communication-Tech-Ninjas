from operations import Operations
from voice_assistant import VoiceAssistant

voice_output = ""
maschinenID = 0
debug = False


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.init()
    voice_input = "Maschine 1 Bauteil nicht greifbar. Bitte manuell greifen"

    assistant.speak(voice_input)
    operations = Operations()

    while True:
        voice_input = assistant.listen()
        voice_input = voice_input.split(" ")

        for word in voice_input:
            if word == "start" or word == "starten":
                operations.start()
            elif word == "ein" or word == "eins":
                operations.select_machine(1)
            elif word == "status":
                operations.status()
            elif word == "eingriff":
                operations.eingriff()
            else:
                pass

        if voice_output == "":
            pass
        else:
            assistant.speak(voice_output)
            voice_output = ""
