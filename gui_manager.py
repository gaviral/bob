import dearpygui.dearpygui as dpg


class GuiManager:
    def __init__(self, start_callback, stop_callback, command_callback):
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.command_callback = command_callback
        self.transcript = None

    def clear_transcript(self, sender, app_data, user_data):
        dpg.set_value(self.transcript, "")

    def setup_gui(self):
        with dpg.window(label="Bob - Your AI Assistant"):
            dpg.add_text("This is where Bob's transcriptions will appear")
            dpg.add_button(label="Start Listening", callback=self.start_callback)
            dpg.add_button(label="Stop Listening", callback=self.stop_callback)
            command_input = dpg.add_input_text(label="Command")
            dpg.add_button(label="Send Command", callback=self.command_callback, user_data=command_input)
            self.transcript = dpg.add_input_text(label="Transcript", multiline=True, readonly=True)
            dpg.add_button(label="Clear Transcript", callback=self.clear_transcript)
