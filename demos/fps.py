"""
fps demo. note that due vsync the window library
glwf limits the frames to 60fps. without this a typlical
computer (2015) would render 20.000fps
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.app import BasicGl
from mygl.fps import GlFPS
import ImageFont, os
FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../resources/fonts'

if __name__ == '__main__':
    app = BasicGl()
    ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", 40)
    gl_fps = GlFPS(ft)
    gl_fps.prepare()

    while app.active():
        app.init_cycle()
        gl_fps.render()
        app.swap()
        gl_fps.tick()


