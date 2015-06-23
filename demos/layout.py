"""
frame demo will render a fps counter within
two frame buffer objects.
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.app import BasicGl
from mygl.objects.fps import GlFPS
from mygl.matricies import *
from mygl.objects.frame import Layout
from time import sleep
import numpy
import ImageFont, os

FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../resources/fonts'

if __name__ == '__main__':
    app = BasicGl(window_title='framebuffer window layout demo')
    ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", 120)
    gl_fps = GlFPS(ft)
    gl_fps.prepare()

    layout = Layout([
        ['peter','pan'],
        ['goes','boom'],
        ['peng','donk', 'derp'],
        range(0,10),
    ])

    # do some fance stuff with the layout
    projection_matrix = numpy.array([
        0.7,0.1, 0, 0,
        0, 0.7, 0, 0,
        0, 0, 1, 0,
        0, 0, 0.0, 1
    ], dtype=numpy.float32)


    layout.prepare()
    layout.windows['peter'].shader.uniform('color', [0.5, 0.5, 0.0, 1.0])
    layout.windows['pan'].shader.uniform('color', [0.0, 0.8, 1.0, 1.0])
    layout.windows['goes'].shader.uniform('color', [0.0, 0.5, 0.6, 1.0])
    layout.windows['boom'].shader.uniform('color', [0.9, 1.0, 0.6, 1.0])
    layout.windows['peng'].shader.uniform('color', [0.0, 0.5, 0.0, 1.0])
    layout.windows['donk'].shader.uniform('color', [0.0, 0.5, 0.6, 1.0])
    layout.windows['derp'].shader.uniform('color', [0.9, 0.0, 0.6, 1.0])
    for i in range(0,10):
        layout.windows[i].shader.uniform('color', [1.0/10*i, .2+.3/10*i, 1.0-1.0/10*i, 1.0])

    while app.active():
        app.init_cycle()
        with layout.windows['peter']:
            gl_fps.render()
        with layout.windows['pan']:
            gl_fps.render()
        with layout.windows['goes']:
            gl_fps.render()
        with layout.windows['boom']:
            gl_fps.render()
        with layout.windows['peng']:
            gl_fps.render()
        with layout.windows['donk']:
            gl_fps.render()
        with layout.windows['derp']:
            gl_fps.render()
        for i in range(0,10):
            with layout.windows[i]:
                gl_fps.render()
        layout.render(mat_projection=projection_matrix)
        app.swap()

        gl_fps.tick()


