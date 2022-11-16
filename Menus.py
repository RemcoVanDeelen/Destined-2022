from Test_room_definitions import *
import Core
import sys


# Save, load and checkpoint functions:
def save_to_file():
    """Function for saving the player object to one of the .txt files.\n
    Writes all keys and value of Player dict to file, replacing tkinter objects with 'passed'.\n
    Written file can be read by load() function."""
    # unbind keys and prepare variables.
    win.unbind("<w>")
    win.unbind("<a>")
    win.unbind("<s>")
    win.unbind("<d>")
    win.unbind("<r>")
    Core.can_escape = False
    current_file = select_file()
    glob = sys.modules["__main__"].global_list

    file = open(r"SaveFile{}.txt".format(current_file), "r+")
    lines = ""
    # Begin writing
    for line in file.readlines():
        if ":pass:" not in line:
            # Write player dictionary to file in current line.
            e = Player1.__dict__.copy()
            for key in e:
                if "<" in str(e[key]) or "<" in repr(e[key]):
                    # Replace found object in dict for name in globals.
                    if type(e[key]) != list:
                        try:
                            e[key] = ["ValueName", list(glob.keys())[list(glob.values()).index(e[key])]]
                        except ValueError:
                            # found object not in globals and thus not required for saving.
                            e[key] = ["passed"]
                    else:
                        lis = []
                        for o in e[key]:
                            # Same function for non list but changed to apply to list.
                            try:
                                o = ["ValueName", list(glob.keys())[list(glob.values()).index(o)]]
                            except ValueError:
                                o = "pass"
                            lis.append(o)
                            if "pass" in lis:
                                # List contains passed values and thus not required for saving.
                                lis = ["passed"]
                        e[key] = lis
            lines += repr(e) + "\n"
        else:
            # Passed lines are passed.
            lines += line
    # Write to- then close file and rebind keys.
    file.close()
    file = open(r"SaveFile{}.txt".format(current_file), "w")
    file.writelines(lines)
    file.close()
    win.bind("<w>", Player1.move)
    win.bind("<a>", Player1.move)
    win.bind("<s>", Player1.move)
    win.bind("<d>", Player1.move)
    win.bind("<r>", Player1.interact)
    Core.can_escape = True
    print(F"<< SAVED TO FILE {current_file} >>")


def load(current_file=0):
    """Function for loading player object from .txt file.\n
    Grabs values from dict and writes to object mentioned above it.\n
    Passes values as required."""
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
                    # Reads value
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
                    # Correctly reads list values
                    for in_value in result:
                        if type(in_value) == str:
                            try:
                                new_value = glob[in_value]
                                result[result.index(in_value)] = new_value
                            except ValueError:
                                pass

                setattr(obj, value, result)   # writes all values to object.
        elif len(line) > 7:
            # if passed line contains object, set current object to write to said object.
            obj = glob[line[7:len(line)-1]]

    # Close menu and load player.
    close_escape_menu()
    door(old, Player1.room, scr, Player1, location=Player1.position)
    scr.coords(Player1.tag, Player1.coordinates[0], Player1.coordinates[1])
    print(F"<< LOADED FILE {current_file} >>")


def select_file():
    """Gives player option to select file, returns file as Int."""
    # placed buttons.
    file1_button.place(x=1920/8*3, y=660, anchor="n")
    file2_button.place(x=1920/8*4, y=660, anchor="n")
    file3_button.place(x=1920/8*5, y=660, anchor="n")
    # wait for result.
    win.waitvar(file_var)
    # remove buttons and return result.
    file1_button.place_forget()
    file2_button.place_forget()
    file3_button.place_forget()
    return file_var.get()


def checkpoint():
    """Checkpoint function for Tile objects,\n
    Shows display asking player if they want to save.\n
    Then asks player where to save to if required."""
    if display(Player1, "Would you like to save at this checkpoint?",
               [[Core.__pass, "Yes"], [Core.__pass, "No"]])[1] == "Yes":
        # The player wants to save,
        # Set player checkpoint to temporary object for save_to_file.
        glob = sys.modules["__main__"].global_list
        Player1.checkpoint = [Player1.position[0], Player1.position[1],
                              list(glob.keys())[list(glob.values()).index(Player1.room)]]
        print(f"checkpoint reached: ({Player1.checkpoint[0]}, {Player1.checkpoint[1]}) in {Player1.checkpoint[2]}")
        # Show GUI complementing select_file function and save to file.
        scr.create_image(960, 636, anchor="center", image=checkpoint_bg, tag="checkpoint_bg")
        scr.create_text(960, 575, text="Select a file to save to:", tag="checkpoint_label", anchor="n",
                        font=("Berlin Sans FB Demi", 18), justify="center")
        save_to_file()
        # Set player object to correct checkpoint list and remove display.
        Player1.checkpoint = [Player1.position[0], Player1.position[1], Player1.room]
        scr.delete("checkpoint_label")
        scr.delete("checkpoint_bg")


# Escape menu functions
def open_escape_menu(*_):
    """Function for displaying escape menu. (bound to Esc.)"""
    if Core.can_escape:
        # Rebind keys
        win.unbind("<w>", )
        win.unbind("<d>", )
        win.unbind("<s>", )
        win.unbind("<a>", )
        win.unbind("<r>", )

        win.bind("<Escape>", close_escape_menu)

        # Place Escape GUI and pause player display
        scr.create_image(960, 540, image=bg_rectangle, tag="BG_rectangle")
        resume_button.place(x=960-120, y=150)
        save_button.place(x=960-120, y=250)
        main_menu_button.place(x=960 - 120, y=350)
        quit_button.place(x=960-120, y=450)

        Player1.disp.cancel()


