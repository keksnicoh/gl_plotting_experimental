from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
import numpy
from numpy import exp, sin, cos
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

KERNEL_SIN = "float g(float r, float x) {return exp(-r*x*x)*(1-sin(r*x));}\n"
KERNEL_SIN_DIFF = "float dg(float r, float x) {return -2*r*x*g(r,x)-2*r*exp(-r*x*x)*cos(r*x);}\n"

LYAPUNOV_ANALYTISCH = KERNEL_SIN + KERNEL_SIN_DIFF + """
uniform int n = 700;
vec4 f(vec4 x) {
    float x0 = 0.6;
    float summe = log(abs(dg(x.x, x0)));
    for (int i = 1; i <= n; i+=1) {
        x0 = g(x.x, x0);
        summe += log(abs(dg(x.x, x0)));
    }
    return vec4(x.x, summe/(3.0*n), 0, 1.0);
}
"""
window = PlotterWindow(axis=(2.3,1.2), origin=(-4.0,0.1),
    bg_color=[0.0,0.0,0.0,1])



log_fnc = lambda r, x: exp(-r*x**2)*(1-sin(r*x))
imax = 300
rn = 50000
pydomain = domain.PythonCodeDomain(int(rn*float(imax)/2))
pydomain.calculata_domain = partial(numerical.bifurcation, log_fnc, 300, rn=rn, imax=imax, xs=4.0, xe=6.3, x_0=lambda i: 0.5*(2*(i%2) -1))

pydomain.recalculate_on_prerender = False
pydomain.dimension = 3
window.plotter.add_graph('iteration', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[1.0,1.0,.0,.1], color_max=[0.0,1.0,0.0,.1])
window.plotter.get_graph('iteration').set_dotsize(0.00075)

adomain = domain.Axis(80000)
window.plotter.add_graph('lyapunov', graph.Discrete2d(adomain, LYAPUNOV_ANALYTISCH))
window.plotter.get_graph('lyapunov').set_colors(color_min=[1.0,0.0,1.0,1], color_max=[1.0,1.0,0.0,1])
window.run()
