"""
Menus.py
--

This file holds all functions regarding large menus and Saving and Loading files.
All used images and buttons are made at end of file.

"""
from Test_room_definitions import *
import Core
import sys


# Save, load and checkpoint functions:
def save_to_file(settings=False):
    """
    Function for saving the changeable objects to one of the .txt files.\n
    Writes all keys and value of object dict to file, replacing tkinter objects with 'passed'.\n
    Written file can be read by load() function.

    When settings=True the file it is saved to is to Settings.txt
    Else the file must be selected first.

    The objects that are to be saved are mentioned in the txt file above the prior dictionary.
    """
    # unbind keys and prepare variables.
    win.unbind(f"<{Settings.inventoryKey}>")
    win.unbind(f"<{Settings.upKey}>")
    win.unbind(f"<{Settings.leftKey}>")
    win.unbind(f"<{Settings.downKey}>")
    win.unbind(f"<{Settings.rightKey}>")
    win.unbind(f"<{Settings.interactKey}>")
    Core.can_escape = False
    if not settings:
        current_file = f"Savefile{select_file()}"
    else:
        current_file = "Settings"
    glob = sys.modules["__main__"].global_list

    file = open(f"{current_file}.txt", "r+")
    lines = ""
    # Begin writing
    obj = None
    for line in file.readlines():
        if ":pass:" not in line:
            # Write object dictionary to file in current line.
            e = obj.__dict__.copy()
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
                            if type(o) not in [int, float]:
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
            if len(line) > 7:
                # if passed line contains object, set current object to write to said object.
                obj = glob[line[7:len(line) - 1]]
            # Passed lines are passed.
            lines += line

    # Write to- then close file and rebind keys if necessary.
    file.close()
    file = open(r"{}.txt".format(current_file), "w")
    file.writelines(lines)
    file.close()
    if not settings:
        win.bind(f"<{Settings.inventoryKey}>", lambda _: open_inventory(Player1))
        win.bind(f"<{Settings.upKey}>", Player1.move)
        win.bind(f"<{Settings.leftKey}>", Player1.move)
        win.bind(f"<{Settings.downKey}>", Player1.move)
        win.bind(f"<{Settings.rightKey}>", Player1.move)
        win.bind(f"<{Settings.interactKey}>", Player1.interact)
        Core.can_escape = True
        print(F"<< SAVED TO FILE {current_file} >>")


def load(current_file=0):
    """
    Function for loading object from .txt file
    Reads keys and values of object dict from file, skipping passed values.\n

    """
    # Prepares variables
    glob = sys.modules["__main__"].global_list
    old = Player1.room

    if current_file == 0:
        current_file = f"Savefile{select_file()}"

    file = open(f"{current_file}.txt", "r")
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
                        result = getattr(obj, value)
                    else:
                        result = dictionary[value]
                        if "ValueName" in str(dictionary[value]):
                            result = []
                            for item in dictionary[value]:
                                if type(item) == list:
                                    result.append(glob[item[1]])
                                else:
                                    result.append(item)
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
            continue

        # if obj is a store, redo its items list.
        if type(obj) == Store:
            obj.items = []
            for item_ind in range(0, obj.size):
                result = getattr(obj, f"item{item_ind}")
                try:
                    result[0] = glob[result[0][1]]
                except TypeError:
                    pass
                obj.items.append(result)

    file.close()
    # Close menu and load player.
    if current_file != "Settings":
        close_all()
        door(old, Player1.room, scr, Player1, location=Player1.position)
        scr.coords(Player1.tag, Player1.coordinates[0], Player1.coordinates[1])
        print(F"<< LOADED FILE {current_file} >>")


def select_file():
    """Gives player option to select file, returns file as Int."""
    # place buttons.
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
    """
    Checkpoint function for Tile objects,\n
    Shows display asking player whether they want to save or not.\n
    Then asks player where to save to if required.
    Finally saves to file and sets player checkpoint.

    """
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
        win.unbind(f"<{Settings.inventoryKey}>")
        win.unbind(f"<{Settings.upKey}>", )
        win.unbind(f"<{Settings.rightKey}>", )
        win.unbind(f"<{Settings.downKey}>", )
        win.unbind(f"<{Settings.leftKey}>", )
        win.unbind(f"<{Settings.interactKey}>", )

        win.bind(f"<{Settings.escapeKey}>", close_all)

        # Place Escape GUI and pause player display
        scr.create_image(960, 540, image=bg_rectangle, tag="BG_rectangle")
        resume_button.place(x=960-120, y=150)
        save_button.place(x=960-120, y=250)
        main_menu_button.place(x=960 - 120, y=350)
        quit_button.place(x=960-120, y=450)

        Player1.disp.cancel()


