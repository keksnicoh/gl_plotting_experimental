#-*- coding: utf-8 -*-
"""
OpenGL Kernel for lyapunov exponent
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget

KERNEL = "float g(float r, float x) {return r * x * (1-x);}\n"
BIFURK = KERNEL + """
uniform float eps = 0.0008;
uniform int n_check = 2;
uniform int n;
vec4 f(vec4 x) {
    float x0 = x.y;
    float summe = x0;
    float x0500 = 0.0f;
    for (int i = 1; i < n; i+=1) {
        x0 = g(x.x, x0);
    }

    x0500 = x.y;
    for (int i = 1;i < n_check; i+=1) {
        x0500 = g(x.x, x0500);
    }

    //float res = exp(-100*abs(x0-x0500));
    float res = exp(-(eps/abs(x0-x0500)));
    return vec4(x.x, x.y, res, 1.0);
}
"""


window = PlotterWindow(axis=(2.45,1.0), origin=(-1.00,-0.0), bg_color=[1,1,1,1], x_label='r', y_label='x_0')

adomain = domain.Cartesian(1000)
window.plotter.add_graph('bifurk', graph.Discrete2d(adomain, BIFURK))
window.plotter.get_graph('bifurk').set_colors(color_min=[.0,.0,.0,1.0], color_max=[1.0,1.0,1.0,1.0])

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('n', 10000)

window.run()
