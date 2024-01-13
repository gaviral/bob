import os
import threading

import dearpygui.dearpygui as dpg
import pyaudio
from google.cloud import speech
from six.moves import queue

# Initialize Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Shared state between threads
is_listening = False
transcript = ""
mic_stream = None


class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(format=pyaudio.paInt16, channels=1, rate=self._rate, input=True,
                                                        frames_per_buffer=self._chunk,
                                                        stream_callback=self._fill_buffer)
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them to the text widget."""
    global transcript
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        # Update the transcript variable with the latest result.
        transcript = result.alternatives[0].transcript.rstrip() + ('' if result.is_final else '...')

        # Update the DearPyGUI transcript box with the latest transcript.
        if dpg.is_dearpygui_running():
            dpg.add_text(transcript, parent="Chat", before="mic_button")


def start_speech_recognition():
    """Starts the speech recognition service."""
    global is_listening, mic_stream
    is_listening = True
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=RATE,
                                      language_code="en-US", max_alternatives=1, enable_automatic_punctuation=True)
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        mic_stream = stream
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)


def microphone_toggle():
    global is_listening, mic_stream
    if not is_listening:
        is_listening = True
        threading.Thread(target=start_speech_recognition, daemon=True).start()
    else:
        is_listening = False
        if mic_stream is not None:
            mic_stream.closed = True


def build_gui():
    dpg.create_context()

    mic_on_status = False

    # Define themes
    with dpg.theme() as red_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # Red color

    with dpg.theme() as green_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0, 255))  # Green color

    # toggle_mic callback
    def toggle_mic(sender, app_data, user_data):
        nonlocal mic_on_status
        mic_on_status = not mic_on_status
        microphone_toggle()

        # Bind theme based on mic status
        if mic_on_status:
            dpg.bind_item_theme(sender, green_theme)
        else:
            dpg.bind_item_theme(sender, red_theme)

    # Window 1
    with dpg.window(label="Chat", pos=(700, 425), width=320, height=800):
        button = dpg.add_button(label="Toggle Microphone", tag="mic_button", callback=toggle_mic)
        dpg.bind_item_theme(button, red_theme)  # Initial theme

    dpg.create_viewport(title='Bob', width=960, height=1080)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def main():
    build_gui()


if __name__ == '__main__':
    main()