def close_all(*_):
    """Function for closing any menu and returning to the previous screen."""
    # rebind keys
    win.bind(f"<{Settings.escapeKey}>", open_escape_menu)

    win.bind(f"<{Settings.inventoryKey}>", lambda _: open_inventory(Player1))
    win.bind(f"<{Settings.upKey}>", Player1.move)
    win.bind(f"<{Settings.rightKey}>", Player1.move)
    win.bind(f"<{Settings.downKey}>", Player1.move)
    win.bind(f"<{Settings.leftKey}>", Player1.move)
    win.bind(f"<{Settings.interactKey}>", Player1.interact)
    Core.can_escape = True

    # reconfigure screen
    Player1.disp.roll()

    for child in scr.winfo_children():
        child.place_forget()
    scr.delete("BG_rectangle")
    scr.delete("control_text")
    scr.delete("Title")


# Main menu functions:
def open_main_menu():
    """Removes all from screen and opens main menu."""
    close_all()
    # Unbind keys
    win.unbind(f"<{Settings.inventoryKey}>")
    win.unbind(f"<{Settings.upKey}>", )
    win.unbind(f"<{Settings.rightKey}>", )
    win.unbind(f"<{Settings.downKey}>", )
    win.unbind(f"<{Settings.leftKey}>", )
    win.unbind(f"<{Settings.interactKey}>", )
    win.unbind(f"<{Settings.escapeKey}>", )

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
    """
    Removes current menu and places settings buttons,\n
    Currently only allows for toggling fullscreen.

    """
    # Removes display and unbinds all keys again.
    close_all()
    Player1.disp.cancel()
    scr.delete(Player1.disp.tag)
    win.unbind(f"<{Settings.inventoryKey}>")
    win.unbind(f"<{Settings.upKey}>", )
    win.unbind(f"<{Settings.rightKey}>", )
    win.unbind(f"<{Settings.downKey}>", )
    win.unbind(f"<{Settings.leftKey}>", )
    win.unbind(f"<{Settings.interactKey}>", )
    win.unbind(f"<{Settings.escapeKey}>", )

    # Places return and settings buttons.
    main_menu_button.place(x=840, y=250)
    fullscreen_button.place(x=840, y=330)
    scr.create_text(960, 435, font=("Berlin Sans FB Demi", 17), fill="#ABABAB", text=f"CONTROLS:\n", tag="control_text")
    Button(scr, text=f"UP:  {Settings.upKey}", font=("Berlin Sans Demi", 17), bg="#040C35", fg="#A8A8A8",
           width=18, command=lambda: redo_key_binds1("up")).place(x=840, y=450)
    Button(scr, text=f"LEFT:  {Settings.leftKey}", font=("Berlin Sans Demi", 17), bg="#040C35", fg="#A8A8A8",
           width=18, command=lambda: redo_key_binds1("left")).place(x=840, y=500)
    Button(scr, text=f"DOWN:  {Settings.downKey}", font=("Berlin Sans Demi", 17), bg="#040C35", fg="#A8A8A8",
           width=18, command=lambda: redo_key_binds1("down")).place(x=840, y=550)
    Button(scr, text=f"RIGHT:  {Settings.rightKey}", font=("Berlin Sans Demi", 17), bg="#040C35", fg="#A8A8A8",
           width=18, command=lambda: redo_key_binds1("right")).place(x=840, y=600)
    Button(scr, text=f"INTERACT:  {Settings.interactKey}", font=("Berlin Sans Demi", 17), bg="#040C35", fg="#A8A8A8",
           width=18, command=lambda: redo_key_binds1("interact")).place(x=840, y=650)
    Button(scr, text=f"OPEN STATS:  {Settings.inventoryKey}", font=("Berlin Sans Demi", 17), bg="#040C35",
           fg="#A8A8A8", width=18, command=lambda: redo_key_binds1("inventory")).place(x=840, y=700)
    Button(scr, text=f"ESCAPE:  {Settings.escapeKey}", font=("Berlin Sans Demi", 17), bg="#040C35", fg="#A8A8A8",
           width=18, command=lambda: redo_key_binds1("escape")).place(x=840, y=750)


