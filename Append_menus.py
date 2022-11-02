import sys
from Action_definitions import *
import Core

Storefront_bg = PhotoImage(file="images/Inventory_GUI/Storefront_bg_filter.png").zoom(120, 120)


# item store:
def open_store(player, store):
    # unbind keys.
    win.unbind("<w>")
    win.unbind("<a>")
    win.unbind("<s>")
    win.unbind("<d>")
    win.unbind("<r>")
    Core.can_escape = False

    # show general store:
    all_widgets = [scr.create_image(960, 540, image=Storefront_bg)]
    close_store_button = Button(scr, text="Close Store", command=lambda: close_store(player, all_widgets))
    close_store_button.place(x=960, y=840)
    close_store_button = Label(scr, text="Gold = "+str(player.gold))
    close_store_button.place(x=960, y=900)
    all_widgets.append(close_store_button)

    item_related_widgets = []

    # show player inventory.  -->>
    for ind in range(0, len(player.inventory)):
        item = player.inventory[ind]
        all_widgets.append(scr.create_image(1200+180, 354/2+(1080-480)*ind/9, image=item.image))
        #   - show each item with value and sell button.
        item.sell_label = Label(scr, text=round(item.value*0.8), bg="#AAAAAA", font=("Berlin Sans FB Demi", 14))
        item.sell_label.place(x=1200+180+144+12, y=354/2+(1080-480)*ind/9-8)

        item.sell_button = Button(scr, text="<- SELL", bg="#AAAAAA", font=("Berlin Sans FB Demi", 14), command=lambda _=item: exchange(player, "sell", _, store_list, store, all_widgets))
        item.sell_button.place(x=1200+180+144+12+32, y=354/2+(1080-480)*ind/9-16)
        all_widgets.append(item.sell_label)
        all_widgets.append(item.sell_button)

    # show store inventory.   <<--
    store_list = sys.modules[__name__].__getattribute__(store)
    for data_set in store_list:
        if type(data_set) == int:
            continue
        else:
            #   - show each item with value and buy button.
            item, stock = data_set

            all_widgets.append(scr.create_image(240+180, 354/2+(1080-480)*(store_list.index(data_set)-1)/9, image=item.image))
            item.buy_label = Label(scr, text=round(item.value*store_list[0]), bg="#AAAAAA", font=("Berlin Sans FB Demi", 14))
            item.buy_label.place(x=240+180+144+12, y=354/2+(1080-480)*(store_list.index(data_set)-1)/9-8)

            item.buy_button = Button(scr, text="<- BUY", bg="#AAAAAA", font=("Berlin Sans FB Demi", 14), command=lambda _=item: exchange(player, "buy", _, store_list, store, all_widgets))
            item.buy_button.place(x=240+180+144+12+32, y=354/2+(1080-480)*(store_list.index(data_set)-1)/9-16)
            if player.gold < item.value*store_list[0]:
                item.buy_button.config(state="disabled")
            if stock <= 0:
                item.buy_label.config(state="disabled")
                item.buy_button.config(state="disabled")
            all_widgets.append(item.buy_label)
            all_widgets.append(item.buy_button)


def close_store(player, all_widgets):
    # hide player & store inventories.
    # rebind keys.
    win.bind("<w>", player.move)
    win.bind("<a>", player.move)
    win.bind("<s>", player.move)
    win.bind("<d>", player.move)
    win.bind("<r>", player.interact)
    Core.can_escape = True
    for widget in all_widgets:
        try:
            widget.destroy()
        except AttributeError:
            scr.delete(widget)


def exchange(player=None, action="buy", item=None, store=None, store_data=None, widgets=None):
    if action == "buy":
        player.gold -= item.value*store[0]
        for _ in store:
            if type(_) != int:
                if item in _:
                    _[1] -= 1
        player.inventory.append(item)
        print("bought", item.name, "for", item.value)
    else:
        player.gold += round(item.value * 0.8)
        player.inventory.remove(item)
        print("sold", item.name, "for", round(item.value*0.8))

    close_store(player, widgets)
    open_store(player, store_data)


# create a store by defining a list starting with a cost modifier followed by all sold items listed with their stock:
Test_store = [1, [health_potion, 999], [large_health_potion, 100], [vitality_potion, 1],
              [stamina_potion, 999], [large_stamina_potion, 100], [staminaless_potion, 10],
              [strength_potion, 999], [resistance_potion, 999], [shield_potion, 100]]
