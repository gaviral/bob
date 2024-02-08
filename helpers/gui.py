from dearpygui import dearpygui as dpg


def build_gui(is_listening, mic_button_press_handler):
    """Builds the GUI using DearPyGui."""
    dpg.create_context()

    with dpg.theme() as red_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # Red theme for button.

    with dpg.theme() as green_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0, 255))  # Green theme for button.

    # toggle_mic callback
    def toggle_mic(sender, app_data, user_data):
        mic_button_press_handler()

        # Update button theme based on microphone status.
        dpg.bind_item_theme(sender, green_theme if is_listening() else red_theme)

    with dpg.window(label="Chat", pos=(700, 425), width=320, height=800):
        button = dpg.add_button(label="Toggle Microphone", tag="mic_button", callback=toggle_mic)
        dpg.bind_item_theme(button, red_theme)  # Initial red theme.
        dpg.add_text("", tag="transcript_text", parent="Chat", before="mic_button")

    dpg.create_viewport(title='Bob', width=960, height=1080)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def listen_print_loop(responses):
    """Iterates through server responses and updates the transcript."""
    transcript = ""
    partial_transcript = ""

    for response in responses:
        if not response.results or not response.results[0].alternatives:
            continue

        result = response.results[0]

        if result.is_final:
            # Final response - replace the transcript with the punctuated version.
            transcript += result.alternatives[0].transcript.strip() + '\n'
            partial_transcript = ""
        else:
            # Partial response - update the partial transcript.
            partial_transcript = result.alternatives[0].transcript.strip() + "..."

        # Update the DearPyGUI transcript box with the latest transcript.
        if dpg.is_dearpygui_running():
            current_transcript = transcript + ' ' + partial_transcript
            dpg.set_value("transcript_text", current_transcript)
