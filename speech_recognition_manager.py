from threading import Event

import speech_recognition as sr


class SpeechRecognitionManager:
    def __init__(self, transcript_callback, logger):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_listening = None
        self.transcript_callback = transcript_callback
        self.stop_event = Event()
        self.logger = logger

    def start_listening(self):
        self.stop_event.clear()
        self.stop_listening = self.recognizer.listen_in_background(self.microphone, self.recognize_speech)
        self.logger.debug("Started listening.")

    def stop_listening(self):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=True)  # It should block until listening stops.
            self.stop_event.set()
        self.logger.debug("Stopped listening.")

    def recognize_speech(self, recognizer, audio):
        if self.stop_event.is_set():
            return

        try:
            self.logger.debug("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            self.transcript_callback(text)
        except sr.UnknownValueError:
            self.logger.error("Could not understand the audio")
        except sr.RequestError as e:
            self.logger.error(f"Request failed; {e}")
