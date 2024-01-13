import dearpygui.dearpygui as dpg

from gui_manager import GuiManager
from logger_manager import setup_logger
from speech_recognition_manager import SpeechRecognitionManager


class Bob:
    def __init__(self):
        self.logger = setup_logger()
        self.speech_manager = SpeechRecognitionManager(self.transcript_callback, self.logger)
        self.gui_manager = GuiManager(self.start_listening, self.stop_listening, self.process_command)

    def transcript_callback(self, text):
        if self.gui_manager.transcript:
            current_text = dpg.get_value(self.gui_manager.transcript)
            dpg.set_value(self.gui_manager.transcript, current_text + '\n' + text)

    def start_listening(self, sender, app_data):
        self.speech_manager.start_listening()

    def stop_listening(self, sender, app_data):
        self.speech_manager.stop_listening()

    def process_command(self, sender, app_data, user_data):
        command = dpg.get_value(user_data)
        self.logger.info(f"Processing command: {command}")  # Do something with the command

    def run(self):
        dpg.create_context()
        dpg.create_viewport()
        dpg.setup_dearpygui()
        self.gui_manager.setup_gui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
