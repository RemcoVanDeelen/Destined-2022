from Anim_class import *


class Room:
    def __init__(self, tiles, width, height):
        """
        Basic room class:

        INSERT DEFINITION HERE
        """
        self.width = width
        self.height = height
        self.tiles = tiles

        for a in range(0, height):
            setattr(self, "Y_"+str(a), [])
            for b in range(0, width):
                t = a*width+b
                getattr(self, "Y_"+str(a)).append(tiles[t])

    def load(self):
        for tile in self.tiles:
            tile.display()

    def unload(self):
        for tile in self.tiles:
            if tile.disp is not None:
                tile.disp.parent.delete(tile.disp.tag)


class Tile:
    def __init__(self, parent, pos: tuple, sprite, act=None, interact=False, animated=False, framerate=None, wall=False):
        """
        Basic tile class:

        INSERT DEFINITION HERE
        """
        self.pos = pos  # position in (x, y)
        self.act = act  # Action function
        self.sprite = sprite  # Displayed PhotoImage
        self.interact = interact  # Whether self.act() happens upon interaction (True), or else upon entering (False)
        self.animated = animated  # Whether the displayed image is animated or not
        self.disp = None
        self.parent = parent
        self.framerate = framerate
        self.wall = wall

    def display(self):
        pos = [self.pos[0] * 48 * 5 / 4 + 24 * 5 / 4, self.pos[1] * 60 + 30]
        if self.framerate is None:
            self.disp = Animation(self.parent, coords=pos, gif=self.sprite, repeats=self.animated)
        else:
            self.disp = Animation(self.parent, coords=pos, gif=self.sprite, framerate=self.framerate, repeats=self.animated)
        self.disp.roll()

    def activate(self):
        if self.act is not None:
            self.act()


def door(old: Room, new: Room, parent, player, camera=[0, 0], location=[0, 0], warp=False):
    old.unload()
    parent.xview_moveto(camera[0])
    parent.yview_moveto(camera[1])
    new.load()
    parent.tag_raise(player.disp.tag)
    player.room = new
    if warp:
        player.warp(location, new)
