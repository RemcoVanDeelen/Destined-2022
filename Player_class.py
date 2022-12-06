"""
Player_class.py
--

This file defines the Player and Weapon classes.
All objects of these classes are defined at the end of the file.
"""

from Core import *
import os
from Room_class import *


class Player:
    def __init__(self, tag: str):
        """
        The player object s the most important object in the game and holds almost all changeable data.
        All attributes other than tag are set to base values and need to be changed after object definition.
        This is done by loading a SaveFile.

        Define a player by giving it a tag.\n
        it will be located at [1, 1] and will not yet be animated. [self.disp.roll]\n
        Functions:\n
        - MOVE, To be bound to 4 keys for 4 directions;
        - INTERACT, To be bound to any key;
        - WARP;

        """
        # Inventories:
        self.inventory = []
        self.spells = [None, None, None, None, None]
        self.weapon = None
        self.gold = 80

        # Battle statistics:
        self.status = []
        self.damage = 10
        self.max_health = 25
        self.health = 25
        self.max_stamina = 20
        self.stamina = 20
        self.speed = 10
        self.light_atk_cost = 5
        self.heavy_atk_cost = 8
        self.focus = 0

        self.soul = 0
        self.level = 1

        # Movement statistics
        self.checkpoint = [["X", "Y"], "Room"]
        self.position = [1, 1]
        self.tile = None
        self.coordinates = [self.position[0] * 48 * 5 / 4 + 24 * 5 / 4,  self.position[1] * 60]
        self.room = None
        self.moving = False
        self.move_delay = 280    # 280 base, minimum is 10

        # Imagery
        self.tag = tag
        self.facing = S
        self.health_label = None
        self.stamina_label = None

        # sprite list:
        self.idle_n_sprites = []
        for ind in range(0, 6):
            self.idle_n_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_idle_N.gif", format=f"gif -index {ind}"
                           .replace("/", os.sep)).zoom(10, 10).subsample(4, 4))
        self.idle_e_sprites = []
        for ind in range(0, 6):
            self.idle_e_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_idle_E.gif", format=f"gif -index {ind}"
                           .replace("/", os.sep)).zoom(10, 10).subsample(4, 4))
        self.idle_s_sprites = []
        for ind in range(0, 6):
            self.idle_s_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_idle_S.gif", format=f"gif -index {ind}"
                           .replace("/", os.sep)).zoom(10, 10).subsample(4, 4))
        self.idle_w_sprites = []
        for ind in range(0, 6):
            self.idle_w_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_idle_W.gif", format=f"gif -index {ind}"
                           .replace("/", os.sep)).zoom(10, 10).subsample(4, 4))

        self.movement_n_sprites = []
        for ind in range(0, 6):
            self.movement_n_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_movement_N.gif", format=f"gif -index {ind}"
                           .replace("/", os.sep)).zoom(10, 10).subsample(4, 4))
        self.movement_e_sprites = []
        for ind in range(0, 6):
            self.movement_e_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_movement_E.gif", format=f"gif -index {ind}"
                           .replace("/", os.sep)).zoom(10, 10).subsample(4, 4))
        self.movement_s_sprites = []
        for ind in range(0, 6):
            self.movement_s_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_movement_S.gif", format=f"gif -index {ind}"
                           .replace("/", os.sep)).zoom(10, 10).subsample(4, 4))
        self.movement_w_sprites = []
        for ind in range(0, 6):
            self.movement_w_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_movement_W.gif", format=f"gif -index {ind}"
                           .replace("/", os.sep)).zoom(10, 10).subsample(4, 4))

        self.idle_framerate = [150, 150, 200, 150, 200, 150]

        self.movement_sprites = []
        self.battle_sprites = []
        self.disp = Animation(scr, self.coordinates,  self.tag, self.idle_s_sprites, self.idle_framerate, True)
        self.stop = False

    #                                       Movement functions:                                     #
    def move(self, event):
        """
        Function bound to direction keys (such as the arrow keys).\n
         Moves player and triggers tile.activate()\n
         Cannot move player out of bounds or into walls.\n
         Changes sprite to correct animation (direction faced and movement/idle).
         """

        # set direction faced to new direction:
        if not self.moving:
            temp_pos = [self.position[0], self.position[1]]
            if event.keysym == Settings.upKey:
                self.facing = N
                temp_pos[1] -= 1
            if event.keysym == Settings.rightKey:
                self.facing = E
                temp_pos[0] += 1
            if event.keysym == Settings.downKey:
                self.facing = S
                temp_pos[1] += 1
            if event.keysym == Settings.leftKey:
                self.facing = W
                temp_pos[0] -= 1

            # Wall detection, sprite correction and movement start:
            if self.room.width > temp_pos[0]-self.room.displacement[0] >= 0 \
                    and self.room.height > temp_pos[1]-self.room.displacement[1] >= 0 \
                    and not getattr(self.room, "Y_"+str(temp_pos[1]))[temp_pos[0]-self.room.displacement[0]].wall:

                self.disp.gif = getattr(self, "movement_" + self.facing + "_sprites")
                self.tile = getattr(self.room, "Y_"+str(temp_pos[1]))[temp_pos[0]-self.room.displacement[0]]
                self.moving = True
                self.position = temp_pos
                self.movement(self.facing)
                if not self.tile.interact:
                    self.tile.activate()
            else:
                self.disp.gif = getattr(self, "idle_" + self.facing + "_sprites")
            scr.itemconfigure(self.tag, image=self.disp.gif[self.disp.frame])

    def movement(self, direction, delay=0):
        """
        Internal function for moving display when moving.
        Moves the player display 1/10 of a Tile image in the direction it is facing.
        Repeats itself 10 times with 1/10 of the move delay.
        (Cannot delay itself by less than 1 ms)

        Returns player sprite to idle after 10 repeats.
        """

        if not self.stop:
            if delay < self.move_delay:
                win.after(int(self.move_delay/10), lambda: self.movement(direction, delay+int(self.move_delay/10)))
                if direction == "e":
                    self.coordinates[0] += 6
                if direction == "n":
                    self.coordinates[1] += -6
                if direction == "w":
                    self.coordinates[0] += -6
                if direction == "s":
                    self.coordinates[1] += 6
                scr.coords(self.tag, self.coordinates[0], self.coordinates[1])
            else:
                self.disp.gif = getattr(self, "idle_" + self.facing + "_sprites")
                self.moving = False
        else:
            self.disp.gif = getattr(self, "idle_" + self.facing + "_sprites")
            self.stop = False
            self.moving = False

    def interact(self, *_):
        """
        Function for activating the tile the player is facing.
        This function is bound to the interaction key.
        """

        temp_pos = [self.position[0], self.position[1]]
        if self.facing == N:
            temp_pos[1] -= 1
        if self.facing == E:
            temp_pos[0] += 1
        if self.facing == S:
            temp_pos[1] += 1
        if self.facing == W:
            temp_pos[0] -= 1

        try:
            tile = getattr(self.room, "Y_"+str(temp_pos[1]))[temp_pos[0]-self.room.displacement[0]]
            if tile.interact:
                tile.activate()
        except AttributeError:
            pass

    def warp(self, destination, room, activate=False):
        """
        Warp function for player movement without animation, to any tile, to any room.
        Used in combination with Tile.door() function to teleport players to new locations.
        """

        if room != self.room:
            door(self.room, room, scr, self, location=destination)
        self.position = destination
        self.coordinates = [self.position[0] * 48 * 5 / 4 + 24 * 5 / 4,  self.position[1] * 60]
        scr.coords(self.tag, self.coordinates[0], self.coordinates[1])

        self.tile = getattr(self.room, "Y_"+str(destination[1]))[destination[0]-self.room.displacement[0]]

        if activate:
            self.tile.activate()

    def turn(self, data):
        """Internal function required for battle. \n
        Since player turn is defined in Battle.py, this function simply passes."""
        pass