def close_escape_menu(*_):
    """Function for removing menus from screen. (bound to Esc. when menu is open)"""
    # Rebind keys
    win.bind("<Escape>", open_escape_menu)

    win.bind("<w>", Player1.move)
    win.bind("<d>", Player1.move)
    win.bind("<s>", Player1.move)
    win.bind("<a>", Player1.move)
    win.bind("<r>", Player1.interact)

    # Remove Escape GUI and unpause player display
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
    """Removes all from screen and opens main menu."""
    close_escape_menu()
    # Unbind keys
    win.unbind("<w>", )
    win.unbind("<d>", )
    win.unbind("<s>", )
    win.unbind("<a>", )
    win.unbind("<r>", )
    win.unbind("<Escape>", )

    # Redo display
    Player1.room.unload()
    Player1.disp.cancel()
    scr.delete(Player1.disp.tag)
    scr.create_image(960, 110, image=title_img, tag="Title")

    load_button.place(x=960 - 120, y=250)
    settings_button.place(x=960 - 120, y=350)
    quit_button.place(x=960 - 120, y=450)


# Setting functions:
def open_settings_menu():
    """Removes current menu and places settings buttons,\n
    Currently only allows for toggling fullscreen."""
    # Removes display and unbinds all keys again.
    close_escape_menu()
    Player1.disp.cancel()
    scr.delete(Player1.disp.tag)
    win.unbind("<w>", )
    win.unbind("<d>", )
    win.unbind("<s>", )
    win.unbind("<a>", )
    win.unbind("<r>", )
    win.unbind("<Escape>", )

    # Places return and settings buttons.
    main_menu_button.place(x=840, y=250)
    fullscreen_button.place(x=840, y=350)


def toggle_fullscreen():
    """Current only settings function, toggles fullscreen on or off."""
    if win.attributes("-fullscreen"):
        win.attributes("-fullscreen", False)
    else:
        win.attributes("-fullscreen", True)


# Escape menu GUI:
bg_rectangle = PhotoImage(file="images/BG_rectangle.png".replace("/", os.sep)).zoom(120, 120)
resume_img = PhotoImage(file="images/ButtonTest_resume.png".replace("/", os.sep)).zoom(5, 4)
save_img = PhotoImage(file="images/ButtonTest_save.png".replace("/", os.sep)).zoom(5, 4)
load_img = PhotoImage(file="images/ButtonTest_load.png".replace("/", os.sep)).zoom(5, 4)
main_menu_img = PhotoImage(file="images/ButtonTest_Main_menu.png".replace("/", os.sep)).zoom(5, 4)
settings_img = PhotoImage(file="images/ButtonTest_settings.png".replace("/", os.sep)).zoom(5, 4)
quit_img = PhotoImage(file="images/ButtonTest_quit.png".replace("/", os.sep)).zoom(5, 4)
resume_button = Button(scr, image=resume_img, highlightthickness=0, border=0,
                       activebackground="#000000", command=close_escape_menu)
save_button = Button(scr, image=save_img, highlightthickness=0, border=0,
                     activebackground="#000000", command=save_to_file)
load_button = Button(scr, image=load_img, highlightthickness=0, border=0, activebackground="#000000", command=load)
main_menu_button = Button(scr, image=main_menu_img, highlightthickness=0, border=0,
                          activebackground="#000000", command=open_main_menu)
settings_button = Button(scr, image=settings_img, highlightthickness=0, border=0,
                         activebackground="#000000", command=open_settings_menu)
quit_button = Button(scr, image=quit_img, highlightthickness=0, border=0, activebackground="#000000", command=exit)

title_img = PhotoImage(file="images/Title_screen_name.png".replace("/", os.sep)).zoom(8, 8)


# Setting menu GUI:

toggle_fullscreen_img = PhotoImage(file="images/ButtonTest_toggle_fullscreen.png".replace("/", os.sep)).zoom(5, 4)
fullscreen_button = Button(scr, image=toggle_fullscreen_img, highlightthickness=0, border=0,
                           activebackground="#000000", command=toggle_fullscreen)

# Save menu GUI:
file_var = IntVar()
file1_button = Button(scr, text="File 1", command=lambda: file_var.set(1), font=("Berlin Sans FB Demi", 16),
                      bg="#35AA57", relief="groove", padx=2, pady=2, bd=3, activebackground="#101010")
file2_button = Button(scr, text="File 2", command=lambda: file_var.set(2), font=("Berlin Sans FB Demi", 16),
                      bg="#35AA57", relief="groove", padx=2, pady=2, bd=3, activebackground="#101010")
file3_button = Button(scr, text="File 3", command=lambda: file_var.set(3), font=("Berlin Sans FB Demi", 16),
                      bg="#35AA57", relief="groove", padx=2, pady=2, bd=3, activebackground="#101010")

checkpoint_bg = PhotoImage(file="images/Backgrounds/checkpoint_bg.png".replace("/", os.sep)).zoom(9, 9)

# Binding of Esc.
win.bind("<Escape>", open_escape_menu)
