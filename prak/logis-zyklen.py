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

NORMAL = """
vec4 f(vec4 x) {
    return vec4(x.x, 1-0-1.0/x.x, 0, 0.5);
}
"""

NORMAL2 = """
vec4 f(vec4 x) {
    float sqr = x.x*x.x-2.0*x.x-3.0;
    float y = 0.0;
    if(sqr >= 0.0) {
        y = (sqrt(sqr)+x.x+1.0)/(2*x.x);
    }
    return vec4(x.x, y, 0, 0.5);
}
"""

NORMAL3 = """
vec4 f(vec4 x) {
    float sqr = x.x*x.x-2.0*x.x-3.0;
    float y = 0.0;
    if(sqr >= 0.0) {
        y = (-sqrt(sqr)+x.x+1.0)/(2*x.x);
    }
    return vec4(x.x, y, 0, 0.5);
}
"""



window = PlotterWindow(axis=(1.1,0.7), origin=(-2.9,-0.3), x_label='r', y_label='x_n')

axis_domain = domain.Axis(10000)

def update_uniform(self, value):
    log_domain.updateParameterR(value, KERNEL)

window.plotter.add_graph('Periodenverdopplung Simple', graph.Discrete2d(axis_domain, NORMAL))
window.plotter.add_graph('Periodenverdopplung Square +', graph.Discrete2d(axis_domain, NORMAL2))
window.plotter.add_graph('Periodenverdopplung Square -', graph.Discrete2d(axis_domain, NORMAL3))

log_fnc = lambda r, x: r*x*(1-x)
imax = 1500
rn = 1500
pydomain = domain.PythonCodeDomain(int(rn*float(imax)/2))
pydomain.calculata_domain = partial(numerical.bifurcation, log_fnc, 300, rn=rn, imax=imax, xs=2.9, xe=4.0, x_0=lambda i: 0.5*(2*(i%2) -1))
pydomain.recalculate_on_prerender = False
pydomain.dimension = 2
window.plotter.add_graph('iteration', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[0.0,0.0,.0,.1], color_max=[0.0,0.0,0.0,.1])
window.plotter.get_graph('iteration').set_dotsize(0.0015)

lines=  [3.0, 3.45]
for x in lines:
    origin_domain = domain.Domain(2)
    origin_domain.push_data([x, -10.0, x, 10.0])
    window.plotter.add_graph('origin'+str(x), graph.Line2d(origin_domain))
    window.plotter.get_graph('origin'+str(x)).set_colors(color_min=[0.0,0.0,.0,1.0], color_max=[0.0,0.0,0.0,1.0]) 

#uniforms = window.plotter.get_uniform_manager()
#uniforms.set_global('r', r)
#uniforms.set_global('n', 1.0)
#window.add_widget('manipulate', widget.Uniforms(uniforms, update_callback=update_uniform))
window.run()
