from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
import numpy

GERADE = """
uniform float r;
uniform int n = 5;
float l(float x) {
    return r*x*(1-x);
}
vec4 f(vec4 x) {
    float a = x.x;
    for (int i = 0; i < n; i++) {
        a = l(a);
    }
    return vec4(x.x, a, x.z, 1.0);
}
"""

window = PlotterWindow(axis=(1.0,0.7), origin=(0.0,-0.3),
    bg_color=[1.0,1.0,1.0,1], x_label='iterations', y_label='x_n')

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('r', 3.471, 0.001)
pydomain = domain.Axis(500000)
window.plotter.add_graph('iteration', graph.Line2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[0.0,0.0,.0,1], color_max=[0.0,0.0,0.0,1])
window.plotter.get_graph('iteration').set_dotsize(0.0005)

window.add_widget('test', widget.Uniforms(uniforms, font_color=[.0, .0, .0, 1]))
window.run()
