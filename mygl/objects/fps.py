"""
simple gl object to render FPS
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""

from mygl.font import GlFont
from PIL import ImageFont
import time
import os
class GlFPS():
    def __init__(self, ft):
        """ required a ImageFont object """
        self.fps = [.0, .0, .0, .0, .0]
        self.last_tick = time.time()
        self.fps_tick = 0
        self.ft = ft
        self.gl_ft_tick = None
        self.last_update = 0
    def prepare(self):
        self.gl_ft_tick = GlFont('', self.ft)
    def tick(self):
        new_tick = time.time()
        self.fps[self.fps_tick] = 1.0/(time.time() - self.last_tick)
        self.last_tick = new_tick
        self.fps_tick = (self.fps_tick+1)%5
    def render(self, mat_projection=None):
        if time.time() - self.last_update > 0.5:
            self.gl_ft_tick.set_text(self.__str__())
            self.last_update = time.time()
        self.gl_ft_tick.render(mat_projection=mat_projection)

    def __str__(self):
        return "{:2.02f}fps".format(sum(self.fps)/5.0)

