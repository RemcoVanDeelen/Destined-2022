from Anim_class import *


class Room:
    def __init__(self, tiles, width, height, displacement: list[int] = [0, 0]):
        """
        Basic room class:\n
        \n
        A room holds Tile objects and allows movement between them.\n
        \n
        32x18 size room is large enough to fill a 1920x1080 screen.\n
        A room this size requires 578 lines of code,\n
        for this reason tool use is advised when creating rooms (Dave can help).\n
        \n
        To center rooms smaller than 32x18 a displacement is required.\n
        Displacement = [(32-width)/2 , (18-height)/2]\n
        Displacement should also be applied to all tiles in room manually.
        """
        self.width = width
        self.height = height
        self.tiles = tiles
        self.displacement = displacement

        for a in range(0, height):
            setattr(self, "Y_"+str(a+displacement[1]), [])
            for b in range(0, width):
                t = a*width+b
                getattr(self, "Y_"+str(a+displacement[1])).append(tiles[t])

    def load(self):
        """Displays room on screen."""
        for tile in self.tiles:
            tile.display()

    def unload(self):
        """Removes room from screen."""
        for tile in self.tiles:
            if tile.disp is not None:
                tile.disp.parent.delete(tile.disp.tag)
                tile.disp.cancel()


class Tile:
    def __init__(self, parent, pos: tuple, sprite, act=None, interact=False, animated=False, framerate=None, wall=False):
        """
        Basic tile class:

        Tile objects are entered into room objects in large masses.
        They hold their position, function, image, and more.

        The typical Tile definition will look something like this:

        - Tile(scr, (3, 0), [FightImage], lambda: battle([Player1], [Dummy], "TestBackground"), True, False, [], True),

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
        """Displays tile on screen, based on coordinates"""
        pos = [self.pos[0] * 60 + 30, self.pos[1] * 60 + 30]
        if self.framerate is None:
            self.disp = Animation(self.parent, coords=pos, gif=self.sprite, repeats=self.animated)
        else:
            self.disp = Animation(self.parent, coords=pos, gif=self.sprite, framerate=self.framerate,
                                  repeats=self.animated)
        if self.animated:
            self.disp.roll()

    def activate(self):
        """If it can, triggers tile.act()."""
        if self.act is not None:
            self.act()


def door(old: Room, new: Room, parent, player, camera=[0, 0], location=[0, 0], warp=False):
    """changes the players room and loads and unload accordingly.\n
     If player location changes, set warp to True. player.warp is then called to warp the player to the new tile.\n
     If warp is False, location variable is ignored."""
    old.unload()
    new.load()
    parent.tag_raise(player.disp.tag)
    player.room = new
    if warp:
        player.stop = True
        player.warp(location, new)

    parent.xview_moveto(0)
    parent.yview_moveto(0)
    parent.xview_scroll(camera[0], "units")
    parent.yview_scroll(camera[1], "units")
