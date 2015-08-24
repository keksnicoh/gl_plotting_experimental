from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
import numpy
LOGISTISCH_MAP = """
uniform float r;
vec4 f(vec4 x) {
    return vec4(x.x, r*x.x*(1-x.x), 0, 0.5);
}
"""

GERADE = """
vec4 f(vec4 x) {
    return vec4(x.x, x.x, 1, 1);
}
"""

window = PlotterWindow(axis=(1.0,1.0), origin=(-0.0,0.0),
    bg_color=[.9,.9,.9,1])

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('r', 2.75, 0.001)
window.add_widget('test', widget.Uniforms(uniforms, font_color=[.0, .0, .0, 1]))

cdomain = domain.Axis(50)
window.plotter.add_graph('bifurkation', graph.Line2d(cdomain, LOGISTISCH_MAP))
window.plotter.get_graph('bifurkation').set_colors(color_min=[.0,0.0,.0,1], color_max=[0.0,.0,.0,1])

window.plotter.add_graph('gerade', graph.Line2d(cdomain, GERADE))
window.plotter.get_graph('gerade').set_colors(color_min=[.0,0.0,.0,1], color_max=[0.0,.0,.0,1])

log_fnc = lambda x: uniforms.get_global('r')*x*(1-x)
pydomain = domain.PythonCodeDomain(600)
pydomain.calculata_domain = partial(numerical.iteration_attractor_quadruple, log_fnc, 300)
window.plotter.add_graph('iteration', graph.Line2d(pydomain))
window.plotter.get_graph('iteration').set_colors(color_min=[.0,0.0,.0,1], color_max=[0.0,.0,.0,1])

window.run()
