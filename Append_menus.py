"""
Append_menus.py
--

This file holds append menus and related functions such as learn_spell() and exchange().

An Append menu is any menu that displays and/or changes any player related list (e.g. inventory or spells).
These menus include:
 * Stores,
 * Displays,
 * Open_inventory,

"""

import sys
from Action_definitions import *
import Core


Storefront_bg = PhotoImage(file="images/Backgrounds/Storefront_bg_filter.png".replace("/", os.sep)).zoom(120, 120)
Inventory_bg = PhotoImage(file="images/Backgrounds/Inventory_menu_bg.png".replace("/", os.sep)).zoom(120, 120)


# item store:
def open_store(player, store: str):
    """
    This function opens stores (who would have guessed).

    Player inventory is shown on the right with buttons for selling items at 0.8x value.\n
    Store items are shown on the left with stock labels and buttons for buying items at store[0]x value.\n
    In the center the player gold is displayed paired with a button to close the menu. \n

    For store definitions look below exchange() definition. \n
    The store parameter required here is the string name of the list variable.

    """
    # unbind keys.
    win.unbind(f"<{Settings.inventoryKey}>")
    win.unbind(f"<{Settings.upKey}>")
    win.unbind(f"<{Settings.leftKey}>")
    win.unbind(f"<{Settings.downKey}>")
    win.unbind(f"<{Settings.rightKey}>")
    win.unbind(f"<{Settings.interactKey}>")
    Core.can_escape = False

    # show general store:
    all_widgets = [scr.create_image(960, 540, image=Storefront_bg)]
    close_store_button = Button(scr, text="   Close Store   ", command=lambda: close_store(player, all_widgets),
                                font=["Berlin Sans FB Demi", 18], bg="#30A555")
    close_store_button.place(x=960, y=640, anchor="center")
    all_widgets.append(close_store_button)
    player_gold_label = Label(scr, text=f" Gold = {player.gold} G ",
                              font=["Berlin Sans FB Demi", 18], bg="#151515", fg="#FFAF00")
    player_gold_label.place(x=960, y=690, anchor="center")
    all_widgets.append(player_gold_label)

    # show player inventory.  -->>
    for ind in range(0, len(player.inventory)):
        item = player.inventory[ind]
        all_widgets.append(scr.create_image(1380, 177+200*ind/3, image=item.image))
        #   - show each item with value and sell button.
        all_widgets.append(scr.create_text(1522, 177+200*ind/3, text=f"{round(item.value * 0.8):<3}G", fill="#FFAF00",
                                           font=["Berlin Sans FB Demi", 14]))

        item.sell_button = Button(scr, text="<- SELL", bg="#6678AA", font=("Berlin Sans FB Demi", 14),
                                  command=lambda _=item: exchange(player, "sell", _, store_list, store, all_widgets))
        item.sell_button.place(x=1569, y=161+200*ind/3)
        all_widgets.append(item.sell_button)

    # show store inventory.   <<--
    store_list = sys.modules[__name__].__getattribute__(store)
    for data_set in store_list.items:
        #   - show each item with value, stock and buy button.
        item, stock = data_set

        all_widgets.append(scr.create_image(420, 177+200*(store_list.items.index(data_set))/3, image=item.image))
        all_widgets.append(scr.create_text(258, 177+200*(store_list.items.index(data_set))/3, text=f"[{stock}]",
                                           fill="#FFFFFF", font=["Berlin Sans FB Demi", 14]))
        all_widgets.append(scr.create_text(566, 177+200*(store_list.items.index(data_set))/3,
                                           text=f"{round(item.value*store_list.cost_modifier):<3} G", fill="#FFAF00",
                                           font=["Berlin Sans FB Demi", 14]))
        item.buy_button = Button(scr, text="<- BUY", bg="#6678AA", font=("Berlin Sans FB Demi", 14),
                                 command=lambda _=item: exchange(player, "buy", _, store_list, store, all_widgets),
                                 disabledforeground="#FF0000")
        item.buy_button.place(x=608, y=161+200*(store_list.items.index(data_set))/3)

        # disable buttons if item is out of stock or player is too poor.
        if player.gold < item.value*store_list.cost_modifier:
            item.buy_button.config(state="disabled")
        if stock <= 0 or len(player.inventory) >= 12:
            item.buy_button.config(state="disabled")
        all_widgets.append(item.buy_button)


