import threading
from tkinter import Tk

from pynput.keyboard import Key, Listener


def on_press(key):
    print('{0} pressed'.format(key))

def on_release(key):
    if key == Key.esc:
        return False

# with Listener(on_press=on_press, on_release=on_release) as listener:
print(Listener.__dict__)
xxx = threading.Thread(target=Listener, args=(on_press, 7,))
# xxx.setDaemon(1)  # 设置守护线程，当线程结束，守护线程同时关闭，要不然这个线程会一直运行下去。
xxx.run()

root = Tk()
root.mainloop()