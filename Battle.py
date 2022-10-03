# from Core import *
from Player_class import *
from Enemy_class import *

in_turn = IntVar()


def end_turn():  # function for ending turns, spell in put is after this because spells use this function.
    place_main()
    for button in placed_buttons:
        button.configure(state="disabled")
    # data[1][0].health -= 10

    in_turn.set(1)


def find_target(targets):
    global placed_buttons
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = []
    target_index = IntVar()

    for target in targets:
        button = Button(scr, text=target.name, font=("", 15), borderwidth=0, highlightthickness=0, activebackground="#000000", command=lambda _=target: target_index.set(targets.index(_)))
        button.place(x=1920/(len(targets)+1)*(targets.index(target)+1)-48*3, y=845)

        placed_buttons.append(button)
    scr.wait_variable(target_index)
    return targets[target_index.get()]


from Spell_definitions import *

# imagery:
img_fight_button = PhotoImage(file="images/Battle_GUI/ButtonTest-Fight.png").zoom(6, 6)
img_magic_button = PhotoImage(file="images/Battle_GUI/ButtonTest-Magic.png").zoom(6, 6)
img_bag_button = PhotoImage(file="images/Battle_GUI/ButtonTest-Bag.png").zoom(6, 6)
img_action_button = PhotoImage(file="images/Battle_GUI/ButtonTest-Action.png").zoom(6, 6)
img_return_button = PhotoImage(file="images/Battle_GUI/ReturnButtonTest.png").zoom(3, 3)

img_heavy_attack_button = PhotoImage(file="images/Battle_GUI/ButtonTest-Heavy_atk.png").zoom(6, 6)
img_light_attack_button = PhotoImage(file="images/Battle_GUI/ButtonTest-Light_atk.png").zoom(6, 6)


img_battle_frame = PhotoImage(file="images/Battle_GUI/BattleMenuTest.png").zoom(5, 5)
img_text_label_frame = PhotoImage(file="images/Battle_GUI/TextLabelTest.png").zoom(5, 5)

# Global list definitions (need to be moved to other location):
placed_buttons = []
data = []