def close_store(player, all_widgets):
    """Internal function for closing store menus."""
    # rebind keys.
    win.bind(f"<{Settings.inventoryKey}>", lambda _: open_inventory(player))
    win.bind(f"<{Settings.upKey}>", player.move)
    win.bind(f"<{Settings.leftKey}>", player.move)
    win.bind(f"<{Settings.downKey}>", player.move)
    win.bind(f"<{Settings.rightKey}>", player.move)
    win.bind(f"<{Settings.interactKey}>", player.interact)
    Core.can_escape = True

    # hide player & store inventories.
    for widget in all_widgets:
        try:
            widget.destroy()
        except AttributeError:
            scr.delete(widget)


def exchange(player=None, action="buy", item=None, store=None, store_data=None, widgets=None):
    """Function for buying and selling items, to be bound to store Buy and Sell buttons."""
    if action == "buy":  # for buying
        player.gold -= item.value*store.cost_modifier
        for _ in store.items:          # this loop decreases the items stock by 1 in this store.
            if item in _:
                _[1] -= 1
        player.inventory.append(item)
        print("bought", item.name, "for", item.value*store.cost_modifier)
    else:                # for selling
        player.gold += round(item.value * 0.8)
        player.inventory.remove(item)
        print("sold", item.name, "for", round(item.value*0.8))

    close_store(player, widgets)
    open_store(player, store_data)


# create a store by defining a list starting with a cost modifier followed by all sold items listed with their stock:
class Store:
    def __init__(self, cost_modifier, *items):
        """

        Class for holding store data, added solely to fix a major bug.
        This class was added very late in development and is thus not 100% efficient.

        When creating a store an empty save slot should be added to all SaveFiles:
        |:pass: store_name
        |{}
        """
        self.cost_modifier = cost_modifier
        self.size = len(items)
        self.items = items

        ind = 0
        for item in items:
            setattr(self, f"item{ind}", item)
            ind += 1


hut_store = Store(1, [health_potion, 999], [large_health_potion, 100], [vitality_potion, 3], [stamina_potion, 999],
                  [large_stamina_potion, 100], [staminaless_potion, 10], [strength_potion, 999],
                  [resistance_potion, 999], [shield_potion, 100])

potion_store = Store(1, [health_potion, 4], [stamina_potion, 4], [resistance_potion, 2],  [shield_potion, 1],
                     [vitality_potion, 1])


# Display menu:
img_display_frame = PhotoImage(file="images/Backgrounds/TextDisplay.png".replace("/", os.sep)).zoom(5, 5)


def pack(func, display_wait, ind):
    """Internal function for advancing display loop when selecting options."""
    func()
    display_wait.set(ind)


