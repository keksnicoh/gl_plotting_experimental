from plotting.app import PlotterWindow
from plotting import graph, domain

LOG_KERNEL = """
float g(float r, float x) {
    return r*x*(1-x);
}
float k(float r, float x) {
    if(x < 0.5) {
        return r*x;
    }
    else {
        return r*(1-x);
    }
}
vec4 f(vec4 x) {
    float x0 = x.y;
    float x1;
    for (int i = 0; i < 200; i+=1) {
        x0 = g(x.x, x0);
    }
    return vec4(x.x, x0, 0, 0.3);
}
"""

SIN_KERNEL = """
vec4 f(vec4 x) {
    float y0 = x.y;
    for (int i = 0; i < 200; i+=1) {
        y0 = x.x * sin(y0);
    }
    return vec4(x.x, y0, 0, 0.3);
}
"""

window = PlotterWindow(axis=(3.0,5.0), origin=(-1.0,1.0))
domain = domain.Cartesian(1000, min_y=0.01)
domain.transformation_matrix = domain.fixed_y_transformation
window.plotter.add_graph('bifurkation', graph.Discrete2d(domain, SIN_KERNEL))
window.run()
