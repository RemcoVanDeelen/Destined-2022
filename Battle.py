# from Core import *
from Player_class import *
from Enemy_class import *

in_turn = IntVar()


def end_turn():  # function for ending turns, spell in put is after this because spells use this function.
    place_main()
    for button in placed_buttons:
        button.configure(state="disabled")

    in_turn.set(1)


def find_target(targets):
    global placed_buttons
    for child in placed_buttons:
        child.place_forget()
    return_button.configure(state="disabled")
    placed_buttons = []
    target_index = IntVar()

    for target in targets:
        button = Button(scr, text=target.name, font=("", 15), borderwidth=0, highlightthickness=0, activebackground="#000000", command=lambda _=target: target_index.set(targets.index(_)))
        button.place(x=1920/(len(targets)+1)*(targets.index(target)+1)-48*3, y=845)

        placed_buttons.append(button)
    scr.wait_variable(target_index)
    return_button.configure(state="normal")
    return targets[target_index.get()]


def deal_damage(attacker=None, target=None, is_melee=True, exact_damage=0, percent_damage=0):
    base_damage = exact_damage + (target.max_health / 100 * percent_damage)

    pre_addition = 0
    dmg_multiplier = 1
    post_addition = 0

    # Attacker effects:
    for status_effect in attacker.status:
        if is_melee:                                                            # The following effects are only for melee attacks.
            if status_effect.effect in ["enchanted_weapon"]:                    # Checks for attacker effects that add DMG values after multiplier.
                post_addition += status_effect.tick(data)
            elif status_effect.effect in ["enchanted_weapon_empowered"]:        # Checks for attacker effects that add DMG values before multiplier.
                pre_addition += status_effect.tick(data)
            elif status_effect.effect in ["strength"]:                          # Checks for attacker effects that affect the DMG multiplier.
                dmg_multiplier += status_effect.tick(data)

            if status_effect.duration == 0:
                attacker.status.remove(status_effect)                           # Removes effects that are no longer in effect.

                if status_effect in ["enchanted_weapon", "enchanted_weapon_empowered"]:     # Sets cooldown for Enchant_weapon Spell in needs be.
                    _ = next((spell for spell in attacker.spells if spell.name == "enchant_weapon"), None)
                    _.cooldown = 3  # FILLER cooldown

    # Target effects:
    for status_effect in target.status:
        if status_effect.effect in ["defending", "resistance", "weakened"]:     # Checks for target effects that affect the DMG multiplier.
            dmg_multiplier -= status_effect.tick(data)
        elif status_effect.effect in ["shielded"]:                              # Checks if target can be damaged this turn. (shielded effect)
            dmg_multiplier = 0
            post_addition = 0
            base_damage = 0
            pre_addition = 0
            status_effect.tick(data)

        if status_effect.duration == 0:
            target.status.remove(status_effect)                                 # Removes effects that are no longer in effect.

    # total damage calculation:
    damage = round((base_damage + pre_addition) * dmg_multiplier + post_addition)
    target.health -= damage                                                     # Deals damage.

    try:                                          # Temporary statement.
        print("=", attacker.tag, "dealt", [damage], "damage to", target.name)
    except AttributeError:
        print("-", attacker.name, "dealt", [damage], "damage to", target.tag)

    return damage


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

pointer_img = PhotoImage(file="images/Battle_GUI/item_pointer.png").zoom(5, 5)

# Global list definitions (need to be moved to other location):
placed_buttons = []
data = []


