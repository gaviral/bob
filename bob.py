import logging

import speech_recognition as sr

# Initialize the logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Bob')


class Bob:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False

    def start_listening(self):
        self.listening = True
        logger.debug("Bob started listening.")
        # This will be an asynchronous call in the actual implementation
        self.listen()

    def stop_listening(self):
        self.listening = False
        logger.debug("Bob stopped listening.")

    def listen(self):
        if self.listening:
            try:
                with self.microphone as source:
                    logger.debug("Adjusting for ambient noise, please wait...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    logger.debug("Listening for speech...")
                    audio = self.recognizer.listen(source)

                logger.debug("Recognizing speech...")
                text = self.recognizer.recognize_google(audio)
                self.process_transcription(text)
            except sr.UnknownValueError:
                logger.error("Bob could not understand the audio")
            except sr.RequestError as e:
                logger.error(f"Request failed; {e}")

    def process_transcription(self, text):
        logger.info(f"Bob heard: {text}")

    def process_command(self, command):
        logger.info(f"Processing command: {command}")  # Additional command processing logic would go here
