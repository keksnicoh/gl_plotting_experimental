#-*- coding: utf-8 -*-
"""
OpenGL Kernel for lyapunov exponent
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget

KERNEL_LOG = "float g(float r, float x) {return r * x * (1-x);}\n"
KERNEL_LOG_DIFF = "float dg(float r, float x) {return r-2.0*r*x;}\n"

LYAPUNOV_ANALYTISCH = KERNEL_LOG_DIFF + KERNEL_LOG + """
uniform int n=80000;
vec4 f(vec4 x) {
    float x0 = 0.6;
    float summe = log(abs(dg(x.x, x0)));
    for (int i = 1; i <= n; i+=1) {
        x0 = g(x.x, x0);
        summe += log(abs(dg(x.x, x0)));
    }
    return vec4(x.x, summe/n, 1.0, 1.0);
}
"""

window = PlotterWindow(axis=(0.00012, 0.00004), origin=(-2.99990,0.00022), bg_color=[1,1,1,1], x_label='r', y_label='lambda(x)')
window.plotter.set_precision_axis((5, 5))

adomain = domain.Axis(100000)
window.plotter.add_graph('lyapunov', graph.Discrete2d(adomain, LYAPUNOV_ANALYTISCH))
window.plotter.get_graph('lyapunov').set_dotsize(0.005)
window.run()
