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
KERNEL_LOG = "float g(float r, float x) {return r * x * (1-x);}\n"
KERNEL_LOG_DIFF = "float dg(float r, float x) {return r-2.0*r*x;}\n"
LYAPUNOV_NORMIERT = KERNEL_LOG + """
uniform float eps = 0.00001;
uniform int n;
vec4 f(vec4 x) {
    float x0 = 0.5;
    float summe = x0;
    for (int i = 1; i <= n - 1; i+=1) {
        x0 = g(x.x, x0);
        summe += log(abs(g(x.x, x0+eps)-g(x.x, x0))/eps);
    }
    return vec4(x.x, summe/n, 0, 1.0);
}
"""

LYAPUNOV_ANALYTISCH = KERNEL_LOG_DIFF + KERNEL_LOG + """
uniform int n;
vec4 f(vec4 x) {
    float x0 = 0.6;
    float summe = log(abs(dg(x.x, x0)));
    for (int i = 1; i <= n; i+=1) {
        x0 = g(x.x, x0);
        summe += log(abs(dg(x.x, x0)));
    }
    return vec4(x.x, summe/n, 0, 1.0);
}
"""

LYAPUNOV_DEFINITION = KERNEL_LOG + """
uniform float eps = 0.0001;
uniform int n;
uniform float x_0 = 0.5;
vec4 f(vec4 x) {
    float x0 = x_0;
    float x0eps = x0 + eps;

    for (int i = 0; i < n; i+=1) {
        x0 = g(x.x, x0);
        x0eps = g(x.x, x0eps);
    }
    return vec4(x.x, log(abs((x0eps-x0)/eps))/n, 0, 1.0);
}
"""

window = PlotterWindow(axis=(3.0,6.0), origin=(-1.0,3.6), bg_color=[1,1,1,1], x_label='r', y_label='Bifurkation Logistische Abblidung')

# bifurcation diagram
log_fnc = lambda r, x: r*x*(1-x)
pydomain = domain.PythonCodeDomain(5000*500)
pydomain.calculata_domain = partial(numerical.bifurcation, log_fnc, 300, rn=5000, imax=500, xs=1.0)
pydomain.recalculate_on_prerender = False
pydomain.dimension = 3
window.plotter.add_graph('bifurcation', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('bifurcation').set_colors(color_min=[0.0,0.0,.0,.05], color_max=[0.0,0.0,0.0,.05])
window.plotter.get_graph('bifurcation').set_dotsize(0.00175)

adomain = domain.Axis(100000)
window.plotter.add_graph('lyapunov', graph.Discrete2d(adomain, LYAPUNOV_ANALYTISCH))

origin_domain = domain.Domain(2)
origin_domain.push_data([0.0, 0.0, 10.0, 0.0])
window.plotter.add_graph('origin', graph.Line2d(origin_domain))
window.plotter.get_graph('origin').set_colors(color_min=[0.0,0.0,.0,1.0], color_max=[0.0,0.0,0.0,1.0])


lines= [2.0000000000249916, 3.236067977509959, 3.498561699344952, 3.554640862779951, 3.5666673798649517]
for x in lines:
    origin_domain = domain.Domain(2)
    origin_domain.push_data([x, -10.0, x, 10.0])
    window.plotter.add_graph('origin'+str(x), graph.Line2d(origin_domain))
    window.plotter.get_graph('origin'+str(x)).set_colors(color_min=[0.0,0.0,.0,1.0], color_max=[0.0,0.0,0.0,1.0]) 

uniforms = window.plotter.get_uniform_manager()
#uniforms.set_global('eps', 0.01, 0.000001)
uniforms.set_global('n', 700, 2)
uniforms.set_global('x_0', 0.4, 0.005)
window.add_widget('test', widget.Uniforms(uniforms))




window.run()
