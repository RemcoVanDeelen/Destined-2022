"""
Battle.py
--

This file holds the general battle functionality.
for the status effect, player action and enemy related functionality,
see Status_effects.py, Action_definition.py and Enemy_class.py respectively.

This file holds four sets of functions (in order):
 * General in-turn functions,
 * Display configuration,
 * Unique actions and info card display,
 * Main battle function.

"""

from Player_class import *
from Status_effects import *
import Core
from random import randint

in_turn = IntVar()  # variable for player turn detection.


# General in-turn functions:
def end_turn(stamina_return):
    """
    Function for ending turns.
    """

    # Returns menu to main buttons and disables them until start of next turn.
    place_main()
    for button in placed_buttons:
        button.configure(state="disabled")

    # Adds stamina_return to player.stamina.
    data[2].stamina += stamina_return
    if data[2].stamina > data[2].max_stamina:
        data[2].stamina = data[2].max_stamina

    # Detects staminaless effect and handles it correctly.
    for status in data[2].status:
        if status.effect == "staminaless":
            status.tick(data)
            if status.duration == 0:
                data[2].status.remove(status)
                data[2].light_atk_cost += 2
                data[2].heavy_atk_cost += 2

    # alters variable for tkinter wait variable function in battle function.
    in_turn.set(1)


def find_target(targets):
    """
    Function for asking the player to pick a target enemy from targets list.
    """
    # removes current buttons from display:
    global placed_buttons
    for child in placed_buttons:
        child.place_forget()
    return_button.configure(state="disabled")
    placed_buttons = []
    target_index = IntVar()

    # Adds buttons for each target in targets list
    for target in targets:
        # The button placed on screen shows the target's name and
        # the button command sets the target_index variable to the target's index from list.
        button = Button(scr, text=target.name, font=("Berlin Sans FB Demi", 16), bd=1, highlightthickness=0,
                        activebackground="#339A75", command=lambda _=target: target_index.set(targets.index(_)),
                        bg="#328964", height=2, width=18, relief="ridge")

        button.place(x=1920/(len(targets)+1)*(targets.index(target)+1), y=845, anchor="center")
        placed_buttons.append(button)

    # Wait variable until a button is pressed, then return to main and return target from list.
    scr.wait_variable(target_index)
    place_main()
    return_button.configure(state="normal")
    return targets[target_index.get()]


def deal_damage(attacker=None, target=None, is_melee=True, exact_damage=0, percent_damage=0):
    """
    Function for dealing damage to a target.
    This function calculates the damage dealt based on status effects and base damages.

    Calculation:

    base damage = exact damage + (target max health / 100 * percent damage)
    total damage = (base damage + pre addition) * multiplier + post addition
    round(total damage)

    pre addition, post addition and multiplier are modified by
    status effects from both the attacker and the target.
    With their base values being 0 (additions) and 1 (multiplier).

    :param attacker: Attacker object (player/foe),
    :param target: Target object (player/foe),
    :param is_melee: Boolean value dictating attack type,
    :param exact_damage: Base exact damage integer,
    :param percent_damage: Base percent damage integer,

    :returns: Total damage dealt
    """

    # base variable calculation:
    base_damage = exact_damage + (target.max_health / 100 * percent_damage)

    pre_addition = 0
    dmg_multiplier = 1
    post_addition = 0

    # Attacker effects:
    if attacker is not None:
        for status_effect in attacker.status:
            if is_melee:

                # The following effects are only for melee attacks.
                if status_effect.effect in ["enchanted_weapon", "opponent_enchanted_weapon"]:
                    # Checks for attacker effects that add DMG values after multiplier (post_addition).
                    post_addition += status_effect.tick(data)

                elif status_effect.effect in ["enchanted_weapon_empowered"]:
                    # Checks for attacker effects that add DMG values before multiplier (pre_addition).
                    pre_addition += status_effect.tick(data)

                elif status_effect.effect in ["strength"]:
                    # Checks for attacker effects that affect the DMG multiplier (dmg_multiplier).
                    dmg_multiplier += status_effect.tick(data)

                if status_effect.duration == 0:
                    # Removes effects that are no longer in effect.
                    attacker.status.remove(status_effect)

                    if status_effect in ["enchanted_weapon", "enchanted_weapon_empowered"]:
                        # Sets cooldown for Enchant_weapon Spell if needs be.
                        _ = next((spell for spell in attacker.spells if spell.name == "enchant_weapon"), None)
                        _.cooldown = 3 + attacker.focus if type(attacker) == Player else 0

    # Target effects:
    for status_effect in target.status:
        if status_effect.effect in ["defending", "resistance", "weakened", "barrier"]:
            # Checks for target effects that affect the DMG multiplier (dmg_multiplier).
            dmg_multiplier -= status_effect.tick(data)

        elif status_effect.effect in ["shielded"]:
            # Checks if target can be damaged this turn. (shielded effect)
            dmg_multiplier = 0
            post_addition = 0
            base_damage = 0
            pre_addition = 0
            status_effect.tick(data)

        if status_effect.duration == 0:
            # Removes effects that are no longer in effect.
            target.status.remove(status_effect)

    # Final damage calculation and subtraction from target health:
    damage = round((base_damage + pre_addition) * dmg_multiplier + post_addition)
    target.health -= damage

    # action log:
    try:
        print("=", attacker.tag, "dealt", [damage], "damage to", target.name)
    except AttributeError:
        print("-", attacker.name, "dealt", [damage], "damage to", target.tag)

    # return total damage dealt, not including damage below 0 health.
    return damage


