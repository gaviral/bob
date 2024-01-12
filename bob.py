import logging
from threading import Event

import speech_recognition as sr

# Initialize the logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Bob')


class Bob:
    def __init__(self, transcript_callback):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_listening = None
        self.transcript_callback = transcript_callback  # Callback method to update the GUI with the transcription
        self.stop_event = Event()

    def start_listening(self):
        self.stop_event.clear()
        self.stop_listening = self.recognizer.listen_in_background(self.microphone, self.recognize_speech)
        logger.debug("Bob started listening.")

    def stop_listening(self):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
            self.stop_event.set()
        logger.debug("Bob stopped listening.")

    def recognize_speech(self, recognizer, audio):
        if self.stop_event.is_set():
            return  # Stop processing if stop_event is set

        try:
            logger.debug("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            self.process_transcription(text)
        except sr.UnknownValueError:
            logger.error("Bob could not understand the audio")
        except sr.RequestError as e:
            logger.error(f"Request failed; {e}")

    def process_transcription(self, text):
        logger.info(f"Bob heard: {text}")
        self.transcript_callback(text)

    def process_command(self, command):
        logger.info(f"Processing command: {command}")  # Additional command processing logic would go here

# file: bob.py
