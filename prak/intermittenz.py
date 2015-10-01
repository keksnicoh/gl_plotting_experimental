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

window = PlotterWindow(axis=(10000.0,1.0), origin=(-2.5,0.0),
    bg_color=[1.0,1.0,1.0,1], x_label='iterations', y_label='x_n')


uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('r', 3.801020, 0.0001)
window.add_widget('test', widget.Uniforms(uniforms, font_color=[.0, .0, .0, 1]))
log_fnc = lambda x: uniforms.get_global('r')*x*(1-x)
pydomain = domain.PythonCodeDomain(10000)
pydomain.calculata_domain = partial(numerical.iteration, log_fnc, 10000)
window.plotter.add_graph('iteration', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[0.0,0.0,.0,1], color_max=[0.0,0.0,0.0,1])
window.plotter.get_graph('iteration').set_dotsize(0.005)


window.run()
