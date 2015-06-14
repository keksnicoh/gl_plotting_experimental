from mygl.app import BasicGl
from mygl.font import GlFont
from time import sleep
from OpenGL.GL import *
import numpy
import ImageFont
import os
FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../../resources/fonts'

ALL_CHARS = ''
for i in range(0, 255):
    if chr(i) == '\n': continue
    ALL_CHARS += chr(i)
    if not i % 25: ALL_CHARS += '\n'

TEXT_ARIAL = 'arial.ttf\n----------------------------------\n'+ALL_CHARS
TEXT_COURIER = 'courier.ttf\n----------------------------------\n'+ALL_CHARS

if __name__ == '__main__':
    # prepare fonts
    ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/arial.ttf", 20)
    ft_courier = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", 20)

    # start opengl
    app = BasicGl()
    gl_font_arial = GlFont(TEXT_ARIAL, ft)
    gl_font_courier = GlFont(TEXT_COURIER, ft_courier)

    # move courier font in the upper left corner
    courier_translation_matrix = numpy.array([
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        -0.8, 0.8, 0, 1,
    ], dtype=numpy.float32)

    while app.active():
        app.init_cycle()

        # courier without blending
        gl_font_courier.render(mat_projection=courier_translation_matrix)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        gl_font_arial.render()

        app.swap()
        sleep(0.05)
