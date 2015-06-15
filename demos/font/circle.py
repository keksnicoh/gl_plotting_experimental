"""
some demo for a custom mat_modelview_f drawing a
text as a circle
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.app import BasicGl
from mygl.font import GlFont
from mygl.fps import GlFPS
from mygl.matricies import *
from OpenGL.GL import *
import numpy
import ImageFont
import math
import time
import os
FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../../resources/fonts'

TEXT = "I WANT TO BE A CIRCLE    ###    I WANT TO BE A CIRCLE    ###    I WANT TO BE A CIRCLE    ###    I WANT TO BE A CIRCLE   ###    "
TEXT += "\n\n"
TEXT += "i am an inner circle yeah  ++++   i am an inner circle yeah"
TEXT += "\n\n"
TEXT += "even deeeeppeeeeeerrrr"
TEXT += "\n\n"
TEXT += "even deeeeppeeeeeerrrr"
TEXT += "\n\n"
TEXT += "even deeeeppeeeeeerrrr"
TEXT += "\n\n"
TEXT += "even deeeeppeeeeeerrrreven deeeeppeeeeeerrrreven deeeeppeeeeeerrrrAAAeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdaaaDdddeeeeppeeeeeerrrr"
TEXT += "\n\nAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdd"
TEXT += "AAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdddeeeeppeeeeeerrrrAAAaaaDdd"

def mat_modelview_f(rel_xy, n, l):
    """
    funny matrix to draw the text as a circle
    """
    R = 0.9 + rel_xy[1]
    phi = rel_xy[0] / R
    return numpy.array([
        math.cos(phi),   -math.sin(phi),  0, 0, # rotate letters
        math.sin(phi),   math.cos(phi),   0, 0,
        0,               0            ,   1, 0,
        R*math.sin(phi), R*math.cos(phi), 0, 1, # translate to circumfence
    ], dtype=numpy.float32)


if __name__ == '__main__':
    app = BasicGl()
    ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", 40)
    gl_fps = GlFPS(ft)
    gl_fps.prepare()
    fps_translation_left = translation_matrix(-1, 1)
    fps_translation_right = translation_matrix(0.5, 1)
    second_render_translation = translation_matrix(.005, .005)

    # circle font
    ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/arial.ttf", 30)
    gl_font_arial = GlFont(TEXT, ft)
    gl_font_arial.mat_modelview_f = mat_modelview_f

    tick = 0
    start_time = time.time()
    while app.active():
        app.init_cycle()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # do magic mushroom color stuff
        gl_font_arial.set_color([
            math.pow(math.sin(math.pi * (time.time()-start_time)),2),
            math.pow(math.cos(math.pi * (time.time()-start_time)),2),
            math.pow(math.cos(1.0/2.0* (time.time()-start_time)),2),
            .3+0.7*math.pow(math.sin(5* (time.time()-start_time)),2)])
        # set text length and render
        gl_font_arial.set_render_length(tick*2)
        gl_font_arial.render()

        gl_font_arial.set_color([
            math.pow(math.cos(1.0/2.0* (time.time()-start_time)),2),
            math.pow(math.sin(math.pi * (time.time()-start_time)),2),
            math.pow(math.cos(math.pi * (time.time()-start_time)),2),
            .3+0.7*math.pow(math.sin(5* (time.time()-start_time)),2)])
        gl_font_arial.render(mat_projection=second_render_translation)
        tick = (tick+1)%int(len(TEXT)/2)

        # render FPS counter in the upper left corner
        gl_fps.render(mat_projection=fps_translation_left)

        # just for fun render another FPS counter in the upper right corner
        gl_fps.render(mat_projection=fps_translation_right)
        app.swap()
        gl_fps.tick()
        print(gl_fps)
