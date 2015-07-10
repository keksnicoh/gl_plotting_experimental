from plotting.app import PlotterWindow
from plotting import graph, domain
from plotting import widget
KERNEL = """

uniform float x0;
uniform float r;

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
    x.y = x0;
    for(int i=1; i <= int(x.x);i++) {
        x.y = g(r, x.y);
    }
    return vec4(x.x, x.y, 1.0, 1.0);
}
"""

window = PlotterWindow(axis=(200,0.6), origin=(0.0,-0.4))
domain = domain.Series(201)
window.plotter.add_graph('bifurkation', graph.Discrete2d(domain, KERNEL))

r=3.1
eps=0.0001
uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('x0', 1-1/r+eps)
uniforms.set_global('r', r)
window.add_widget('test', widget.Uniforms(uniforms, size=(0.6, 0.6)))


window.run()
