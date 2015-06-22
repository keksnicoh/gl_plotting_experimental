"""
frame demo will render a fps counter within
two frame buffer objects.
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.app import BasicGl
from mygl.objects.fps import GlFPS
from mygl.matricies import *
from mygl.objects.frame import Window
from time import sleep
import ImageFont, os

FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../resources/fonts'

if __name__ == '__main__':
    app = BasicGl(window_title='framebuffer window layout demo')
    ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", 120)
    gl_fps = GlFPS(ft)
    gl_fps.prepare()

    resolution = 8
    window1 = Window(size=(1.0, 1.0), resolution=(resolution, resolution)) #bad resolution
    window2 = Window(size=(0.5, 0.5), color=[.5, .5, 0, 1])

    # translate window 2
    window2.shader.uniform('mat_modelview', translation_matrix(-.5, .5))

    render_200th = 1
    while app.active():

        app.init_cycle()
        if 82 in app.keyboardActive:
            if resolution < 512: resolution *= 2
            window1 = Window(size=(1.0, 1.0), resolution=(resolution, resolution))
            sleep(0.1)
            continue

        with window1: gl_fps.render()

        # this window is "cached"
        if render_200th == 1:
            with window2: gl_fps.render()

        window1.render()
        window2.render()
        app.swap()

        gl_fps.tick()
        render_200th = 1 if not render_200th % 200 else render_200th +1

