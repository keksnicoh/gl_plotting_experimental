#-*- coding: utf-8 -*-
"""
OpenGL Kernel for lyapunov exponent
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial

GERADE = """
vec4 f(vec4 x) {
    return vec4(x.x, 6*x.y-4.0, x.z, 1.0);
}
"""
KERNEL_LOG = """
float g(float r, float x) {
    float v = r * x * (1-x);
    return v;
}
uniform float eps;
uniform int n;
uniform int start;
vec4 f(vec4 x) {
    float x0 = 0.4;// = g(x.x, x.y);
    float summe = x0;
    for (int i = 1; i <= n - 1; i+=1) {
        x0 = g(x.x, x0);

        //if (i > start) {
            summe += log(abs(g(x.x, x0+eps)-g(x.x, x0))/eps);
        //}

    }
    return vec4(x.x, summe/n, 0, 1.0);
}
"""


#window = PlotterWindow(axis=(0.002,0.002), origin=(-2.999,0.001))
window = PlotterWindow(axis=(3.0,6.0), origin=(-1.0,4.0), bg_color=[1,1,1,1])
#domain = domain.Cartesian(1000, min_y=0.01)


#window = PlotterWindow(axis=(1.0,1.0), origin=(-0.0,0.0),
#    bg_color=[.9,.9,.9,1])



log_fnc = lambda r, x: r*x*(1-x)
pydomain = domain.PythonCodeDomain(10000*1000)
pydomain.calculata_domain = partial(numerical.bifurcation, log_fnc, 300, rn=10000, imax=1000, xs=1.0)
pydomain.recalculate_on_prerender = False
pydomain.dimension = 3
window.plotter.add_graph('iteration', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[0.0,0.0,.0,.05], color_max=[0.0,0.0,0.0,.05])
window.plotter.get_graph('iteration').set_dotsize(0.00175)

adomain = domain.Axis(100000)
window.plotter.add_graph('lyapunov', graph.Discrete2d(adomain, KERNEL_LOG))

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('eps', 0.00001, 0.000001)
uniforms.set_global('n', 2000, 10)
uniforms.set_global('start', 0, 5)
window.add_widget('test', widget.Uniforms(uniforms))
#window.add_widget('coordinates', widget.Coordinates(window.plotter.gl_plot))


window.run()
