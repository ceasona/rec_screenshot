from pynput.keyboard import Listener

def on_press(key):
    print("PRESSED", key)


with Listener(on_press=on_press) as listener:
    listener.join()