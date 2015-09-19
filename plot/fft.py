from plotting.app import PlotterWindow
from plotting import graph, domain

KERNEL = """
vec4 f(vec2 pc) {
    float h1 = 0.2;
    float h2 = 5;
    float pi = 3.1;
    float delta_y = 0.05;

    float delta1 = 0;
    float delta2 = 10;

    float x = 0;
    float y = 0;
    float x2 = 0;
    float y2 = 0;
    for (int i = 0; i < 4; ++i) {
        x += (sin(pi*pc.y/h1))/(pc.y*pi*abs(h1));
        y += cos(i*delta2*pc.x)*(sin(pi*pc.x/h2))/(pc.x*pi*abs(h2));
    }
    for (int i = 0; i < 4; ++i) {
        x2 += (sin(pi*pc.x/h1))/(pc.x*pi*abs(h1));
        y2 += cos(i*delta2*pc.y)*(sin(pi*pc.y/h2))/(pc.y*pi*abs(h2));
    }

    float res = 0;
    res = x*x*y*y+x2*x2*y2*y2;
    return vec4(8/(2*pi)*1*res, 8/(2*pi)*res, 8/(2*pi)*res, 1);
    discard;
}
"""

window = PlotterWindow(axis=(30.0,30.0), origin=(15.0, 15.0), plot_time=True)
window.plotter.add_graph('bla', graph.Field2d(KERNEL))
window.run()
