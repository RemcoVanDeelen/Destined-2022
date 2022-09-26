from tkinter import *
import sys


scr = Tk()
scr.title("Destined")
scr.geometry("1024x576+250+110")
scr.iconphoto(False, PhotoImage(file=(sys.path[0] + "\Images\DestinedWindowIcon.png")))

global screen_size
screen_size = [1024, 576]
global zoom_in, zoom_out
zoom_in = 1
zoom_out = 1


def correct_size(direct=False):
    global screen_size

    if scr.winfo_width() >= scr.winfo_screenwidth() or direct:
        if scr.attributes("-fullscreen"):
            scr.attributes("-fullscreen", False)
        else:
            scr.attributes("-fullscreen", True)
    if scr.winfo_width() / 16 != scr.winfo_width() // 16:
        size = scr.winfo_width() // 16
        height = size * 9
        scr.geometry(str(scr.winfo_width() // 16 * 16) + "x" + str(height))
    size = scr.winfo_width() // 16
    if scr.winfo_height() / 9 != size:
        size = scr.winfo_height() // 9
        width = size * 16
        scr.geometry(str(width) + "x" + str(scr.winfo_height() // 9 * 9))
    screen_size = [scr.winfo_width(), scr.winfo_height()]

    global zoom_in, zoom_out
    for ZoomValue in range(1, 50):
        if ZoomValue / 2 != ZoomValue // 2:
            if int(1024/scr.winfo_width()*ZoomValue) == 1024/scr.winfo_width()*ZoomValue:
                zoom_out = int(1024/scr.winfo_width()*ZoomValue)
                zoom_in = ZoomValue
                break


def fix_screen_size():
    global screen_size, zoom_in, zoom_out

    correct_size()

    for widget in scr.winfo_children():

        try:
            img = widget.image
            img = img.zoom(zoom_in, zoom_in)
            img = img.zoom(4, 4)
            img = img.subsample(zoom_out, zoom_out)
            widget.new_image = img
            widget.configure(image=widget.new_image)
            widget.place_forget()
            widget.show(widget)
        except AttributeError:
            pass

    button.configure(text="Change resolution: " + str(screen_size))
    button.pack_forget()
    button.pack()


e = PhotoImage(file=(sys.path[0] + "\Images\TileTest.png"))
Tile = Label(scr, image=e,)
Tile.image = e


def show(self):
    self.place(relx=-0.4, rely=0.1, relwidth=1, relheight=1)


Tile.show = show

button = Button(scr, command=fix_screen_size,
                text="Change resolution: " + str(screen_size))
button.pack()

scr.bind("<F11>", func=correct_size)
scr.mainloop()
