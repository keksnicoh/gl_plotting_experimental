#-*- coding: utf-8 -*-
"""
OpenGL Kernel for lyapunov exponent
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain

SIMPLE = """
float g(float r, float x) {
    return log(abs(r * cos(x)));
}

float h(float r, float x) {
    return log(abs(r - 2*r*x));
}

vec4 f(vec4 x) {
    float y0 = x.y;// = g(x.x, x.y);
    float summe = 0;
    float n = 1000;
    for (int i = 1; i < n - 1; i+=1) {
        y0 = h(x.x, y0);
        summe += y0;
    }
    return vec4(x.x, summe/n, 0, 0.3);
}
"""


window = PlotterWindow(axis=(3.0,7.0), origin=(-1.0,5.0))
domain = domain.Cartesian(100, min_y=0.01)
domain.transformation_matrix = domain.fixed_y_transformation
window.plotter.add_graph('lyapunov', graph.Discrete2d(domain, SIMPLE))
window.run()
