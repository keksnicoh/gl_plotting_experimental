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
uniform float eps = 0.0001;
uniform int n;

vec4 f(vec4 x) {
    float x0 = 0.01;

    float def = lyapunov_definition(n, x.x, x0, eps);
    float analytisch = lyapunov_analytisch(n, x.x, x0);
    return vec4(x.x, abs((analytisch-def)/analytisch), 0, 1.0);
}
"""

window = PlotterWindow(axis=(3.0,6.0), origin=(-1.0,3.6), bg_color=[1,1,1,1], x_label='r', y_label='Bifurkation Logistische Abblidung')

adomain = domain.Axis(1000000)
window.plotter.add_graph('lyapunov', graph.Discrete2d(adomain, LYAPUNOV_COMPARE))

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('n', 1000, 2)
uniforms.set_global('x_0', 0.4, 0.005)




window.run()
