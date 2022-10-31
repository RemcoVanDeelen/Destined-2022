from Action_definitions import *


# item store:
def open_store():
    # unbind keys.
    # show player inventory.  -->>
    #   - show each item with value and sell button.
    # show store inventory.   <<--
    #   - show each item with value and buy button.
    #   - if item.value > player.gold: item.configure(state="disabled")
    pass


def close_store():
    # hide player & store inventories.
    # rebind keys.
    pass


def exchange(player=None, action="buy", item=None):
    if action == "buy":
        player.gold -= item.value
        player.inventory.append(item)
        print("bought", item.name, "for", item.value)
    else:
        player.gold += round(item.value * 0.8)
        player.inventory.remove(item)
        print("sold", item.name, "for", round(item.value*0.8))