# Display configuration:
# imagery:
img_fight_button = PhotoImage(file="images/Battle_GUI/Button-Fight.png".replace("/", os.sep)).zoom(6, 6)
img_magic_button = PhotoImage(file="images/Battle_GUI/Button-Magic.png".replace("/", os.sep)).zoom(6, 6)
img_bag_button = PhotoImage(file="images/Battle_GUI/Button-Bag.png".replace("/", os.sep)).zoom(6, 6)
img_action_button = PhotoImage(file="images/Battle_GUI/Button-Action.png".replace("/", os.sep)).zoom(6, 6)
img_return_button = PhotoImage(file="images/Battle_GUI/ReturnButton.png".replace("/", os.sep)).zoom(3, 3)

img_heavy_attack_button = PhotoImage(file="images/Battle_GUI/Button-Heavy_atk.png".replace("/", os.sep)).zoom(6, 6)
img_light_attack_button = PhotoImage(file="images/Battle_GUI/Button-Light_atk.png".replace("/", os.sep)).zoom(6, 6)

img_defend_button = PhotoImage(file="images/Battle_GUI/Button-Defend.png".replace("/", os.sep)).zoom(6, 6)
img_run_button = PhotoImage(file="images/Battle_GUI/Button-Run.png".replace("/", os.sep)).zoom(6, 6)

img_battle_frame = PhotoImage(file="images/Battle_GUI/BattleMenu.png".replace("/", os.sep)).zoom(5, 5)
img_text_label_frame = PhotoImage(file="images/Battle_GUI/TextLabel.png".replace("/", os.sep)).zoom(5, 5)

pointer_img = PhotoImage(file="images/Battle_GUI/item_pointer.png".replace("/", os.sep)).zoom(5, 5)

# empty variables:
placed_buttons = []
data = []


