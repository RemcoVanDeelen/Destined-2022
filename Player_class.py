from Core import *
from Room_class import *


class Player:
    def __init__(self, tag: str):
        """
        Define a player by giving it a tag.\n
        it will be located at [1, 1] and will not yet be animated. [self.disp.roll]\n
        Functions:\n
        - MOVE, To be bound to arrow keys or WASD;
        - INTERACT, To be bound to any key;
        - WARP;
        - OTHER {[To Be Added In Future]}.

        :param tag: str | int
        """
        # Inventories:
        self.inventory = []
        self.spells = []
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

        self.soul = 0
        self.level = 1

        # Movement statistics
        self.checkpoint = [["X", "Y"], "Room"]
        self.position = [1, 1]
        self.tile = None
        self.coordinates = [self.position[0] * 48 * 5 / 4 + 24 * 5 / 4,  self.position[1] * 60]
        self.room = None
        self.running = False
        self.moving = False
        self.move_delay = 400

        # Imagery
        self.tag = tag
        self.facing = S
        self.health_label = None
        self.stamina_label = None

        # sprite list:
        self.idle_n_sprites = []
        for ind in range(0, 6):
            self.idle_n_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_idle_N.gif", format="gif -index {}".format(ind)).zoom(10, 10).subsample(4, 4))
        self.idle_e_sprites = []
        for ind in range(0, 6):
            self.idle_e_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_idle_E.gif", format="gif -index {}".format(ind)).zoom(10, 10).subsample(4, 4))
        self.idle_s_sprites = []
        for ind in range(0, 6):
            self.idle_s_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_idle_S.gif", format="gif -index {}".format(ind)).zoom(10, 10).subsample(4, 4))
        self.idle_w_sprites = []
        for ind in range(0, 6):
            self.idle_w_sprites.append(
                PhotoImage(file="images/Movement_GUI/player_idle_W.gif", format="gif -index {}".format(ind)).zoom(10, 10).subsample(4, 4))

        self.idle_framerate = [200, 90, 105, 200, 105, 90]

        self.movement_sprites = []
        self.battle_sprites = []
        self.disp = Animation(scr, self.coordinates,  self.tag, self.idle_s_sprites, self.idle_framerate, True)
        self.stop = False

    #                                       Movement functions:                                     #
    def move(self, event):
        if not self.moving:
            temp_pos = [self.position[0], self.position[1]]
            if event.keysym == "w" or event.keysym == "Up":
                self.facing = N
                temp_pos[1] -= 1
            if event.keysym == "d" or event.keysym == "Right":
                self.facing = E
                temp_pos[0] += 1
            if event.keysym == "s" or event.keysym == "Down":
                self.facing = S
                temp_pos[1] += 1
            if event.keysym == "a" or event.keysym == "Left":
                self.facing = W
                temp_pos[0] -= 1
            self.disp.gif = getattr(self, "idle_" + self.facing + "_sprites")
            scr.itemconfigure(self.tag, image=self.disp.gif[self.disp.frame])
            if not getattr(self.room, "Y_"+str(temp_pos[1]))[temp_pos[0]].wall:
                self.tile = getattr(self.room, "Y_"+str(temp_pos[1]))[temp_pos[0]]
                self.moving = True
                self.position = temp_pos
                self.movement(self.facing)
                if not self.tile.interact:
                    self.tile.activate()

    def movement(self, direction, delay=0):
        if not self.stop:
            if delay < self.move_delay:
                win.after(int(self.move_delay/8), lambda: self.movement(direction, delay+int(self.move_delay/8)))
                if direction == "e":
                    self.coordinates[0] += 7.5
                if direction == "n":
                    self.coordinates[1] += -7.5
                if direction == "w":
                    self.coordinates[0] += -7.5
                if direction == "s":
                    self.coordinates[1] += 7.5
                scr.coords(self.tag, self.coordinates[0], self.coordinates[1])
            else:
                self.moving = False
        else:
            self.stop = False
            self.moving = False

    def interact(self, binds):
        temp_pos = [self.position[0], self.position[1]]
        if self.facing == N:
            temp_pos[1] -= 1
        if self.facing == E:
            temp_pos[0] += 1
        if self.facing == S:
            temp_pos[1] += 1
        if self.facing == W:
            temp_pos[0] -= 1
        tile = getattr(self.room, "Y_"+str(temp_pos[1]))[temp_pos[0]]

        if tile.interact:
            tile.activate()

    def warp(self, destination, room, activate=False):
        if room != self.room:
            door(self.room, room, scr, self, location=destination)
        self.position = destination
        self.coordinates = [self.position[0] * 48 * 5 / 4 + 24 * 5 / 4,  self.position[1] * 60]
        scr.coords(self.tag, self.coordinates[0], self.coordinates[1])

        self.tile = getattr(self.room, "Y_"+str(destination[1]))[destination[0]]

        if activate:
            self.tile.activate()

    #                                   Battle functions:                                         #
    def turn(self, data):
        pass


class Weapon:
    def __init__(self, damage_modifier, light_atk_cost, heavy_atk_cost, speed_modifier):
        self.damage_modifier = damage_modifier
        self.light_atk_cost = light_atk_cost
        self.heavy_atk_cost = heavy_atk_cost
        self.speed_modifier = speed_modifier

    def equip(self, player):
        print("Player equipped", self, "over", player.weapon)
        if player.weapon:
            player.weapon.un_equip(player)

        player.weapon = self
        player.damage += self.damage_modifier
        player.light_atk_cost += self.light_atk_cost
        player.heavy_atk_cost += self.heavy_atk_cost
        player.speed += self.speed_modifier

    def un_equip(self, player):
        player.damage -= self.damage_modifier
        player.light_atk_cost -= self.light_atk_cost
        player.heavy_atk_cost -= self.heavy_atk_cost
        player.speed -= self.speed_modifier


hammer = Weapon(5, 2, 2, -4)
battle_axe = Weapon(4, 1, 1, -2)
sword = Weapon(3, 0, 0, 0)
short_sword = Weapon(2, -1, -1, +2)
daggers = Weapon(1, -2, -2, +4)

Player1 = Player("Player1")  # PLAYER location moved here for tile-combat and saving to file.
