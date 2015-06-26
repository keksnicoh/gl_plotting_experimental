from plotting.app import PlotterWindow
from plotting import graph, domain

KERNEL_SIN = """
vec4 f(vec4 x) {
    x.y = 1.0;
    return vec4(x.x, sin(20*exp(-x.x*x.x)), 0,1);
}
"""

window = PlotterWindow(axis=(3.0,3.0),origin=(1.5,1.5))
domain = domain.Axis(10000)
window.plotter.add_graph('sinexp', graph.Discrete2d(domain, KERNEL_SIN))
window.run()
