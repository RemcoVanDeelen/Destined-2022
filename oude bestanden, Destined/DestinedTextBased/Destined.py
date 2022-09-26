from battle import *
from Movement import *
from enemies import *
from player_related import *
# import DestinedGraphicals
# File Location (to run in straight python):py C:\Users\remco\PycharmProjects\DestinedTextBased\Destined.py

# Test
loc.show_tiles()
print(loc.coords)
run = False
while True:
    direction = input("Where:  ")
    if direction == "break":
        break
    elif direction == "run":
        if run is False:
            run = True
            print("now running!")
        else:
            run = False
            print("no longer running...")
    else:
        if run is False:
            loc.move(direction)
        else:
            loc.move(direction, True)
    print(loc.coords)

