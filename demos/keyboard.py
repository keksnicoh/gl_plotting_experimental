"""
fps demo. note that due vsync the window library
glwf limits the frames to 60fps. without this a typlical
computer (2015) would render 20.000fps
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.app import BasicGl
from mygl.fps import GlFPS
from mygl.font import GlFont
from mygl.matricies import *
import ImageFont, os
FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../resources/fonts'
TEXT = 'a'*2000
BTN_SHIFT = False
BTN_ALT = False
if __name__ == '__main__':
    app = BasicGl()
    ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", 20)
    gl_fps = GlFPS(ft)
    gl_fps.prepare()
    translation = translation_matrix(-1,1)
    gl_font = GlFont('', ft)

    while app.active():
        app.init_cycle()

        key_stack = app.keyboardStack
        print(app.keyboardActive)
        BTN_SHIFT = 280 in app.keyboardActive or 344 in app.keyboardActive or 340 in app.keyboardActive
        BTN_ALT = 346 in app.keyboardActive
        while len(key_stack):

            key = key_stack.pop()
            if key == 256 and len(TEXT):
                TEXT = TEXT[:-1]
            elif key < 256:
                shift = 32 if not BTN_SHIFT else 0
                TEXT += chr(key + shift)

        n = 40
        splitted = '\n'.join([TEXT[i:i+n] for i in range(0, len(TEXT), n)])
        if gl_font.text != splitted:
            gl_font.set_text(splitted)

        gl_font.render(mat_projection=translation)

        gl_fps.render()
        app.swap()
        gl_fps.tick()
        print(gl_fps)


