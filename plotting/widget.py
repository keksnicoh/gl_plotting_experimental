#-*- coding: utf-8 -*-
"""
widgets
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
import os
import numpy
from PIL import ImageFont

from mygl.objects.frame import Window
from mygl.font import GlFont
from mygl.matricies import *

FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../resources/fonts'

CORNER_TL = 1
CORNER_TR = 2
CORNER_BL = 3
CORNER_BR = 4

class Widget():
    """ basic widget class """
    ACTIVE_COLOR = [1, 1, 1, 0.3]
    INACTIVE_COLOR = [0, 0, 0, 0]
    IS_DRAGABLE = True
    BORDER_SIZE = 0.03
    RESIZEABLE = True

    def __init__(self, pos=(0.0, 0.0), size=(0.5, 0.5)):
        self.pos = pos
        self.size = size
        self.frame = Window(size=(1.0, 1.0), color=[1,0,1,0.2])
        self.mouse = [None, None]
        self.mouse_drag = [None, None]
        self.cursor = (0.0, 0.0)
        self.active = None
        self._active_rscorner = None
        self._over_drag = (0.0, 0.0)
        self.set_active(False)
        self._init_matrix()

    def _init_matrix(self):
        """
        initilizes matrix to transform frame into widget space and
        translate frame to current position
        """
        self.frame.shader.uniform('mat_projection', numpy.array([
            2.0*self.size[0], 0, 0, 0,
            0, 2.0*self.size[1], 0, 0,
            0, 0, 1, 0,
            -1.0+2.0*self.pos[0], 1.0-2.0*self.pos[1], 0, 1,
        ], dtype=numpy.float32))

    def set_cursor(self, cursor): self.cursor = (cursor[0]-self.pos[0], cursor[1]-self.pos[1])
    def set_mouse(self, mouse): self.mouse = mouse
    def set_mouse_drag(self, drag): self.mouse_drag = drag
    def set_active(self, active=True):
        """ sets an widget active / inactive """
        if active != self.active:
            self.active = active
            self.frame.set_color(self.ACTIVE_COLOR if active else self.INACTIVE_COLOR)
            self.refresh_widget = True
    def active_corner(self):
        """ returns CORNER_* when cursor is on a corner """
        if self._active_rscorner is not None: return self._active_rscorner
        (cx, cy) = self.cursor
        if cx < self.BORDER_SIZE and cy < self.BORDER_SIZE: return CORNER_TL
        if self.size[0]-cx < self.BORDER_SIZE and cy < self.BORDER_SIZE: return CORNER_TR
        if self.size[0]-cx < self.BORDER_SIZE and self.size[1]-cy < self.BORDER_SIZE: return CORNER_BR
        if cx < self.BORDER_SIZE and self.size[1]-cy < self.BORDER_SIZE: return CORNER_BL

    def capture_mouse(self):
        """ returns True when the mouse is captured by this widget """
        if self.IS_DRAGABLE and self.mouse[1] is not None: return True
        if self.active_corner() is not None and self.mouse[0] is not None: return True

    def capture_keyboard(self):
        """ returns True when the keyboard is captured by this widget """
        return False

    def coords_in(self, coords):
        """ returns whether given coords are in the widget or not """
        return (coords[0] > self.pos[0] and coords[0] < self.pos[0] + self.size[0]
            and coords[1] > self.pos[1] and coords[1] < self.pos[1] + self.size[1])

    def execute(self):
        """ execute actions on the widget """
        if not self.active: return False

        # drag window
        if self.IS_DRAGABLE and self.mouse_drag[1] is not None and self.mouse_drag[1] != (0.0, 0.0):
            (dx, dy) = self.mouse_drag[1]
            self.pos = (
                max(0.0, self.pos[0]+dx),
                max(0.0, self.pos[1]-dy)
            )
            self._init_matrix()

        # resize window
        if self.RESIZEABLE:
            if self.mouse_drag[0] is not None:
                if self._active_rscorner is None:
                    self._over_drag = (0.0, 0.0)
                    self._active_rscorner = self.active_corner()
            else: self._active_rscorner = None

            if self._active_rscorner is not None and self.mouse_drag[0] != (0.0, 0.0):
                (dw, dh) = self.mouse_drag[0]
                if self._active_rscorner == CORNER_TL: c = (dw, -dh, -dw, dh)
                elif self._active_rscorner == CORNER_TR: c = (0, -dh, +dw, dh)
                elif self._active_rscorner == CORNER_BL: c = (dw, 0, -dw, -dh)
                elif self._active_rscorner == CORNER_BR: c = (0, 0, +dw, -dh)

                new_size = (self.size[0]+c[2], self.size[1]+c[3])
                if new_size[0] > 0.2 and new_size[1] > 0.2:
                    self.pos = (self.pos[0]+c[0], self.pos[1]+c[1])
                    self.size = new_size
                    self._init_matrix()

    def render_widget(self): pass
    def render(self):
        if self.refresh_widget:
            with self.frame:
                self.render_widget()
        self.frame.render()
        pass

class Uniforms(Widget):
    """ renders active uniform values from UniformManager """
    IS_DRAGABLE = True
    def __init__(self, uniform_manager, pos=(0.1, 0.03), size=(0.30, 0.3)):
        Widget.__init__(self, pos, size)
        self._um = uniform_manager
        ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", 60)
        gl_font = GlFont('', ft)
        gl_font.color = [0.0, 0, 0, 1.0]
        self.gl_font = gl_font
        self.refresh_widget = True
        self._last_time = 0.0
    def render_widget(self):
        str_uniforms = ''
        for name, value in self._um.get_global_uniforms().items():
            str_uniforms += '{}={:.2f}\n'.format(name, value)
        for plot, uniforms in self._um.get_local_uniforms().items():
            for name, value in uniforms.items():
                str_uniforms += '{}.{}={:.2f}\n'.format(plot, name, value)
        self.gl_font.set_text(str_uniforms)
        self.gl_font.render(mat_projection=translation_matrix(-1.0, 1.0))
        self.refresh_widget = False
    def execute(self):
        Widget.execute(self)
        if 't' in self._um.get_global_uniforms():
            if self._um.get_global_uniforms()['t'] - self._last_time > 2.0:
                self.refresh_widget = True
                self._last_time = self._um.get_global_uniforms()['t']

class Text(Widget):
    """ simple text widget """
    IS_DRAGABLE = True
    def __init__(self, text, font_size=40, font_color=[0,0,0,1], pos=(0.0, 0.0), size=(0.50, 0.7)):
        Widget.__init__(self, pos, size)
        ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", font_size)
        self.gl_font = GlFont(text, ft)
        self.gl_font.color = font_color
        self.refresh_widget = True
    def render_widget(self):
        self.gl_font.render(mat_projection=translation_matrix(-1.0, 1.0))
        self.refresh_widget = False



