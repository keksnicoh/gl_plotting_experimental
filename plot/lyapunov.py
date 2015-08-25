#-*- coding: utf-8 -*-
"""
OpenGL Kernel for lyapunov exponent
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

# XXX
# - 3 methoden vergleichen. 
# - bestimmung von feigenbaum über superattraktive punkte. 6-8 stellen

from plotting.app import PlotterWindow
from plotting import graph, domain, widget

KERNEL_SIN = """
float g(float r, float x) {
    float v = r * cos(x);
    return v;
}
float G(float r, float x) {
    float v = r * sin(x);
    return v;
}
uniform float a;
vec4 f(vec4 x) {
    float y0 = 0.4;// = g(x.x, x.y);
    float summe = y0;
    float n = 1000;
    for (int i = 1; i < n - 1; i+=1) {
        y0 = G(x.x, y0);

        if (i > 200) {
            summe += log(abs(g(x.x, y0)));
        }

    }
    return vec4(x.x, summe/n+a, 0, 0.5);
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
    return vec4(x.x, summe/n, 0, 0.5);
}
"""


window = PlotterWindow(axis=(0.002,0.002), origin=(-2.999,0.001))
#window = PlotterWindow(axis=(1.0,1.0), origin=(0.0,0.0))
#domain = domain.Cartesian(1000, min_y=0.01)
domain = domain.Axis(100)
#domain.transformation_matrix = domain.fixed_y_transformation
window.plotter.add_graph('lyapunov', graph.Discrete2d(domain, KERNEL_LOG))
uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('eps', 0.00001, 0.000001)
uniforms.set_global('n', 2000, 10)
uniforms.set_global('start', 0, 5)
window.add_widget('test', widget.Uniforms(uniforms))
window.add_widget('coordinates', widget.Coordinates(window.plotter.gl_plot))


window.run()
