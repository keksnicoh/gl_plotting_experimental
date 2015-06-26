#-*- coding: utf-8 -*-
"""
PlotterWindow
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from plotting import domain, graph
from plotting.plot2d import *
from mygl.app import BasicGl
from mygl.glfw import *

ORIGIN_TRANSLATION_INTENSITY = 0.05


class PlotterWindow():
    """
    plotting window enables interaction
    """
    def __init__(self, axis=(1.0, 1.0), origin=(0.0,0.0)):
        self.app = BasicGl(window_title='plot')
        self.plotter = Plotter(axis=axis, origin=origin, size=(2.0,2.0))

    def run(self):
        glClearColor(1,1,1,1)
        while self.app.active():
            self.app.init_cycle()
            active_keyboard = self.app.keyboardActive

            # origin translations
            if GLFW_KEY_LEFT in active_keyboard or GLFW_KEY_A in active_keyboard:
                self.plotter.translate_origin(ORIGIN_TRANSLATION_INTENSITY, 0.00)
            if GLFW_KEY_RIGHT in active_keyboard or GLFW_KEY_D in active_keyboard:
                self.plotter.translate_origin(-ORIGIN_TRANSLATION_INTENSITY, 0.00)
            if GLFW_KEY_UP in active_keyboard or GLFW_KEY_W in active_keyboard:
                self.plotter.translate_origin(0.00, -ORIGIN_TRANSLATION_INTENSITY)
            if GLFW_KEY_DOWN in active_keyboard or GLFW_KEY_S in active_keyboard:
                self.plotter.translate_origin(0.00, ORIGIN_TRANSLATION_INTENSITY)

            # zooming
            if GLFW_KEY_RIGHT_BRACKET in active_keyboard:
                self.plotter.zoom(0.99)
            if GLFW_KEY_SLASH in active_keyboard:
                self.plotter.zoom(1.01)

            self.plotter.render()
            self.app.swap()


def axis_plot2d(*kernels):
    """ starts a axis plot window """
    colors = [
        [0.0, 0.0, 0.0, 1],
        [1.0, 0.0, 0.0, 1],
        [0.0, 1.0, 0.0, 1],
        [0.0, 0.0, 1.0, 1],
    ]
    window = PlotterWindow(axis=(2.0, 2.0), origin=(1.0, 1.0))
    xaxis = domain.Axis(50000)
    for i, kernel in enumerate(kernels):
        fgraph = graph.Discrete2d(xaxis, kernel)
        fgraph.set_colors(colors[i%3])
        window.plotter.add_graph('main'+str(i), fgraph)
    window.run()
