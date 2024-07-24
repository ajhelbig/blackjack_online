from pygame_widgets.button import ButtonArray
from pygame_widgets.textbox import TextBox

def get_new_play_buttons(window, insurance, double_down, hit, stand, split, surrender):
        window_size = window.get_size()
        height = 100
        width = window_size[0] * 0.75
        x = window_size[0] * 0.125
        y = window_size[1] - 2 * height

        new_play_buttons = ButtonArray(
                            # Mandatory Parameters
                            window,  # Surface to place button array on
                            x,  # X-coordinate
                            y,  # Y-coordinate
                            width,  # Width
                            height,  # Height
                            (6, 1),  # Shape: 2 buttons wide, 2 buttons tall
                            border=10,  # Distance between buttons and edge of array
                            texts=('Insurance', 'Double Down', 'Hit', 'Stand', 'Split', 'Surrender'),  # Sets the texts of each button (counts left to right then top to bottom)
                            # When clicked, print number
                            onClicks=(insurance, double_down, hit, stand, split, surrender))
        
        new_play_buttons.hide()

        return new_play_buttons

def get_new_bet_text_box(window, bet):
        window_size = window.get_size()
        height = 100
        width = window_size[0] * 0.75
        x = window_size[0] * 0.125
        y = window_size[1] - 2 * height

        new_text_box = TextBox(
                            window, 
                            x, 
                            y, 
                            width, 
                            height, 
                            fontSize=50,
                            borderColour=(0, 0, 0), 
                            textColour=(0, 0, 0),
                            onSubmit=bet, 
                            radius=10, 
                            borderThickness=5, 
                            placeholderText="Place Bet")
        
        new_text_box.hide()

        return new_text_box