# Display functions:
def place_bg(location):
    scr.bg = PhotoImage(file="images/Backgrounds/"+location+".png").zoom(10, 10)
    scr.create_image(1920/2, 1080/2, image=scr.bg, tag="bg_img")

    scr.create_image(15+1890/2, 1080 // 4 * 3 + 80, image=img_battle_frame)
    scr.create_image(15+1890/2, 1080 // 4 * 3 - 130, image=img_text_label_frame)
    return_button.place(x=50, y=760)


def place_attack():
    global placed_buttons
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = [light_attack_button, heavy_attack_button]

    if data[2].stamina < 5:
        light_attack_button.configure(state="disabled")
    else:
        light_attack_button.configure(state="normal")
    if data[2].stamina < 8:
        heavy_attack_button.configure(state="disabled")
    else:
        heavy_attack_button.configure(state="normal")

    light_attack_button.place(x=1920 / 3 - 48 * 3, y=845)
    heavy_attack_button.place(x=1920 / 3 * 2 - 48 * 3, y=845)


def place_spells():
    global placed_buttons, data
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = []

    for spell in data[2].spells:
        button = Button(scr, image=spell.image, borderwidth=0, highlightthickness=0, activebackground="#000000", command=lambda _=spell: _.use(data))
        button.place(x=1920/(len(data[2].spells)+1)*(data[2].spells.index(spell)+1)-48*3, y=845)

        if spell.cooldown > 0:
            button.configure(state="disabled")

        placed_buttons.append(button)


def place_bag():
    global placed_buttons, data
    for child in placed_buttons:
        child.place_forget()

    pointer = scr.create_image(-100, -100, image=pointer_img, tag="pointer")

    temp_x = 0
    temp_y = 1
    item_index = 0
    for item in data[2].inventory:
        button = Button(scr, image=item.image, borderwidth=0, highlightthickness=0,
                        activebackground="#31486F", command=lambda _=item: _.use(data))

        if item.cooldown > 0:
            button.configure(state="disabled")

        temp_y += 1
        if item_index % 3 == 0:
            temp_x += 1
            temp_y = 1
        button.place(x=temp_x * 77 * 6 - 72 * 6 + 120, y=temp_y * 16 * 6 - 16 * 6 + 760)

        button.bind("<Enter>", lambda bound, x=temp_x, y=temp_y: scr.moveto(pointer, x=x*460-10, y=y*97+675))
        button.bind("<Leave>", lambda bound, x=temp_x, y=temp_y: scr.moveto(pointer, x=-100, y=-100))
        placed_buttons.append(button)
        item_index += 1


def place_main():
    global placed_buttons
    for child in placed_buttons:
        try:
            child.place_forget()
        except AttributeError:
            scr.delete(child)
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


# melee attack functions
def light_attack():
    deal_damage(attacker=data[2], target=find_target(data[1]), exact_damage=7)  # FILLER damage.
    data[2].stamina -= 6                        # FILLER stamina cost.
    end_turn()


def heavy_attack():
    deal_damage(attacker=data[2], target=find_target(data[1]), exact_damage=12)  # FILLER damage.
    data[2].stamina -= 8                        # FILLER stamina cost.

    end_turn()


# = Main button creation and placement =
fight_button = Button(scr, image=img_fight_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=place_attack)
magic_button = Button(scr, image=img_magic_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=place_spells)
bag_button = Button(scr, image=img_bag_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=place_bag)
action_button = Button(scr, image=img_action_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=place_actions)

return_button = Button(scr, image=img_return_button, borderwidth=0, highlightthickness=0, activebackground="#555555", bg="#555555", command=place_main)


# = Attack button creation =
light_attack_button = Button(scr, image=img_light_attack_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=light_attack)
heavy_attack_button = Button(scr, image=img_heavy_attack_button, borderwidth=0, highlightthickness=0, activebackground="#000000", command=heavy_attack)

inventory_frame = Frame(scr, width=scr.winfo_screenwidth() - 40, height=scr.winfo_screenheight() // 4 + 40, bg="#554466")
inventory_frame.pack_propagate(False)

# = Bag button creation and placement and other... requires revision =

# """  # ---------------- Display setting ----------------


def battle(players: list[Player], enemies: list[Foe], location):
    if enemies == [Dummy]:
        players[0].health = 1

    # Battle display prep

    global data
    place_bg(location)
    players[0].room.unload()
    players[0].health_label = Label(scr, text="HP="+str(players[0].health))
    players[0].health_label.place(x=50, y=1080 // 4 * 3 - 130)
    players[0].stamina_label = Label(scr, text="STA="+str(players[0].stamina))
    players[0].stamina_label.place(x=100, y=1080 // 4 * 3 - 130)

    for foe in enemies:
        foe.image = Button(scr, image=foe.display, command=lambda _=foe: print(_.name), border=0, highlightthickness=0, activebackground="#000000", bg="#000000")
        foe.image.place(x=1920/(len(enemies)+1)*(enemies.index(foe)+1)-(enemies.index(foe)+1)*96*2.5+(96*1.25*len(enemies)), y=50)
        foe.health_label = Label(scr, text="HP="+str(foe.health))
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

    print("\n - Battle start -",
          "\n Players: ", end="")
    for _ in players:
        print(_.tag, end=",")
    print("\n Enemies: ", end="")
    for _ in enemies:
        print(_.name, end=", ")
    print("\n")

    while len(living_players) > 0 and len(living_foe) > 0:
        battler = turn_order[turn]
        turn += 1
        turn_total += 1
        if turn >= len(turn_order):
            turn = 0
        print("/", turn_total, "\\")

        if battler.health <= 0:
            print(battler.name, "is dead")
            continue

        data = [living_players, living_foe, battler]

        # During turn
        for status_effect in battler.status:
            if status_effect.time == "start":
                status_effect.tick(data)
                if status_effect.duration == 0:
                    battler.status.remove(status_effect)

        data = [living_players, living_foe, battler]
        has_stasis = next((effect for effect in battler.status if effect.effect == "stasis_effect"), None)
        if has_stasis is not None:
            has_stasis.tick(data)
            if has_stasis.duration <= 0:
                battler.status.remove(has_stasis)
        else:
            if battler in players:
                place_main()
                for button in placed_buttons:
                    button.configure(state="normal")
                for spell in battler.spells:
                    if spell.cooldown > 0:
                        spell.cooldown -= 1

                checked_items = []
                for item in battler.inventory:
                    if item.cooldown > 0:
                        if item not in checked_items:
                            item.cooldown -= 1
                            checked_items.append(item)
                scr.wait_variable(in_turn)

            battler.turn(data)

        data = [living_players, living_foe, battler]

        for status_effect in battler.status:
            if status_effect.time == "end":
                status_effect.tick(data)
                if status_effect.duration == 0:
                    battler.status.remove(status_effect)

        data = [living_players, living_foe, battler]

        # After turn
        for battler in turn_order:
            for status_effect in battler.status:
                if status_effect.time == "always":
                    status_effect.tick([living_players, living_foe, battler])
                    if status_effect.duration == 0:
                        battler.status.remove(status_effect)
            battler.health_label.configure(text="HP="+str(battler.health))
            if battler in living_players:
                battler.stamina_label.configure(text="STA=" + str(battler.stamina))

            if battler.health <= 0:
                if battler in living_foe:
                    living_foe.remove(battler)
                    battler.image.configure(state="disabled")
                    for player in players:
                        player.soul += battler.soul
                elif battler in living_players:
                    living_players.remove(battler)

        win.update_idletasks()

    print("\n - Battle concluded -")
    players[0].room.load()
    for player in players:
        scr.tag_raise(player.disp.tag)
        player.status = []
        for spell in player.spells:
            spell.cooldown = 0
            if spell.name == "slow_time":
                spell.cooldown = 1
    for foe in enemies:
        foe.health = foe.max_health
        foe.status = []
    for child in scr.winfo_children():
        for player in players:
            if child != player.disp:
                child.place_forget()
    scr.delete("bg_img")
