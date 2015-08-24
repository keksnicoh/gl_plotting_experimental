from plotting.app import PlotterWindow
from plotting import graph, domain, widget


NORMAL = """
vec4 f(vec4 x) {
    return vec4(x.x, 1-0-1.0/x.x, 0, 0.5);
}
"""

NORMAL2 = """
vec4 f(vec4 x) {
    float sqr = x.x*x.x-2.0*x.x-3.0;
    float y = 0.0;
    if(sqr >= 0.0) {
        y = (sqrt(sqr)+x.x+1.0)/(2*x.x);
    }
    return vec4(x.x, y, 0, 0.5);
}
"""

NORMAL3 = """
vec4 f(vec4 x) {
    float sqr = x.x*x.x-2.0*x.x-3.0;
    float y = 0.0;
    if(sqr >= 0.0) {
        y = (-sqrt(sqr)+x.x+1.0)/(2*x.x);
    }
    return vec4(x.x, y, 0, 0.5);
}
"""



window = PlotterWindow(axis=(6.0,1.0), origin=(-1.0,0.0), x_label='r', y_label='x_n')

axis_domain = domain.Axis(10000)

def update_uniform(self, value):
    log_domain.updateParameterR(value, KERNEL)

window.plotter.add_graph('Periodenverdopplung Simple', graph.Discrete2d(axis_domain, NORMAL))
window.plotter.add_graph('Periodenverdopplung Square +', graph.Discrete2d(axis_domain, NORMAL2))
window.plotter.add_graph('Periodenverdopplung Square -', graph.Discrete2d(axis_domain, NORMAL3))

#uniforms = window.plotter.get_uniform_manager()
#uniforms.set_global('r', r)
#uniforms.set_global('n', 1.0)
#window.add_widget('manipulate', widget.Uniforms(uniforms, update_callback=update_uniform))
window.run()
