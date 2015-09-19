from plotting.app import PlotterWindow
from plotting import graph, domain, widget

r = 1.0
x_0 = 1

NORMAL = """
vec4 f(vec4 x) {
    return vec4(x.x, x.x, 0, 0.5);
}
"""

LOG = """
uniform float r = %f;
vec4 f(vec4 x) {
    float y = x.x*r*(1-x.x);
    return vec4(x.x, y, 0, 0.5);
}
""" % r

LOG2 = """
uniform float r = %f;
vec4 f(vec4 x) {
    float y = x.x*r*r*(1-x.x)*(1-r*x.x*(1-x.x));
    return vec4(x.x, y, 0, 0.5);
}
""" % r

KERNEL = """
    __kernel void f(int length, float r, __global float *gl) {

        gl[1] = r*gl[0]*(1-gl[0]);
        for(int i=1; i < length; i++) {
            gl[2*i] = gl[2*(i-1)+1];
            gl[2*i+1] = r*gl[2*i]*(1-gl[2*i]);
        }
    }
"""




window = PlotterWindow(axis=(3.0,3.0), origin=(1.5,1.5), x_label='x_n', y_label='x_n')

log_domain = domain.Logistic(1000, x_0, r)

axis_domain = domain.Axis(1000)

def update_uniform(self, value):
    log_domain.updateParameterR(value, KERNEL)

window.plotter.add_graph('Logistische Abbildung Fixpunkt', graph.Discrete2d(log_domain, NORMAL))
window.plotter.add_graph('Logistische Abbildung', graph.Discrete2d(axis_domain, LOG))
window.plotter.add_graph('Logistische Abbildung2', graph.Discrete2d(axis_domain, LOG2))


uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('r', r, 0.1)
#uniforms.set_global('n', 1.0)
window.add_widget('manipulate', widget.Uniforms(uniforms, update_callback=update_uniform))
window.run()
