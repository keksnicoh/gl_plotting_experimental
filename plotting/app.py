#-*- coding: utf-8 -*-
"""
PlotterWindow
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from plotting import domain, graph
from plotting.plot2d import *
from mygl.app import BasicGl
from mygl.glfw import *
from mygl.matricies import *
from collections import OrderedDict
from time import time
import numpy
ORIGIN_TRANSLATION_INTENSITY = 15

class PlotterWindow():
    """
    plotting window implements basic interaction
    e.g. mouse, keyboard, scrolling, ...
    """
    TIME_TO_RERENDER = 0.05

    def __init__(self, axis=(1.0, 1.0), origin=(0.0,0.0), plot_time=False, x_label=None, y_label=None, bg_color=[.9,.9,.9,1], plotter=Plotter):
        self.app = BasicGl(window_title='plot')
        self.plotter = plotter(axis=axis, origin=origin, size=(2.0,2.0), x_label=x_label, y_label=y_label, bg_color=bg_color)
        self._plot_time = plot_time
        if self._plot_time:
            self.plotter.get_uniform_manager().set_global('t', 0.0)
        self._widgets = OrderedDict()

    def run(self):
        self.initRun()
        # main cycle
        while self.app.active():
            self.runCycle()

    def initRun(self):
        # init gl
        glClearColor(1,1,1,1)
        glEnable (GL_BLEND);
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        self.start_time = time()
        self.um = self.plotter.get_uniform_manager()

    def runCycle(self):
        self.app.init_cycle()

        if self._plot_time and time() - self.start_time - self.um.get_global('t') > self.TIME_TO_RERENDER:

            self.plotter.get_uniform_manager().set_global('t', time()-self.start_time)
            self.plotter.render_graphs()

        active_keyboard = self.app.keyboardActive
        keyboard_captured = False
        mouse_captured = False
        mouse_drag = (self.app.get_mouse_drag(0), self.app.get_mouse_drag(1))
        # widget controlling
        active_widget = self.get_active_widget()
        if active_widget is not None:

            active_widget.set_mouse(self.app.mouse)
            active_widget.set_cursor(self.app.get_cursor_absolute_normalized())
            active_widget.set_keyboard_active(active_keyboard)
            keyboard_captured = active_widget.capture_keyboard()
            mouse_captured = active_widget.capture_mouse()

        # keyboard events if keyboard is not captures by a widget
        if not keyboard_captured:
            # translations
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

        # mouse events if mouse is not captured by a widget
        if not mouse_captured:
            # translations
            if mouse_drag[0] is not None and (mouse_drag[0][0] != 0.0 or mouse_drag[0][1] != 0.0):
                self.plotter.translate_origin(float(mouse_drag[0][0]), float(mouse_drag[0][1]))
            # zooming
            if self.app.scrolled != 0.0:
                self.plotter.zoom(1.0 + 0.01*self.app.scrolled)

        # main plot
        self.plotter.render()

        # render and activate widgets
        for name, widget in self._widgets.items():
            if not mouse_captured:
                active = mouse_drag[0] is None and widget.coords_in(self.app.get_cursor_absolute_normalized())
                widget.set_active(active)

            widget.set_mouse_drag((self.app.normalize(mouse_drag[0]), self.app.normalize(mouse_drag[1])))
            widget.execute()
            widget.render()

        self.app.swap()

    def add_widget(self, name, widget):
        self._widgets[name] = widget

    def get_active_widget(self):
        """ returns the current active widget id """
        for name, widget in self._widgets.items():
            if widget.active:
                return widget

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
