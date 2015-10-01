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
    return vec4(x.x, x.y, x.z, 1.0);
}
"""

window = PlotterWindow(axis=(0.04,0.06), origin=(-3.82,-0.12),
    bg_color=[0.0,0.0,0.0,1])


log_fnc = lambda r, x: r*x*(1-x)
LEN =2000
pydomain = domain.PythonCodeDomain(LEN*500)
pydomain.calculata_domain = partial(numerical.bifurcation, log_fnc, rn=LEN, xs=3.82, xe=3.86,)
pydomain.recalculate_on_prerender = False
pydomain.dimension = 3
window.plotter.add_graph('iteration', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[0.0,0.0,.0,.1], color_max=[0.0,0.0,0.0,.1])
window.plotter.get_graph('iteration').set_dotsize(0.0015)
window.run()
