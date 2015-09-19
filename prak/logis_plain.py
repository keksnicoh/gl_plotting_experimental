from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
import numpy

GERADE = """
vec4 f(vec4 x) {
    return vec4(x.x, x.y, x.z, 1.0);
}
"""

window = PlotterWindow(axis=(25,0.8), origin=(0.0,-0.2),
    bg_color=[1.0,1.0,1.0,1], x_label='iterations', y_label='x_n')

window.plotter.set_precision_axis((0, 2))
uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('r', 3.8, 0.0001)
log_fnc = lambda x: uniforms.get_global('r')*x*(1-x)
pydomain = domain.PythonCodeDomain(200)
pydomain.calculata_domain = partial(numerical.iteration, log_fnc, 25)
window.plotter.add_graph('iteration', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[0.0,0.0,.0,1], color_max=[0.0,0.0,0.0,1])
window.plotter.get_graph('iteration').set_dotsize(0.0005)


window.run()
