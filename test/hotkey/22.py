import tkinter
import ctypes
import win32con

class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)

        user32 = ctypes.windll.user32
        # print(user32.RegisterHotKey,"#")
        print((None, 1, win32con.MOD_WIN , win32con.VK_F3))
        # print(user32.RegisterHotKey(None, 1, win32con.MOD_WIN , win32con.VK_F3))
        if user32.RegisterHotKey(None, 1, win32con.MOD_WIN , win32con.VK_F3):
            print("hotkey registered")
        else:
            print("Cannot register hotkey")

        self.protocol("WM_HOTKEY", self.hotkey_received)

    def hotkey_received(self):
        print("hotkey")

if __name__ == "__main__":
    app = App()
    app.mainloop()
    try:
        app.destroy()
    except:
        pass