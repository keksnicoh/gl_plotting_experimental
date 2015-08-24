from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
import numpy
LOGISTISCH_MAP = """
uniform float r;
vec4 f(vec4 x) {
    return vec4(x.x, r*x.x*(1-x.x), 1.0, 1.0);
}
"""

GERADE = """
vec4 f(vec4 x) {
    return vec4(x.x, x.y, x.z, 0.5);
}
"""

window = PlotterWindow(axis=(1.5,1.0), origin=(-2.5,0.0),
    bg_color=[0.0,0.0,0.0,1])


log_fnc = lambda r, x: r*x*(1-x)
pydomain = domain.PythonCodeDomain(10000000)
pydomain.calculata_domain = partial(numerical.bifurcation_opt, log_fnc, 300)
pydomain.recalculate_on_prerender = False
pydomain.dimension = 3
window.plotter.add_graph('iteration', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[1.0,1.0,.0,.1], color_max=[0.0,1.0,0.0,.1])
window.plotter.get_graph('iteration').set_dotsize(0.00075)
window.run()
