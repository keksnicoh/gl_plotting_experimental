#-*- coding: utf-8 -*-
"""
PlotterWindow
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from plotting import domain
from plotting.plot2d import *
from mygl.app import BasicGl

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

            self.plotter.render()
            self.app.swap()