# Display functions:
def place_bg(location):
    scr.bg = PhotoImage(file="images/Backgrounds/"+location+".png").zoom(10, 10)
    scr.create_image(1920/2, 1080/2, image=scr.bg)

    scr.create_image(15+1890/2, 1080 // 4 * 3 + 80, image=img_battle_frame)
    scr.create_image(15+1890/2, 1080 // 4 * 3 - 130, image=img_text_label_frame)
    return_button.place(x=50, y=760)


def place_attack():
    global placed_buttons
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = [light_attack_button, heavy_attack_button]

    light_attack_button.place(x=1920 / 3 - 48 * 3, y=845)
    heavy_attack_button.place(x=1920 / 3 * 2 - 48 * 3, y=845)


def place_spells():
    global placed_buttons, data
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = []

    for spell in data[2].spells:
        button = Button(scr, image=spell.image, borderwidth=0, highlightthickness=0, activebackground="#000000", command=lambda _=spell: _.cast(data))
        button.place(x=1920/(len(data[2].spells)+1)*(data[2].spells.index(spell)+1)-48*3, y=845)

        placed_buttons.append(button)


def place_bag():
    global placed_buttons, data
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = []

    temp_x = 0
    temp_y = 1
    for item in data[2].inventory:
        button = Button(scr, image=item.image, borderwidth=0, highlightthickness=0,
                        activebackground="#31486F", command=lambda _=item: _.function)

        temp_y += 1
        if data[2].inventory.index(item) % 3 == 0:
            temp_x += 1
            temp_y = 1
        button.place(x=temp_x * 77 * 6 - 72 * 6 + 120, y=temp_y * 16 * 6 - 16 * 6 + 760)
        placed_buttons.append(button)


def place_main():
    global placed_buttons
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = [fight_button, magic_button, bag_button, action_button]
    fight_button.place(x=1920 / 5 - 48 * 3, y=845)
    magic_button.place(x=1920 / 5 * 2 - 48 * 3, y=845)
    bag_button.place(x=1920 / 5 * 3 - 48 * 3, y=845)
    action_button.place(x=1920 / 5 * 4 - 48 * 3, y=845)


def place_actions():
    global placed_buttons
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = []


# = Main button creation and placement =
fight_button = Button(scr, image=img_fight_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=place_attack)
magic_button = Button(scr, image=img_magic_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=place_spells)
bag_button = Button(scr, image=img_bag_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=place_bag)
action_button = Button(scr, image=img_action_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=place_actions)

return_button = Button(scr, image=img_return_button, borderwidth=0, highlightthickness=0, activebackground="#555555", bg="#555555", command=place_main)


# = Attack button creation =
light_attack_button = Button(scr, image=img_light_attack_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=end_turn)
heavy_attack_button = Button(scr, image=img_heavy_attack_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=end_turn)

inventory_frame = Frame(scr, width=scr.winfo_screenwidth() - 40, height=scr.winfo_screenheight() // 4 + 40, bg="#554466")
inventory_frame.pack_propagate(False)

# = Bag button creation and placement and other... requires revision =

# """  # ---------------- Display setting ----------------


def battle(players: list[Player], enemies: list[Foe], location):
    # Battle display prep
    global data
    place_bg(location)
    players[0].room.unload()
    players[0].health_label = Label(scr, text=players[0].health)
    players[0].health_label.place(x=50, y=1080 // 4 * 3 - 130)

    for foe in enemies:
        foe.image = Button(scr, image=foe.display, command=lambda _=foe: print(_.name), border=0, highlightthickness=0, activebackground="#000000", bg="#000000")
        foe.image.place(x=1920/(len(enemies)+1)*(enemies.index(foe)+1)-(enemies.index(foe)+1)*96*2.5+(96*1.25*len(enemies)), y=50)
        foe.health_label = Label(scr, text=foe.health)
        foe.health_label.place(x=1920/(len(enemies)+1)*(enemies.index(foe)+1)-(enemies.index(foe)+1)*96*2.5+(96*1.25*len(enemies)), y=50+96*2.5)

    # Decide turn order:
    turn_order = []
    for _ in range(0, 30):
        turn_order.append(0)

    for player in players:
        rng = randint(player.speed - 2, player.speed + 2)
        while turn_order[rng] != 0:
            rng = randint(player.speed - 2, player.speed + 2)
        turn_order[rng] = player

    for foe in enemies:
        rng = turn_order.index(players[0])
        while turn_order[rng] != 0:
            rng = randint(foe.speed - 2, foe.speed + 2)
        turn_order[rng] = foe

    try:
        while True:
            turn_order.remove(0)
    except ValueError:
        turn_order.reverse()

    # Battle:
    living_foe = enemies[0:len(enemies)]
    living_players = []
    for player in players:
        if player.health > 0:
            living_players.append(player)

    turn = 0
    turn_total = 0

    while len(living_players) > 0 and len(living_foe) > 0:
        battler = turn_order[turn]
        turn += 1
        turn_total += 1
        if turn >= len(turn_order):
            turn = 0

        if battler.health <= 0:
            continue

        # During turn
        for status_effect in battler.status:
            if status_effect.time == "start":
                status_effect.tick()
                if status_effect.count == 0:
                    battler.status.remove(status_effect)

        data = [living_players, living_foe, battler]
        if battler in players:
            place_main()
            for button in placed_buttons:
                button.configure(state="normal")
            scr.wait_variable(in_turn)

        battler.turn(data)

        for status_effect in battler.status:
            if status_effect.time == "end":
                status_effect.tick()
                if status_effect.count == 0:
                    battler.status.remove(status_effect)

        # After turn
        for battler in turn_order:
            battler.health_label.configure(text=battler.health)
            if battler.health <= 0:
                if battler in living_foe:
                    living_foe.remove(battler)
                    battler.image.configure(state="disabled")
                elif battler in living_players:
                    living_players.remove(battler)

        win.update_idletasks()
    players[0].room.load()
    for player in players:
        scr.tag_raise(player.disp.tag)
        player.status = []
    for foe in enemies:
        foe.health = foe.max_health
        foe.status = []
    for child in scr.winfo_children():
        for player in players:
            if child != player.disp:
                child.place_forget()