def display(player, message: list[str] | str, options: list = None):
    """
    Displays message on screen.\n
    Message must be list of pages of strings, \n
    Newline creates extra lines in a page.\n
    if str is not in list, message is single page.\n

    Commands are put in the options variable as [function, text]. \n
    Commands are displayed on bottom side of the menu on the last page
    and pressed using left mouse button. \n
    When no commands are present, Enter button and left mouse button advance display to its next page.

    - Returns list of chosen option.
    """

    if type(message) == str:
        message = [message]

    # rebind keys and set variables
    win.unbind(f"<{Settings.inventoryKey}>")
    win.unbind(f"<{Settings.upKey}>")
    win.unbind(f"<{Settings.leftKey}>")
    win.unbind(f"<{Settings.downKey}>")
    win.unbind(f"<{Settings.rightKey}>")
    win.unbind(f"<{Settings.interactKey}>")
    Core.can_escape = False

    display_wait = IntVar(value=0)
    win.bind("<Return>", lambda _: display_wait.set(1))
    win.bind("<Button-1>", lambda _: display_wait.set(1))

    scr.create_image(960, 890, image=img_display_frame, tag="display_frame")
    option_list = []

    # display texts
    for text in message:
        scr.create_text(960, 815, text=text, font=["Berlin Sans FB Demi", 22], justify="center", tag="display_text")
        if message.index(text) == len(message) - 1 and len(options) > 0:
            # prepare options
            win.unbind("<Return>")
            win.unbind("<Button-1>")
            ind = 0
            for command, label in options:
                # show options
                option_list.append(Button(scr, text=label, command=lambda a=command, i=ind: pack(a, display_wait, i),
                                          font=["Berlin Sans FB Demi", 21], bg="#335E8F", activebackground="#446FA0"))
                option_list[len(option_list)-1].place(x=1920/(len(options)+1)*(ind+1), y=950, anchor="center")
                ind += 1
        # wait for input then reset for next loop
        scr.wait_variable(display_wait)
        scr.delete("display_text")

    # destroy all and rebind keys
    scr.delete("display_frame")
    for button in option_list:
        button.destroy()

    win.bind(f"<{Settings.inventoryKey}>", lambda _: open_inventory(player))
    win.bind(f"<{Settings.upKey}>", player.move)
    win.bind(f"<{Settings.leftKey}>", player.move)
    win.bind(f"<{Settings.downKey}>", player.move)
    win.bind(f"<{Settings.rightKey}>", player.move)
    win.bind(f"<{Settings.interactKey}>", player.interact)
    Core.can_escape = True

    return options[display_wait.get()]


def learn_spell(player, ind, spell):
    """Function for learning and forgetting spells."""
    # Undo forgotten passive boosts:
    if player.spells[ind] == agility:
        player.speed -= 4
    elif player.spells[ind] == focus:
        player.focus = 0
    elif player.spells[ind] == stamina:
        player.max_stamina -= 5

    # Learn spell:
    print(f"player learned {spell.name} and "
          f"forgot {player.spells[ind].name if player.spells[ind] is not None else None}!")
    player.spells[ind] = spell

    # Set passive boosts:
    if spell == agility:
        player.speed += 4
    elif spell == focus:
        player.focus = -1
    elif spell == stamina:
        player.max_stamina += 5
        player.stamina += 5


def spells_unlock(player, ind):
    """Functions for asking the player what spell to learn."""
    options = [
        # index 0
        [[lambda: learn_spell(player, ind, regenerate), "Regenerate"],
         [lambda: learn_spell(player, ind, empower), "Empower"],
         [lambda: learn_spell(player, ind, lightning), "Lightning"]],
        # index 1
        [[lambda: learn_spell(player, ind, elemental_volley), "Elemental volley"],
         [lambda: learn_spell(player, ind, stasis), "Stasis"],
         [lambda: learn_spell(player, ind, agility), "Agility [passive]"],
         [lambda: learn_spell(player, ind, weaken), "Weaken"]],
        # index 2
        [[lambda: learn_spell(player, ind, fireball), "Fireball"],
         [lambda: learn_spell(player, ind, stamina), "Stamina [passive]"],
         [lambda: learn_spell(player, ind, whirlwind), "Whirlwind"],
         [lambda: learn_spell(player, ind, enchant_weapon), "Enchant weapon"]],
        # index 3
        [[lambda: learn_spell(player, ind, venom), "Venom"],
         [lambda: learn_spell(player, ind, recover), "Recover"],
         [lambda: learn_spell(player, ind, focus), "Focus [passive]"],
         [lambda: learn_spell(player, ind, barrier), "Barrier"]],
        # index 4
        [[lambda: learn_spell(player, ind, heal), "Heal"],
         [lambda: learn_spell(player, ind, chaotic_strike), "Chaotic strike"],
         [lambda: learn_spell(player, ind, siphon), "Siphon"]]
    ][ind]        # directly takes options from this list using ind.

    display(player, ["Spells can be used in battle and have varying cool-downs.\n"
                     "The player can learn 5 spells, here you can choose what spell\n"
                     f"occupies slot {ind+1}."], options)