class Weapon:
    def __init__(self, damage_modifier, light_atk_cost, heavy_atk_cost, speed_modifier, name):
        """Weapon modifier for player.\n
        Weapons affect:\n
        - damage,
        - both melee stamina costs,
        - speed.
        Only 1 weapon can be equipped at a time.
        """
        self.damage_modifier = damage_modifier
        self.light_atk_cost = light_atk_cost
        self.heavy_atk_cost = heavy_atk_cost
        self.speed_modifier = speed_modifier
        self.name = name

    def equip(self, player):
        """
        Switches equipped weapon for self.\n
        Applies own stats to player.
        """

        print("Player equipped", self.name, "over", player.weapon.name if player.weapon is not None else None)
        # un-equips current weapon
        if player.weapon:
            player.weapon.un_equip(player)

        # apply stats
        player.weapon = self
        player.damage += self.damage_modifier
        player.light_atk_cost += self.light_atk_cost
        player.heavy_atk_cost += self.heavy_atk_cost
        player.speed += self.speed_modifier

    def un_equip(self, player):
        """
        Removes own stats from player. \n
        Sets player weapon to none.
        """

        # removes stats.
        player.damage -= self.damage_modifier
        player.light_atk_cost -= self.light_atk_cost
        player.heavy_atk_cost -= self.heavy_atk_cost
        player.speed -= self.speed_modifier

        # sets player weapon to none.
        player.weapon = None


# Objects:
hammer = Weapon(5, 2, 2, -4, "Hammer")
battle_axe = Weapon(4, 1, 1, -2, "Battle axe")
sword = Weapon(3, 0, 0, 0, "Sword")
short_sword = Weapon(2, -1, -1, +2, "Short sword")
daggers = Weapon(1, -2, -2, +4, "Daggers")

Player1 = Player("Player1")
