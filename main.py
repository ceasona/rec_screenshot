import tkinter
import tkinter.filedialog
import os
from PIL import ImageGrab
from time import sleep
from tkinter import StringVar, NE, messagebox
import paddleocr

ocrer = paddleocr.PaddleOCR(show_log=False, use_gpu=None)

# 创建tkinter主窗口

root = tkinter.Tk()
root.title('REC')
# 指定主窗口位置与大小
root.geometry('200x80+400+300')
# 不允许改变窗口大小
root.resizable(False, False)


class Popup:
    def __init__(self, title: str = "Popup", message: str = "", master=None):
        if master is None:
            # If the caller didn't give us a master, use the default one instead
            master = tkinter._get_default_root()

        # Create a toplevel widget
        self.root = tkinter.Toplevel(root)
        # A min size so the window doesn't start to look too bad
        self.root.minsize(200, 40)
        # Stop the user from resizing the window
        self.root.resizable(False, False)
        # If the user presses the `X` in the titlebar of the window call
        # self.destroy()
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
        # Set the title of the popup window
        self.root.title(title)

        # Calculate the needed width/height
        width = max(map(len, message.split("\n"))) + 2
        height = message.count("\n") + 10
        self.message = message
        # Create the text widget
        self.text = tkinter.Text(self.root, bg="#f0f0ed", height=height,
                                 width=width, highlightthickness=0, bd=0,
                                 selectbackground="orange")
        # Add the text to the widget
        self.text.insert("end", message)
        # Make sure the user can't edit the message
        self.text.config(state="disabled")
        self.text.pack()

        # Create the "Ok" button
        self.button = tkinter.Button(self.root, text="Ok", command=self.destroy)
        self.button.pack()

        # Please note that you can add an icon/image here. I don't want to
        # download an image right now.
        ...

        # Make sure the user isn't able to spawn new popups while this is
        # still alive
        self.root.grab_set()
        # Stop code execution in the function that called us
        self.root.mainloop()

    def destroy(self) -> None:
        # Stop the `.mainloop()` that's inside this class
        self.root.quit()
        # Destroy the window
        self.root.destroy()


class MyCapture:
    def __init__(self, png):
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)

        self.selectPosition = None
        # 屏幕尺寸
        screenWidth = root.winfo_screenwidth()
        # print(screenWidth)
        screenHeight = root.winfo_screenheight()
        # print(screenHeight)
        # 创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=screenWidth, height=screenHeight)
        # 不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=screenWidth, height=screenHeight)
        # 显示全屏截图，在全屏截图上进行区域截图
        self.p_w_picpath = tkinter.PhotoImage(file=png)
        # image = Image.open(png)
        # photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(screenWidth, 0, anchor=NE, image=self.p_w_picpath)

        # self.canvas.create_p_w_picpath(screenWidth // 2, screenHeight // 2, p_w_picpath=self.p_w_picpath)

        # 鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            # 开始截图
            self.sel = True

        self.canvas.bind('<Button-1>', onLeftButtonDown)

        # 鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            if not self.sel:
                return
            global lastDraw
            try:
                # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='black')

        self.canvas.bind('<B1-Motion>', onLeftButtonMove)

        # 获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            self.sel = False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            sleep(0.1)
            # 考虑鼠标左键从右下方按下而从左上方抬起的截图
            myleft, myright = sorted([self.X.get(), event.x])
            mytop, mybottom = sorted([self.Y.get(), event.y])
            self.selectPosition = (myleft, myright, mytop, mybottom)
            self.top.destroy()

        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    # 开始截图


text = StringVar()
text.set('copyright@wf')


def buttonCaptureClick():
    # 最小化主窗口
    # root.state('icon')
    # sleep(0.2)

    filename = 'temp.png'
    im = ImageGrab.grab()
    print(type(im))
    im.save(filename)
    # im.close()
    # 显示全屏幕截图
    full_screen = MyCapture(filename)
    buttonCapture.wait_window(full_screen.top)
    # text.set(str(full_screen.selectPosition))

    # print(w.myleft,w.mybottom)
    # 截图结束，恢复主窗口，并删除临时的全屏幕截图文件
    # label.config(text='Hello')
    root.state('normal')
    w, h = im.size
    myleft, myright, mytop, mybottom = full_screen.selectPosition
    cropim = im.crop((myleft, mytop, myright, mybottom))
    # 保存，也是保存在当前目录
    # print(type(cropim))
    # cropim.save("cropim.png")
    os.remove(filename)

    try:
        import numpy
        word_mes = ocrer.ocr(numpy.array(cropim), det=True, rec=True, cls=False)
        res = []
        line = ''
        for i in word_mes:
            line += i[-1][0]
            if len(line) > 40:
                res.append(line)
                line = ''
            else:
                line += ' '
        if line:
            res.append(line)
        res = '\n'.join(res)
    except Exception as e:
        res = str(e)
    if not len(res):
        messagebox.showinfo('Tips', '要识别的文字距离边界保持一定距离')
    else:
        Popup(title="Output", message=res, master=root)


def hotkey(event):
    if event.keysym == 'c':
        buttonCaptureClick()


label = tkinter.Label(root, textvariable=text, fg="gray")
label.place(x=40, y=50, width=140, height=20)
label.config(text='New test')
buttonCapture = tkinter.Button(root, fg="white", bg="Midnightblue", text='截图识别', command=buttonCaptureClick)
root.bind_all("<Alt-Key>", hotkey)

buttonCapture.place(x=30, y=10, width=140, height=40)
# 启动消息主循环
root.mainloop()
