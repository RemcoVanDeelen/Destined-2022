from Test_room_definitions import *
import sys

Player1 = Player("Player1")  # PLAYER location moved here for tile-combat and saving to file.


# Save and load functions:
def save_to_file():
    current_file = select_file()
    glob = sys.modules["__main__"].global_list

    file = open(r"SaveFile{}.txt".format(current_file), "r+")
    lines = ""
    for line in file.readlines():
        if ":pass:" not in line:
            e = Player1.__dict__.copy()
            for key in e:
                if "<" in str(e[key]) or "<" in repr(e[key]):
                    if type(e[key]) != list:
                        try:
                            e[key] = ["ValueName", list(glob.keys())[list(glob.values()).index(e[key])]]
                        except ValueError:
                            e[key] = ["passed"]
                    else:
                        lis = []
                        for o in e[key]:
                            try:
                                o = ["ValueName", list(glob.keys())[list(glob.values()).index(o)]]
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
    glob = sys.modules["__main__"].global_list
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
                        result = glob[dictionary[value][1]]
                    elif "passed" in dictionary[value]:
                        result = getattr(Player1, value)
                    else:
                        result = dictionary[value]
                        if "ValueName" in str(dictionary[value]):
                            result = []
                            for item in dictionary[value]:
                                result.append(glob[item[1]])
                except TypeError:
                    result = dictionary[value]

                if type(result) == list:
                    for in_value in result:
                        if type(in_value) == str:
                            try:
                                new_value = glob[in_value]
                                result[result.index(in_value)] = new_value
                            except ValueError:
                                pass

                setattr(obj, value, result)
        elif len(line) > 7:
            obj = glob[line[7:len(line)-1]]

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


def checkpoint():
    glob = sys.modules["__main__"].global_list
    Player1.checkpoint = [Player1.position[0], Player1.position[1], list(glob.keys())[list(glob.values()).index(Player1.room)]]
    print("checkpoint reached:", Player1.checkpoint)
    save_to_file()


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
        main_menu_button.place(x=960 - 120, y=350)
        quit_button.place(x=960-120, y=450)

        Player1.disp.cancel()


def close_escape_menu(*bound):
    # Rebind all to movement
    win.bind("<Escape>", open_escape_menu)

    win.bind("<w>", Player1.move)
    win.bind("<d>", Player1.move)
    win.bind("<s>", Player1.move)
    win.bind("<a>", Player1.move)
    win.bind("<r>", Player1.interact)
    win.bind("<l>", lambda bound: battle([Player1], [test_foe1, test_foe2], "TestBackground"))

    # Remove Escape GUI
    scr.delete("BG_rectangle")
    scr.delete("Title")
    resume_button.place_forget()
    save_button.place_forget()
    load_button.place_forget()
    main_menu_button.place_forget()
    settings_button.place_forget()
    quit_button.place_forget()

    file1_button.place_forget()
    file2_button.place_forget()
    file3_button.place_forget()

    fullscreen_button.place_forget()

    Player1.disp.roll()


# Main menu functions:
def open_main_menu():
    close_escape_menu()
    # Unbind all
    win.unbind("<w>", )
    win.unbind("<d>", )
    win.unbind("<s>", )
    win.unbind("<a>", )
    win.unbind("<r>", )
    win.unbind("<l>", )
    win.unbind("<Escape>", )

    Player1.room.unload()
    Player1.disp.cancel()
    scr.delete(Player1.disp.tag)
    scr.create_image(960, 100, image=title_img, tag="Title")

    load_button.place(x=960 - 120, y=250)
    settings_button.place(x=960 - 120, y=350)
    quit_button.place(x=960 - 120, y=450)


# Setting functions:
def open_settings_menu():
    close_escape_menu()
    Player1.disp.cancel()
    scr.delete(Player1.disp.tag)
    win.unbind("<w>", )
    win.unbind("<d>", )
    win.unbind("<s>", )
    win.unbind("<a>", )
    win.unbind("<r>", )
    win.unbind("<l>", )
    win.unbind("<Escape>", )

    main_menu_button.place(x=960 - 120, y=250)
    fullscreen_button.place(x=960 - 120, y=350)


def toggle_fullscreen():
    if win.attributes("-fullscreen"):
        win.attributes("-fullscreen", False)
    else:
        win.attributes("-fullscreen", True)


# Escape menu buttons:
bg_rectangle = PhotoImage(file="images/BG_rectangle.png".replace("/", os.sep)).zoom(120, 120)
resume_img = PhotoImage(file="images/ButtonTest_resume.png".replace("/", os.sep)).zoom(5, 4)
save_img = PhotoImage(file="images/ButtonTest_save.png".replace("/", os.sep)).zoom(5, 4)
load_img = PhotoImage(file="images/ButtonTest_load.png".replace("/", os.sep)).zoom(5, 4)
main_menu_img = PhotoImage(file="images/ButtonTest_Main_menu.png".replace("/", os.sep)).zoom(5, 4)
settings_img = PhotoImage(file="images/ButtonTest_settings.png".replace("/", os.sep)).zoom(5, 4)
quit_img = PhotoImage(file="images/ButtonTest_quit.png".replace("/", os.sep)).zoom(5, 4)
resume_button = Button(scr, image=resume_img, highlightthickness=0, border=0, activebackground="#000000", command=close_escape_menu)
save_button = Button(scr, image=save_img, highlightthickness=0, border=0, activebackground="#000000", command=save_to_file)
load_button = Button(scr, image=load_img, highlightthickness=0, border=0, activebackground="#000000", command=load)
main_menu_button = Button(scr, image=main_menu_img, highlightthickness=0, border=0, activebackground="#000000", command=open_main_menu)
settings_button = Button(scr, image=settings_img, highlightthickness=0, border=0, activebackground="#000000", command=open_settings_menu)
quit_button = Button(scr, image=quit_img, highlightthickness=0, border=0, activebackground="#000000", command=exit)

win.bind("<Escape>", open_escape_menu)
title_img = PhotoImage(file="images/Title_test_img.png".replace("/", os.sep)).zoom(5, 5)


# Setting menu buttons:

toggle_fullscreen_img = PhotoImage(file="images/ButtonTest_toggle_fullscreen.png".replace("/", os.sep)).zoom(5, 4)
fullscreen_button = Button(scr, image=toggle_fullscreen_img, highlightthickness=0, border=0, activebackground="#000000", command=toggle_fullscreen)

# Save menu variables:
file_var = IntVar()
file1_button = Button(scr, text="File 1", command=lambda: file_var.set(1))
file2_button = Button(scr, text="File 2", command=lambda: file_var.set(2))
file3_button = Button(scr, text="File 3", command=lambda: file_var.set(3))
