from plotting.app import PlotterWindow
from plotting import graph, domain

KERNEL = """
vec4 f(vec2 pc) {
    float dx=0;
    float fx = 0;
    float tx = pc.x + -3;
    float ty = pc.y + +0.5;
    fx += sin(sqrt(tx*tx+ty*ty)-10*t)+1;
    tx = pc.x + 3;
    ty = pc.y + +0.5;
    fx += sin(sqrt(tx*tx+ty*ty)-10*t+5)+1;
    tx = pc.x + 8;
    ty = pc.y + +6;
    fx += sin(sqrt(tx*tx+ty*ty)-10*t+2)+1;
    return vec4(fx/6, 1-fx/6, sin(10*fx), 1);
    discard;
}
"""

window = PlotterWindow(axis=(30.0,30.0), origin=(15.0, 15.0), plot_time=True)
window.plotter.add_graph('bla', graph.Field2d(KERNEL))
window.run()
