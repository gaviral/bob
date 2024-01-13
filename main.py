import os

import pyaudio
from google.cloud import speech
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


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
            frames_per_buffer=self._chunk, stream_callback=self._fill_buffer, )
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
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)


# def listen_print_loop(responses):
#     """Iterates through server responses and prints them."""
#     for response in responses:
#         if not response.results:
#             continue
#         result = response.results[0]
#         if not result.alternatives:
#             continue
#         # The `-` is known to indicate that the recognizer is currently
#         # predicting the rest of the sentence.
#         print(f"A: {result.alternatives[0].transcript}")

# def listen_print_loop(responses):
#     """Iterates through server responses and prints them."""
#     num_chars_printed = 0
#     for response in responses:
#         if not response.results:
#             continue
#
#         result = response.results[0]
#         if not result.alternatives:
#             continue
#
#         transcript = result.alternatives[0].transcript
#
#         # Check if this is a final result or an interim result.
#         if not result.is_final:
#             # If interim result, print the new part of the transcript.
#             new_chars = transcript[num_chars_printed:]
#             print(new_chars, end='', flush=True)
#             num_chars_printed = len(transcript)
#
#         else:
#             # If final result, print the entire transcript and reset counter.
#             print(transcript)
#             num_chars_printed = 0

def listen_print_loop(responses):
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        if result.is_final:
            print(f"A: {result.alternatives[0].transcript}")


# def listen_print_loop(responses):
#     num_chars_printed = 0
#     for response in responses:
#         if not response.results:
#             continue
#
#         result = response.results[0]
#         if not result.alternatives:
#             continue
#
#         transcript = result.alternatives[0].transcript
#
#         if not result.is_final:
#             new_chars = transcript[num_chars_printed:]
#             print(new_chars, end='', flush=True)
#             num_chars_printed = len(transcript)
#         else:
#             print(transcript + '\r', end='', flush=True)
#             num_chars_printed = 0



def main():
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=RATE,
        language_code="en-US", max_alternatives=1, enable_automatic_punctuation=True)

    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)


if __name__ == '__main__':
    main()
