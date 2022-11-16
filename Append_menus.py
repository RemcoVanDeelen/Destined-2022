import sys
from Action_definitions import *
import Core

Storefront_bg = PhotoImage(file="images/Backgrounds/Storefront_bg_filter.png").zoom(120, 120)


# item store:
def open_store(player, store: str):
    """Opens stores.\n
    Player inventory is shown on the right with buttons for selling items at 0.8x value.\n
    Store items are shown on the left with stock labels and buttons for buying items at store[0]x value.\n
    In the center the player gold is displayed paired with a button to close the menu. \n
    for store definitions look below exchange() definition. \n
    The store variable required here is the str name of the list variable."""
    # unbind keys.
    win.unbind("<w>")
    win.unbind("<a>")
    win.unbind("<s>")
    win.unbind("<d>")
    win.unbind("<r>")
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
    for data_set in store_list:
        if type(data_set) == int:
            continue
        else:
            #   - show each item with value, stock and buy button.
            item, stock = data_set

            all_widgets.append(scr.create_image(420, 177+200*(store_list.index(data_set)-1)/3, image=item.image))
            all_widgets.append(scr.create_text(258, 177+200*(store_list.index(data_set)-1)/3, text=f"[{stock}]",
                                               fill="#FFFFFF", font=["Berlin Sans FB Demi", 14]))
            all_widgets.append(scr.create_text(566, 177+200*(store_list.index(data_set)-1)/3,
                                               text=f"{round(item.value*store_list[0]):<3} G", fill="#FFAF00",
                                               font=["Berlin Sans FB Demi", 14]))

            item.buy_button = Button(scr, text="<- BUY", bg="#6678AA", font=("Berlin Sans FB Demi", 14),
                                     command=lambda _=item: exchange(player, "buy", _, store_list, store, all_widgets),
                                     disabledforeground="#FF0000")
            item.buy_button.place(x=608, y=161+200*(store_list.index(data_set)-1)/3)

            # disable buttons if item is out of stock or player is too poor.
            if player.gold < item.value*store_list[0]:
                item.buy_button.config(state="disabled")
            if stock <= 0 or len(player.inventory) >= 12:
                item.buy_button.config(state="disabled")
            all_widgets.append(item.buy_button)


def close_store(player, all_widgets):
    """Internal function for closing store menus."""
    # rebind keys.
    win.bind("<w>", player.move)
    win.bind("<a>", player.move)
    win.bind("<s>", player.move)
    win.bind("<d>", player.move)
    win.bind("<r>", player.interact)
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
        player.gold -= item.value*store[0]
        for _ in store:          # this loop decreases the items stock by 1 in this store.
            if type(_) != int:
                if item in _:
                    _[1] -= 1
        player.inventory.append(item)
        print("bought", item.name, "for", item.value)
    else:                # for selling
        player.gold += round(item.value * 0.8)
        player.inventory.remove(item)
        print("sold", item.name, "for", round(item.value*0.8))

    close_store(player, widgets)
    open_store(player, store_data)


# create a store by defining a list starting with a cost modifier followed by all sold items listed with their stock:
hut_store = [1, [health_potion, 999], [large_health_potion, 100], [vitality_potion, 3],
             [stamina_potion, 999], [large_stamina_potion, 100], [staminaless_potion, 10],
             [strength_potion, 999], [resistance_potion, 999], [shield_potion, 100]]

potion_store = [1, [health_potion, 4], [stamina_potion, 4], [resistance_potion, 2],
                [shield_potion, 1], [vitality_potion, 1]]


# Display menu:
img_display_frame = PhotoImage(file="images/Battle_GUI/BattleMenuTest.png".replace("/", os.sep)).zoom(5, 5)


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
    win.unbind("<w>")
    win.unbind("<a>")
    win.unbind("<s>")
    win.unbind("<d>")
    win.unbind("<r>")
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
                                          font=["Berlin Sans FB Demi", 21], bg="#33588F"))
                option_list[len(option_list)-1].place(x=1920/(len(options)+1)*(ind+1), y=950, anchor="center")
                ind += 1
        # wait for input then reset for next loop
        scr.wait_variable(display_wait)
        scr.delete("display_text")

    # destroy all and rebind keys
    scr.delete("display_frame")
    for button in option_list:
        button.destroy()

    win.bind("<w>", player.move)
    win.bind("<a>", player.move)
    win.bind("<s>", player.move)
    win.bind("<d>", player.move)
    win.bind("<r>", player.interact)
    Core.can_escape = True

    return options[display_wait.get()]


def learn_spell(player, ind, spell):
    """Function for learning spell."""
    player.spells[ind] = spell
    print("player learned", spell)


def spells_unlock(player, ind):
    """Functions for asking the player what spell to learn."""
    options = [[[lambda: learn_spell(player, ind, regenerate), "Regenerate"],
                [lambda: learn_spell(player, ind, empower), "Empower"],
                [lambda: learn_spell(player, ind, lightning), "Lightning"]],             # index 0
               [[lambda: learn_spell(player, ind, elemental_volley), "Elemental volley"],
                [lambda: learn_spell(player, ind, stasis), "Stasis"],
                [lambda: learn_spell(player, ind, weaken), "Weaken"]],                   # index 1
               [[lambda: learn_spell(player, ind, fireball), "Fireball"],
                [lambda: learn_spell(player, ind, whirlwind), "Whirlwind"],
                [lambda: learn_spell(player, ind, enchant_weapon), "Enchant weapon"]],   # index 2
               [[lambda: learn_spell(player, ind, venom), "Venom"],
                [lambda: learn_spell(player, ind, recover), "Recover"]],
               [[lambda: learn_spell(player, ind, heal), "Heal"],                       # index 3
                [lambda: learn_spell(player, ind, chaotic_strike), "Chaotic strike"],
                [lambda: learn_spell(player, ind, siphon), "Siphon"]]][ind]              # index 4

    display(player, ["Spells can be used in battle and have varying cooldowns.\n"
                     "The player can learn 5 spells, here you can choose what spell\n"
                     f"occupies slot {ind+1}."], options)