# Display functions:
def place_bg(location):
    """
    Places background images based on location and places return button.
    """

    Core.can_escape = False

    scr.bg = PhotoImage(file="images/Backgrounds/"+location+".png".replace("/", os.sep)).zoom(10, 10)
    scr.create_image(1920/2, 1080/2, image=scr.bg, tag="bg_img")

    scr.create_image(15+1890/2, 1080 // 4 * 3 + 80, image=img_battle_frame, tag="battle_frame")
    scr.create_image(15+1890/2, 1080 // 4 * 3 - 130, image=img_text_label_frame, tag="label_frame")
    return_button.place(x=50, y=760)


def place_attack():
    """
    Removes currently placed buttons and places attack buttons.
    Disables/enables attack buttons based on met stamina requirements.
    """

    global placed_buttons
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = [light_attack_button, heavy_attack_button]

    if data[2].stamina < data[2].light_atk_cost:
        light_attack_button.configure(state="disabled")
    else:
        light_attack_button.configure(state="normal")
    if data[2].stamina < data[2].heavy_atk_cost:
        heavy_attack_button.configure(state="disabled")
    else:
        heavy_attack_button.configure(state="normal")

    light_attack_button.place(x=1920 / 3 - 48 * 3, y=845)
    heavy_attack_button.place(x=1920 / 3 * 2 - 48 * 3, y=845)


def place_spells():
    """
    Removes currently placed buttons and places spell buttons.
    Disables spell buttons based on spell cooldown.
    """

    global placed_buttons, data
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = []

    learned_spells = data[2].spells.copy()
    while None in learned_spells:
        learned_spells.remove(None)

    for spell in learned_spells:
        button = Button(scr, image=spell.image, borderwidth=0, highlightthickness=0, activebackground="#000000",
                        command=lambda _=spell: _.use(data), bg="#006666")
        button.place(x=1920/(len(learned_spells)+1)*(learned_spells.index(spell)+1)-48*3, y=845)

        if spell.cooldown > 0 or spell.name in ["focus", "agility", "stamina"] or \
                spell.name == "chaotic_strike" and data[2].stamina < spell.use([None, None, data[2]]):
            button.configure(state="disabled")

        placed_buttons.append(button)


def place_bag():
    """
    Removes currently placed buttons and places item buttons.
    Disables item buttons based on item cooldown.
    Binds arrow icon to item button upon hover.
    """

    global placed_buttons, data
    for child in placed_buttons:
        child.place_forget()

    pointer = scr.create_image(-100, -100, image=pointer_img, tag="pointer")

    temp_x = 0
    temp_y = 1
    item_index = 0
    for item in data[2].inventory:
        button = Button(scr, image=item.image, borderwidth=0, highlightthickness=0, bg="#104666",
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
    """
    Removes currently placed buttons and places main buttons.
    """

    global placed_buttons
    for child in placed_buttons:
        child.place_forget()

    placed_buttons = [fight_button, magic_button, bag_button, action_button]

    fight_button.place(x=1920 / 5 - 48 * 3, y=845)
    magic_button.place(x=1920 / 5 * 2 - 48 * 3, y=845)
    bag_button.place(x=1920 / 5 * 3 - 48 * 3, y=845)
    action_button.place(x=1920 / 5 * 4 - 48 * 3, y=845)


def place_actions():
    """
    Removes currently placed buttons and places action buttons.
    """

    global placed_buttons
    for child in placed_buttons:
        child.place_forget()
    placed_buttons = [defend_button, run_button]

    defend_button.place(x=1920 / 3 - 48 * 3, y=845)
    run_button.place(x=1920 / 3 * 2 - 48 * 3, y=845)


# = Main button creation and placement =
fight_button = Button(scr, image=img_fight_button, borderwidth=0, highlightthickness=0,
                      activebackground="#000000", command=place_attack)
magic_button = Button(scr, image=img_magic_button, borderwidth=0, highlightthickness=0,
                      activebackground="#000000", command=place_spells)
bag_button = Button(scr, image=img_bag_button, borderwidth=0, highlightthickness=0,
                    activebackground="#000000", command=place_bag)
action_button = Button(scr, image=img_action_button, borderwidth=0, highlightthickness=0,
                       activebackground="#000000", command=place_actions)

return_button = Button(scr, image=img_return_button, borderwidth=0, highlightthickness=0,
                       activebackground="#505F8C", bg="#505F8C", command=place_main)


# Unique actions and info card display:
# Melee attack functions
def light_attack():
    """
    Action function for light attack.

    Deals base exact damage based on player damage stat * 0.7.
    Costs player light_atk_cost stat as stamina.
    Ends turn without stamina gain.
    """

    deal_damage(attacker=data[2], target=find_target(data[1]), exact_damage=int(data[2].damage * 0.7))
    data[2].stamina -= data[2].light_atk_cost
    end_turn(0)


def heavy_attack():
    """
    Action function for heavy attack.

    Deals base exact damage based on player damage stat * 1.3.
    Costs player heavy_atk_cost stat as stamina.
    Ends turn without stamina gain.
    """

    deal_damage(attacker=data[2], target=find_target(data[1]), exact_damage=int(data[2].damage * 1.3))
    data[2].stamina -= data[2].heavy_atk_cost
    end_turn(0)


# = Attack button creation =
light_attack_button = Button(scr, image=img_light_attack_button, borderwidth=0, highlightthickness=0,
                             activebackground="#000000", command=light_attack, bg="#AA4545")
heavy_attack_button = Button(scr, image=img_heavy_attack_button, borderwidth=0, highlightthickness=0,
                             activebackground="#000000", command=heavy_attack, bg="#AA4545")

inventory_frame = Frame(scr, width=scr.winfo_screenwidth() - 40, height=scr.winfo_screenheight() // 4 + 40,
                        bg="#554466")
inventory_frame.pack_propagate(False)

# = Action creation =


def defend():
    """
    Action function for defend action.

    Adds defending status effect to player for 1 turn.
    Ends turn with 4 stamina gain.
    """

    global data
    data[2].status.append(Effect("start", "defending", 1))
    print("Player defends")
    end_turn(4)


def run():
    """
    Action function run action.

    Ends battle by setting data list to ["exit"] and ending player turn.
    """

    global data
    print("Player ran away")
    data = ["exit"]
    in_turn.set(1)


defend_button = Button(scr, image=img_defend_button, borderwidth=0, highlightthickness=0,
                       activebackground="#000000", command=defend)
run_button = Button(scr, image=img_run_button, borderwidth=0, highlightthickness=0,
                    activebackground="#000000", command=run)


# Foe info card display:
def foe_info_display(foe):
    """
    Function bound to foe display, swaps display for stats and descriptions in canvas (info card).

    When the player clicks the foe's image display this function:
    Creates a canvas inside the foe image display.
    Adds text to canvas providing info on the foe's:
     * Name,
     * Current stats and status effects,
     * description (str attribute in Foe class).

    When the cursor leaves the area of the image/canvas the canvas is destroyed.

    """
    canvas = Canvas(foe.image, bg="#150808")
    canvas.pack()
    status_text = "["
    if len(foe.status) != 0:
        for effect in foe.status:
            status_text += effect.effect.replace("_effect", "").replace("opponent_", "").replace(
                "_empowered", " {+}").replace("_", " ")
            if len(foe.status)-2 >= foe.status.index(effect):
                status_text += ", "
    else:
        status_text += " - "
    status_text += "]"
    canvas.create_text(120, 120, font=("", 11), justify="center", fill="#FFFFFF",
                       text=f"-- {foe.name.upper()} --\n"
                            f"Health - {foe.health:>2} / {foe.max_health:<2}\n"
                            f"{status_text}\n"
                            f" Speed - {foe.speed:<11}\n"
                            f"    Soul - {foe.soul:<11}\n"
                            f"    Gold - {foe.gold[0]}~{foe.gold[1]:<7}\n\n"
                            f"{foe.description}")
    foe.image.bind("<Leave>", lambda _: canvas.destroy())


# Main battle function:
def battle(players: list[Player], enemies: list, location):
    """
    This is the main function for starting and loading battles.

    It runs a loop for each battler in the turn order list and processes
    its turn-based status effects and health.
    It also calls all functions to set up the GUI.

    :param players: list of players, cannot be more than one player.
    :param enemies: list of enemies, should be between 1~3 enemies.
    :param location: location for background image.
    """
    # unbinding keybinds:
    win.unbind(f"<{Settings.upKey}>")
    win.unbind(f"<{Settings.leftKey}>")
    win.unbind(f"<{Settings.downKey}>")
    win.unbind(f"<{Settings.rightKey}>")
    win.unbind(f"<{Settings.interactKey}>")

    # Battle display prep:

    global data
    place_bg(location)
    players[0].room.unload()

    # player stats:
    scr.create_rectangle(50, 650, 350, 675, tag="Health_bg", fill="#333333")
    scr.create_rectangle(50, 650, 350, 675, tag="Health_border")
    scr.create_rectangle(50, 710, 350, 685, tag="Stamina_bg", fill="#333333")
    scr.create_rectangle(50, 710, 350, 685, tag="Stamina_border")

    # Enemy images and labels:
    for foe in enemies:
        foe.image = Button(scr, image=foe.display, command=lambda _=foe: foe_info_display(_), border=2, relief="flat",
                           highlightthickness=0, activebackground="#000000", bg="#000000")
        foe.image.place(x=1920/(len(enemies)+1)*(enemies.index(foe)+1), y=50, anchor="n")
        foe.image.pack_propagate(False)
        foe.health_label = Label(scr, text=f"{foe.name} | HP:  {foe.health}".center(33), bd=1, relief="solid",
                                 font=("Berlin Sans FB Demi", 14), fg="#601010", bg="#7A7AAA")
        foe.health_label.place(x=1920/(len(enemies)+1)*(enemies.index(foe)+1), y=50+96*2.5+3, anchor="n")

    # Decide turn order:
    # Creates a list filled with 30 zeros to later replace with the battlers:
    turn_order = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # For the battler in the 'players' and 'enemies' list it adds an integer between -2 and +2 to its speed stat.
    # The resulting integer is this battler's index in the turn order list.
    # If this index was already taken its re-rolls the randint.
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

    # Now all remaining zeros are removed from the turn_order list.
    # Then it reverses the order of the list giving us the final turn order for the rest of the battle.
    try:
        while True:
            turn_order.remove(0)
    except ValueError:
        turn_order.reverse()

    # Setting up two lists for the current living battlers:
    living_foe = enemies[0:len(enemies)]
    living_players = []
    for player in players:
        if player.health > 0:
            living_players.append(player)

    # Battle start:
    turn = 0
    turn_total = 0

    print("\n - Battle start -",
          "\n Players: ", end="")
    for _ in players:
        print(_.tag, end=",")
    print("\n Enemies: ", end="")
    for _ in enemies:
        print(_.name, end=", ")

    # Battle loop start:
    while len(living_players) > 0 and len(living_foe) > 0:
        # Display a border around the current battler's image (in case of foe).
        try:
            if turn == 0:
                temp = len(turn_order)-1
            else:
                temp = turn-1
            turn_order[temp].image.configure(relief="flat")
        except AttributeError:
            pass

        # Current battler setup:
        battler = turn_order[turn]
        turn += 1
        turn_total += 1
        if turn >= len(turn_order):
            turn = 0

        if battler in players:
            print("\n/", turn_total, "\\", "= Player")
        else:
            print("\n/", turn_total, "\\", "-", battler.name)
            battler.image.configure(relief="groove")

        if battler.health <= 0:
            print(battler.name, "is dead")
            continue

        # The 'data' list is used by almost all functions that are called and golds the data as follows:
        data = [living_players, living_foe, battler]

        # First status effect calculation:
        for status_effect in battler.status:
            if status_effect.time == "start":
                status_effect.tick(data)
                if status_effect.duration == 0 or status_effect.effect == "defending":
                    battler.status.remove(status_effect)

        # Display update for all labels and stat displays:
        for combatant in turn_order:
            if combatant in living_players:
                scr.delete("Health_display", "Stamina_display", "Health_label", "Stamina_label", "Status_label")
                scr.create_rectangle(50, 650, 50 + players[0].health / players[0].max_health * 300, 675,
                                     fill="#D20B0B", tag="Health_display")
                scr.create_text(383, 662.5, text=f"{players[0].health} / {players[0].max_health}",
                                tag="Health_label", font=("", 11, "italic"))

                scr.create_rectangle(50, 710, 50 + players[0].stamina / players[0].max_stamina * 300, 685,
                                     fill="#087492", tag="Stamina_display")
                scr.create_text(383, 697.5, text=f"{players[0].stamina} / {players[0].max_stamina}",
                                tag="Stamina_label", font=("", 11, "italic"))
                status_text = "["
                if len(players[0].status) != 0:
                    for effect in players[0].status:
                        status_text += effect.effect.replace("_effect", "").replace("opponent_", "").replace(
                            "_empowered", " {+}").replace("_", " ")
                        if len(players[0].status) - 2 >= players[0].status.index(effect):
                            status_text += ", "
                scr.create_text(1920 - 250, 680, width=200, text=status_text+"]", tag="Status_label", justify="left",
                                font=("Berlin Sans FB Demi", 12))

            else:
                combatant.health_label.configure(text=f"{combatant.name} | HP:  {combatant.health}".center(33))

        # Stasis effect calculation:
        data = [living_players, living_foe, battler]
        has_stasis = next((effect for effect in battler.status if effect.effect == "stasis_effect"), None)
        turn_delay = 0
        if has_stasis is not None:
            has_stasis.tick(data)
            if has_stasis.duration <= 0:
                battler.status.remove(has_stasis)
            print(battler.name if battler in living_foe else "Player", "couldn't move.")
        else:
            # Now comes the actual turn:
            if battler in players:
                # place buttons:
                place_main()
                for button in placed_buttons:
                    button.configure(state="normal")

                # Calculate cool-downs:
                for spell in battler.spells:
                    if spell is not None:
                        if spell.cooldown > 0:
                            spell.cooldown -= 1

                checked_items = []
                for item in battler.inventory:
                    if item.cooldown > 0:
                        if item not in checked_items:
                            item.cooldown -= 1
                            checked_items.append(item)

                # Wait for end of player interaction:
                scr.wait_variable(in_turn)
            else:
                if battler.name != "Training dummy":
                    # This is the time that the game waits on this Foe's turn. (mostly visually)
                    turn_delay = 450
                # The training dummy has the unique case that it wastes no time in battle. (It generally does not move)

            # Finally it calls the .turn() function for the battler.
            battler.turn(data)
            # In the case of a foe this calls its Ai_turn function.
            # In the case of the player it simply passes.

        # If the data list is set to ["exit"] the battle is immediately ended (with a normal data list).
        # This happens when the player uses the 'RUN' action.
        if data == ["exit"]:
            data = [living_players, living_foe, battler]
            break

        data = [living_players, living_foe, battler]

        # End of turn status effect calculation:
        for status_effect in battler.status:
            if status_effect.time == "end":
                status_effect.tick(data)
                if status_effect.duration == 0:
                    battler.status.remove(status_effect)

        data = [living_players, living_foe, battler]

        # The turn has now concluded.
        for battler in turn_order:
            # Now we process any battler with an always ticking status effect (such as Venom_empowered).
            for status_effect in battler.status:
                if status_effect.time == "always":
                    status_effect.tick([living_players, living_foe, battler])
                    if status_effect.duration == 0:
                        battler.status.remove(status_effect)

            # And remove defeated battlers from the living lists.
            if battler.health <= 0:
                if battler in living_foe:
                    # in case of Foe, their image is also disabled and their soul is granted to the player.
                    living_foe.remove(battler)
                    battler.image.configure(state="disabled")
                    for player in players:
                        player.soul += battler.soul
                elif battler in living_players:
                    living_players.remove(battler)

        # proceed to next loop after turn delay (450 ms, see actual turn calculation).
        win.after(turn_delay, win.update_idletasks())

    # The loop has been broken and the battle has now concluded:
    print("\n - Battle concluded -")
    players[0].room.load()

    if players[0].health <= 0:
        # process player death:
        players[0].warp([players[0].checkpoint[0], players[0].checkpoint[1]], players[0].checkpoint[2])
        players[0].health = players[0].max_health
        players[0].gold = round(players[0].gold/2)
        print(" Caused by Player death")
    else:
        # process victory:
        print(" Gold earned: ", end="")
        gold = 0
        for foe in enemies:
            if foe.health <= 0:
                gold += randint(foe.gold[0], foe.gold[1])
        print(gold, end=",\n")
        players[0].gold += gold

    # always add soul for defeated enemies:
    print(" Soul earned: ", end="")
    for foe in enemies:
        if foe.health <= 0:
            print(foe.soul, ", ", end="", sep="")

    print("\n")

    for player in players:
        # reset player for movement and next battle correctly:
        scr.tag_raise(player.disp.tag)
        player.status = []
        for spell in player.spells:
            if spell is not None:
                spell.cooldown = 0
        player.stamina = player.max_stamina
        for item in player.inventory:
            item.cooldown = 0
        # calculates Level-up:
        while player.soul >= 20:
            player.level += 1
            print(f"Player level increased to {player.level}!\n")
            player.max_health += 5
            player.health += 5
            player.damage += 1 if player.level % 3 == 0 else 0
            player.soul -= 20

    # Reset Enemies for next battle:
    for foe in enemies:
        foe.health = foe.base_max_health
        foe.max_health = foe.base_max_health
        foe.met_requirements = []
        foe.turn_prior = 'passed'
        foe.status = []
    for child in scr.winfo_children():
        for player in players:
            if child != player.disp:
                child.place_forget()

    # Rebind keys:
    Core.can_escape = True
    win.bind(f"<{Settings.upKey}>", players[0].move)
    win.bind(f"<{Settings.leftKey}>", players[0].move)
    win.bind(f"<{Settings.downKey}>", players[0].move)
    win.bind(f"<{Settings.rightKey}>", players[0].move)
    win.bind(f"<{Settings.interactKey}>", players[0].interact)

    # Delete images:
    scr.delete("battle_frame", "label_frame", "bg_img", "Health_display", "Health_border", "Health_label",
               "Stamina_display", "Stamina_border", "Stamina_label", "Health_bg", "Stamina_bg", "Status_label")

    # Player location correction:
    players[0].warp(players[0].position, players[0].room)
