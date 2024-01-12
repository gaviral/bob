import dearpygui.dearpygui as dpg

from bob import Bob

bob = None


def start_listening_callback(sender, app_data):
    global bob
    if bob: bob.start_listening()


def stop_listening_callback(sender, app_data):
    global bob
    if bob: bob.stop_listening()


def send_command_callback(sender, app_data, user_data):
    command = dpg.get_value(user_data)
    if bob: bob.process_command(command)


def setup_bob_gui():
    with dpg.window(label="Bob - Your AI Assistant"):
        dpg.add_text("This is where Bob's responses will go")
        dpg.add_button(label="Start Listening", callback=start_listening_callback)
        dpg.add_button(label="Stop Listening", callback=stop_listening_callback)
        command_input = dpg.add_input_text(label="Command")
        dpg.add_button(label="Send Command", callback=send_command_callback, user_data=command_input)
        transcript = dpg.add_input_text(label="Transcript", multiline=True, readonly=True)
        dpg.add_button(label="Clear Transcript", callback=lambda: dpg.set_value(transcript, ""))


if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    setup_bob_gui()

    bob = Bob()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