def open_inventory(player):
    """Function bound to inventoryKey. Displays player stats and lists."""
    if Core.can_escape:
        Core.can_escape = False
        win.unbind(f"<{Settings.inventoryKey}>")
        win.unbind(f"<{Settings.upKey}>")
        win.unbind(f"<{Settings.leftKey}>")
        win.unbind(f"<{Settings.downKey}>")
        win.unbind(f"<{Settings.rightKey}>")
        win.unbind(f"<{Settings.interactKey}>")
        win.bind(f"<{Settings.inventoryKey}>", lambda _: close_inventory(player))

        scr.create_image(960, 540, image=Inventory_bg, tag="inventory_bg")

        # Stats:

        scr.create_text(480, 270, font=("Berlin Sans FB Demi", 20), text="-= STATS =-", justify="center",
                        fill="#FFFFFF", tag="inv_label")
        scr.create_text(395, 545, font=("Berlin Sans FB Demi", 17),
                        text="Health:\n\n"
                             "Stamina:\n\n"
                             "Level:\n\n"
                             "Gold:\n\n"
                             "Weapon:\n\n"
                             "Damage:\n\n"
                             "Speed:\n\n"
                             "Light stamina cost:\n\n"
                             "Heavy stamina cost:",
                        justify="left", fill="#FCFCFC", width=480, tag="inv_label")

        scr.create_text(615, 545, font=("Berlin Sans FB Demi", 17),
                        text=f"{player.health} / {player.max_health}\n\n"
                             f"{player.max_stamina}\n\n"
                             f"{player.level} [{int(player.soul/20*100)}%]\n\n"
                             f"{player.gold}\n\n"
                             f"{player.weapon.name if player.weapon is not None else None}\n\n"
                             f"{player.damage}\n\n"
                             f"{player.speed}\n\n"
                             f"{player.light_atk_cost}\n\n"
                             f"{player.heavy_atk_cost}",
                        justify="right", fill="#FCFCFC", width=480, tag="inv_label")

        # Items and Spells:

        scr.create_text(1500, 336-120, font=("Berlin Sans FB Demi", 20), text="< INVENTORY <", justify="center",
                        fill="#FFFFFF", tag="inv_label")
        scr.create_text(1500, 852, font=("Berlin Sans FB Demi", 20), text="^ SPELLS ^", justify="center",
                        fill="#FFFFFF", tag="inv_label")

        for ind in range(0, 12):
            scr.create_rectangle(2996/3-8/3*2, 427/3+200*ind/3, 3836/3+8/3*2, 635/3+200*ind/3, fill="#01133A",
                                 width=8/3, tag="inv_image")

            if ind < len(player.inventory):
                item = player.inventory[ind]
                scr.create_image(1139, 177+200*ind/3, image=item.image, tag="inv_image")

        for ind in range(0, 5):
            spell = player.spells[ind]
            scr.create_rectangle(1500-144-1.5, 336+ind*96-48, 1500+144, 336+ind*96+48, width=3,
                                 fill="#1F1013",  tag="inv_image")
            if spell is not None:
                scr.create_image(1500, 336+ind*96, image=spell.image, tag="inv_image")


def close_inventory(player):
    """Internal function bound to inventoryKey by open_inventory().
    Removes everything displayed by open_inventory() and resumes gameplay."""
    Core.can_escape = True
    win.unbind(f"<{Settings.inventoryKey}>")

    win.bind(f"<{Settings.inventoryKey}>", lambda _: open_inventory(player))
    win.bind(f"<{Settings.upKey}>", player.move)
    win.bind(f"<{Settings.leftKey}>", player.move)
    win.bind(f"<{Settings.downKey}>", player.move)
    win.bind(f"<{Settings.rightKey}>", player.move)
    win.bind(f"<{Settings.interactKey}>", player.interact)

    scr.delete("inventory_bg", "inv_label", "inv_image")
