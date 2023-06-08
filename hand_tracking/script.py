import keyboard

def print_p(e):
    print("'p' is pressed")

keyboard.on_press_key('p', print_p)

# Blocking event loop
keyboard.wait()
