#-*- coding: utf-8 -*-
"""
Test plot for visualizing simulation
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from plotting.simulation import Simulation

SIMPLE = """
vec4 f(vec4 x) {
    return vec4(x.x, x.y, 0, 0.3);
}

"""


window = PlotterWindow(axis=(3.0,7.0), origin=(-1.0,5.0))
simulation = Simulation(window)
domain = domain.AxisGL(1000, simulation.calculator)
simulation.domain = domain

window.plotter.add_graph('velocity', graph.Discrete2d(domain, SIMPLE))
#uniforms = window.plotter.get_uniform_manager()
#window.add_widget('test', widget.Uniforms(uniforms))


simulation.run()