def toggle_fullscreen():
    """
    Settings function, toggles fullscreen on or off.
    Defaults to fullscreen = on.
    * The game is not optimized for windowed mode.

    """
    if win.attributes("-fullscreen"):
        win.attributes("-fullscreen", False)
    else:
        win.attributes("-fullscreen", True)


def redo_key_binds1(function):
    """
    Step 1 for rebinding keys in the settings menu.
    rebinds <Key> to step 2
    """
    win.bind("<Key>", lambda event: redo_key_binds2(event, function))


def redo_key_binds2(key, function):
    """
    Final step in rebinding keys in the settings menu.
    rebinds pressed key from <Key> to function and unbinds <Key>
    """

    win.unbind("<Key>")
    Settings.__setattr__(f"{function}Key", key.keysym)
    print(f"Changed {function} Key to {key.keysym}")
    close_all()
    open_settings_menu()
    save_to_file(True)


# - Images and buttons: -
# Escape menu:
bg_rectangle = PhotoImage(file="images/Backgrounds/BG_rectangle.png".replace("/", os.sep)).zoom(120, 120)
resume_img = PhotoImage(file="images/Menu/Button_resume.png".replace("/", os.sep)).zoom(5, 4)
save_img = PhotoImage(file="images/Menu/Button_save.png".replace("/", os.sep)).zoom(5, 4)
load_img = PhotoImage(file="images/Menu/Button_load.png".replace("/", os.sep)).zoom(5, 4)
main_menu_img = PhotoImage(file="images/Menu/Button_Main_menu.png".replace("/", os.sep)).zoom(5, 4)
settings_img = PhotoImage(file="images/Menu/Button_settings.png".replace("/", os.sep)).zoom(5, 4)
quit_img = PhotoImage(file="images/Menu/Button_quit.png".replace("/", os.sep)).zoom(5, 4)
resume_button = Button(scr, image=resume_img, highlightthickness=0, border=0,
                       activebackground="#000000", command=close_all)
save_button = Button(scr, image=save_img, highlightthickness=0, border=0,
                     activebackground="#000000", command=save_to_file)
load_button = Button(scr, image=load_img, highlightthickness=0, border=0, activebackground="#000000", command=load)
main_menu_button = Button(scr, image=main_menu_img, highlightthickness=0, border=0,
                          activebackground="#000000", command=open_main_menu)
settings_button = Button(scr, image=settings_img, highlightthickness=0, border=0,
                         activebackground="#000000", command=open_settings_menu)
quit_button = Button(scr, image=quit_img, highlightthickness=0, border=0, activebackground="#000000", command=exit)

title_img = PhotoImage(file="images/Menu/Title_screen_name.png".replace("/", os.sep)).zoom(8, 8)


# Setting menu:

toggle_fullscreen_img = PhotoImage(file="images/Menu/Button_toggle_fullscreen.png".replace("/", os.sep)).zoom(5, 4)
fullscreen_button = Button(scr, image=toggle_fullscreen_img, highlightthickness=0, border=0,
                           activebackground="#000000", command=toggle_fullscreen)

# Save menu:
file_var = IntVar()
file1_button = Button(scr, text="File 1", command=lambda: file_var.set(1), font=("Berlin Sans FB Demi", 16),
                      bg="#35AA57", relief="groove", padx=2, pady=2, bd=3, activebackground="#101010")
file2_button = Button(scr, text="File 2", command=lambda: file_var.set(2), font=("Berlin Sans FB Demi", 16),
                      bg="#35AA57", relief="groove", padx=2, pady=2, bd=3, activebackground="#101010")
file3_button = Button(scr, text="File 3", command=lambda: file_var.set(3), font=("Berlin Sans FB Demi", 16),
                      bg="#35AA57", relief="groove", padx=2, pady=2, bd=3, activebackground="#101010")

checkpoint_bg = PhotoImage(file="images/Backgrounds/checkpoint_bg.png".replace("/", os.sep)).zoom(9, 9)
