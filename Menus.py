from Test_room_definitions import *
from Action_definitions import *


# Save and load functions:
def save_to_file():
    current_file = select_file()

    file = open(r"SaveFile{}.txt".format(current_file), "r+")
    lines = ""
    for line in file.readlines():
        if ":pass:" not in line:
            e = Player1.__dict__.copy()
            for key in e:
                if "<" in str(e[key]) or "<" in repr(e[key]):
                    if type(e[key]) != list:
                        try:
                            e[key] = ["ValueName", list(globals().keys())[list(globals().values()).index(e[key])]]
                        except ValueError:
                            e[key] = ["passed"]
                    else:
                        lis = []
                        for o in e[key]:
                            try:
                                o = ["ValueName", list(globals().keys())[list(globals().values()).index(o)]]
                            except ValueError:
                                o = "pass"
                            lis.append(o)
                            if "pass" in lis:
                                lis = ["passed"]
                        e[key] = lis
            lines += repr(e) + "\n"
        else:

            lines += line
    file.close()
    file = open(r"SaveFile{}.txt".format(current_file), "w")
    file.writelines(lines)
    file.close()


def load(current_file=0):
    old = Player1.room

    if current_file == 0:
        current_file = select_file()

    file = open(r"SaveFile{}.txt".format(current_file), "r")
    obj = None
    for line in file.readlines():
        if ":pass:" not in line:
            dictionary = eval(line)
            for value in dictionary:
                try:
                    if "ValueName" in dictionary[value]:
                        result = globals()[dictionary[value][1]]
                    elif "passed" in dictionary[value]:
                        result = getattr(Player1, value)
                    else:
                        result = dictionary[value]
                        if "ValueName" in str(dictionary[value]):
                            result = []
                            for item in dictionary[value]:
                                result.append(globals()[item[1]])
                except TypeError:
                    result = dictionary[value]

                setattr(obj, value, result)
        elif len(line) > 7:
            obj = globals()[line[7:len(line)-1]]

    close_escape_menu()
    door(old, Player1.room, scr, Player1, location=Player1.position)
    scr.coords(Player1.tag, Player1.coordinates[0], Player1.coordinates[1])


def select_file():
    file1_button.place(x=100, y=100)
    file2_button.place(x=300, y=100)
    file3_button.place(x=500, y=100)
    win.waitvar(file_var)
    file1_button.place_forget()
    file2_button.place_forget()
    file3_button.place_forget()
    return file_var.get()


# Escape menu functions
def open_escape_menu(*bound):
    if not scr.find_withtag("bg_img"):  # if not in battle:
        # Unbind all
        win.unbind("<w>", )
        win.unbind("<d>", )
        win.unbind("<s>", )
        win.unbind("<a>", )
        win.unbind("<r>", )
        win.unbind("<l>", )

        win.bind("<Escape>", close_escape_menu)

        # Place Escape GUI
        scr.create_image(960, 540, image=bg_rectangle, tag="BG_rectangle")
        resume_button.place(x=960-120, y=150)
        save_button.place(x=960-120, y=250)
        load_button.place(x=960-120, y=350)
        settings_button.place(x=960-120, y=450)
        quit_button.place(x=960-120, y=550)


def close_escape_menu(*bound):
    # Rebind all to movement
    win.bind("<Escape>", open_escape_menu)

    win.bind("<w>", Player1.move)
    win.bind("<d>", Player1.move)
    win.bind("<s>", Player1.move)
    win.bind("<a>", Player1.move)
    win.bind("<r>", Player1.interact)
    win.bind("<l>", lambda bound: battle([Player1], [test_foe1], "TestBackground"))

    # Remove Escape GUI
    scr.delete("BG_rectangle")
    resume_button.place_forget()
    save_button.place_forget()
    load_button.place_forget()
    settings_button.place_forget()
    quit_button.place_forget()

    file1_button.place_forget()
    file2_button.place_forget()
    file3_button.place_forget()


# Escape menu buttons:
bg_rectangle = PhotoImage(file="images/BG_rectangle.png").zoom(120, 120)
resume_img = PhotoImage(file="images/ButtonTest_resume.png").zoom(5, 4)
save_img = PhotoImage(file="images/ButtonTest_save.png").zoom(5, 4)
load_img = PhotoImage(file="images/ButtonTest_load.png").zoom(5, 4)
settings_img = PhotoImage(file="images/ButtonTest_settings.png").zoom(5, 4)
quit_img = PhotoImage(file="images/ButtonTest_quit.png").zoom(5, 4)
resume_button = Button(scr, image=resume_img, highlightthickness=0, border=0, activebackground="#000000", command=close_escape_menu)
save_button = Button(scr, image=save_img, highlightthickness=0, border=0, activebackground="#000000", command=save_to_file)
load_button = Button(scr, image=load_img, highlightthickness=0, border=0, activebackground="#000000", command=load)
settings_button = Button(scr, image=settings_img, highlightthickness=0, border=0, activebackground="#000000", command=exit)
quit_button = Button(scr, image=quit_img, highlightthickness=0, border=0, activebackground="#000000", command=exit)

win.bind("<Escape>", open_escape_menu)


# Save menu variables:
file_var = IntVar()
file1_button = Button(scr, text="File 1", command=lambda: file_var.set(1))
file2_button = Button(scr, text="File 2", command=lambda: file_var.set(2))
file3_button = Button(scr, text="File 3", command=lambda: file_var.set(3))
