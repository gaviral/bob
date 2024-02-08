import threading

from google.cloud import speech

from config import RATE, CHUNK
from helpers.gui import listen_print_loop, build_gui
from helpers.mic import MicrophoneStream


class Bob:
    """
    Bob - AI assistant
    """

    def __init__(self):
        self.listening = False
        self.mic_stream = None
        build_gui(self.is_listening, self.mic_button_press_handler)

    def is_listening(self):
        return self.listening

    def start_speech_recognition(self):
        """Starts the speech recognition service."""

        is_listening = True
        client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code="en-US",
            max_alternatives=1
            # enable_automatic_punctuation=True
        )
        streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

        with MicrophoneStream(RATE, CHUNK) as stream:
            self.mic_stream = stream
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
            responses = client.streaming_recognize(streaming_config, requests)

            # Put the transcription responses to use.
            listen_print_loop(responses)

    def mic_button_press_handler(self):
        """Toggles the microphone stream on or off."""
        if not self.listening:
            self.listening = True
            threading.Thread(target=self.start_speech_recognition, daemon=True).start()
        else:
            self.listening = False
            if self.mic_stream:
                self.mic_stream.closed = True
