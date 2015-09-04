#-*- coding: utf-8 -*-
"""
OpenGL Kernel for lyapunov exponent
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
from numpy import log
import numpy


KERNEL_LOG = "float g(float r, float x) {return r * x * (1-x);}\n"
KERNEL_LOG_DIFF = "float dg(float r, float x) {return r-2.0*r*x;}\n"

LYAPUNOV_IMPLEMENTATIONEN = """
float lyapunov_analytisch(int n, float r, float x0) {
    float summe = log(abs(dg(r, x0)));
    for (int i = 1; i <= n; i+=1) {
        x0 = g(r, x0);
        summe += log(abs(dg(r, x0)));
    }
    return summe/n;   
}

float lyapunov_definition(int n, float r, float x0, float eps) {
    float x0eps = x0 + eps;

    for (int i = 0; i < n; i+=1) {
        x0 = g(r, x0);
        x0eps = g(r, x0eps);
    }
    return log(abs((x0eps-x0)/eps))/n;    
}

"""
LYAPUNOV_COMPARE = KERNEL_LOG_DIFF + KERNEL_LOG + LYAPUNOV_IMPLEMENTATIONEN + """
uniform float eps = 0.00001;
uniform int n;

vec4 f(vec4 x) {
    float x0 = 0.7;

    float def = lyapunov_definition(int(x.x), x.y, x0, eps);
    if (abs(def) > 10) { 
        def = 100;
    }
    return vec4(x.x, def, 0, 1.0);
}
"""
LYAPUNOV_COMPARE2 = KERNEL_LOG_DIFF + KERNEL_LOG + LYAPUNOV_IMPLEMENTATIONEN + """
uniform float eps = 0.00001;
uniform int n;

vec4 f(vec4 x) {
    float x0 = 0.7;

    float def = lyapunov_analytisch(int(x.x), x.y, x0);
    return vec4(x.x, def, 0, 1.0);
}
"""

N = 140
domain_data = numpy.zeros(N*2)
for i in range(0, N):
    domain_data[i*2] = i 
    domain_data[i*2+1] = 3.05


window = PlotterWindow(axis=(N,0.15), origin=(-1.0,0.10), bg_color=[1,1,1,1], x_label='iterations', y_label='lambda(3.05)')
idomain = domain.Domain(N)
idomain.push_data(domain_data)
window.plotter.add_graph('lyapunov', graph.Line2d(idomain, LYAPUNOV_COMPARE))

idomain.push_data(domain_data)
window.plotter.add_graph('lyapunov2', graph.Discrete2d(idomain, LYAPUNOV_COMPARE2))
window.plotter.get_graph('lyapunov2').set_colors(color_min=[1,0,0,1], color_max=[1,0,0,1])

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('n', 10, 2)
uniforms.set_global('x_0', 0.4, 0.005)




window.run()
