"""
Anim_class.py
--

This file holds a class for animating images in tkinter.
This file has no imports and can be used in other projects as well.

"""


class Animation:
    def __init__(self, parent,
                 coords=[0, 0],
                 tag: str | int = None,
                 gif=None,
                 framerate=[],
                 repeats=0,
                 trajectory=[],
                 frame=0,
                 destroy=False,
                 t_repeats=0):
        """
        Animation class:

        Allows for animating a gif object. \n
         - Use .roll() to animate and .cancel() to cancel.
         - Trajectories are added on coordinates at index frame.
         - Repeats and t_repeats (trajectory repeats) add to loops,
           there is always 1 loop, Setting them to True makes it never end.
         - Destroy = True makes the image disappear once the animation ends.
         - Framerate is in ms (0.001 s)

        NECESSARY PARAMETERS:
         * parent = tkinter.Canvas
         * gif = list of PhotoImages

        """

        self.parent = parent
        self.coords = coords
        self.tag = tag
        self.gif = gif
        self.framerate = framerate
        self.repeats = repeats
        self.trajectory = trajectory
        self.frame = frame
        self.rolling = True
        self.destroy = destroy
        self.t_repeats = t_repeats

        if tag is None:
            self.tag = str(str(framerate) + str(parent) + str(coords)).replace(" ", "").replace("!", "")

        if not framerate:
            for _ in gif:
                self.framerate.append(10)

        self.parent.create_image(self.coords[0], self.coords[1], image=self.gif[0], tag=self.tag)

    def roll(self, called=False):
        """
        Starts or continues the animation.
        Calls itself with self.framerate intervals.
        """
        if not called:
            if len(self.gif) > 1:
                while self.frame >= len(self.gif):
                    self.frame -= 1
                if not self.parent.find_withtag(self.tag):
                    self.frame = 0
                    self.parent.create_image(self.coords[0], self.coords[1], image=self.gif[self.frame], tag=self.tag)
                self.rolling = True

        if self.rolling:
            if called:
                if self.frame == len(self.gif):
                    if self.repeats > 0:
                        if self.repeats is not True:
                            self.repeats -= 1
                        if self.t_repeats is not True:
                            self.t_repeats -= 1
                        self.frame = 0
                    else:
                        self.rolling = False

            if self.rolling:
                self.parent.itemconfigure(image=self.gif[self.frame], tagOrId=self.tag)

                if self.trajectory:
                    if self.t_repeats >= 0:
                        self.coords[0] += self.trajectory[self.frame][0]
                        self.coords[1] += self.trajectory[self.frame][1]

                    self.parent.coords(self.tag, self.coords[0], self.coords[1])

                self.parent.after(self.framerate[self.frame], self.call_self)
            else:
                if self.destroy:
                    self.parent.delete(self.tag)

    def call_self(self):
        """
        Internal function for self.roll().
        Continues to next frame and calls self.roll() with Called=True.

        """
        self.frame += 1
        self.roll(True)

    def cancel(self, finish=False, destroy=False):
        """
        Stops animation
        :param finish: If true, allows the animation to finish its current cycle
        :param destroy: If true, removes frame from screen
        """

        if finish:
            self.repeats = 0
        else:
            self.rolling = False

        self.destroy = destroy
