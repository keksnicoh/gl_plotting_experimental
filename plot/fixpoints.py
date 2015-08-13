from plotting.app import PlotterWindow
from plotting import graph, domain, widget


NORMAL = """
vec4 f(vec4 x) {
    return vec4(x.x, x.x, 0, 0.5);
}
"""

DIF_LOG_FIX1 = """
vec4 f(vec4 x) {
    float fixpoint = 1.0 - 1.0/x.x;

    float y = x.x*(1.0-2.0*fixpoint);
    return vec4(x.x, y, 0, 0.5);
}
"""

DIF_LOG_FIX2 = """
vec4 f(vec4 x) {
    float fixpoint = (sqrt(x.x*x.x-2.0*x.x-3.0) + x.x + 1.0) / (2*x.x);

    //float y = x.x*(1.0-2.0*fixpoint);
    float y = -x.x*x.x*(2.0*fixpoint-1.0)*(2.0*x.x*(fixpoint-1.0)*fixpoint+1.0);

    return vec4(x.x, y, 0, 0.5);
}
"""

DIF_LOG_FIX3 = """
vec4 f(vec4 x) {
    float fixpoint = (-sqrt(x.x*x.x-2.0*x.x-3.0) + x.x + 1.0) / (2*x.x);

    //float y = x.x*(1.0-2.0*fixpoint);
    float y = -x.x*x.x*(2.0*fixpoint-1.0)*(2.0*x.x*(fixpoint-1.0)*fixpoint+1.0);

    return vec4(x.x, y, 0, 0.5);
}
"""

STABLE_ZONE = """
vec4 f(vec4 x) {
    return vec4(x.x, x.y, 0, 0.5);
}
"""



window = PlotterWindow(axis=(6.0,6.0), origin=(3.0,3.0), x_label='x_n', y_label='x_n')


c_domain = domain.Cartesian(500, min_y=-1.0)
c_domain.transformation_matrix = c_domain.fixed_y_transformation
axis_domain = domain.Axis(6000, dot_size=0.003)

#def update_uniform(self, value):
#    log_domain.updateParameterR(value, KERNEL)

window.plotter.add_graph('stable', graph.Discrete2d(c_domain, STABLE_ZONE))
window.plotter.get_graph('stable').set_colors(color_min=[1.0,0.0,0.0,0.2])

window.plotter.add_graph('fix1', graph.Discrete2d(axis_domain, DIF_LOG_FIX1))
window.plotter.get_graph('fix1').set_colors(color_min=[0.0,0.0,1.0,1])

window.plotter.add_graph('fix2', graph.Discrete2d(axis_domain, DIF_LOG_FIX2))
window.plotter.get_graph('fix2').set_colors(color_min=[0.0,1.0,.0,1])

window.plotter.add_graph('fix3', graph.Discrete2d(axis_domain, DIF_LOG_FIX3))
window.plotter.get_graph('fix3').set_colors(color_min=[0.0,.0,0.0,1])

#uniforms = window.plotter.get_uniform_manager()
#uniforms.set_global('r', r)
##uniforms.set_global('n', 1.0)
#window.add_widget('manipulate', widget.Uniforms(uniforms, update_callback=update_uniform))
window.run()
