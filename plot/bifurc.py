from plotting.app import PlotterWindow
from plotting import graph, domain, widget

BIFURCATION_KERNEL = """
float g(float r, float x) {
    return r*x*(1-x);
}
"""

KERNEL = BIFURCATION_KERNEL + """
uniform float n_b;
vec4 f(vec4 x) {
    float x0 = x.y;
    float x1;
    for (int i = 0; i < n_b; i+=1) {
        x0 = g(x.x, x0);
    }
    return vec4(x.x, x0, x.y, 0.2);
}
"""
KERNEL_LY = BIFURCATION_KERNEL + """
uniform float a;
uniform float eps = 0.0001;
uniform float n_l;
uniform float n_l_min;
vec4 f(vec4 x) {
    float y0 = 0.4;// = g(x.x, x.y);
    float summe = y0;
    float n = n_l;
    for (int i = 1; i < n - 1; i+=1) {
        y0 = g(x.x, y0);

        if (i > n_l_min) {
            summe += log(abs(g(x.x, y0+eps)-g(x.x, y0))/eps);
        }

    }
    return vec4(x.x, summe/n+a, 0, 0.5);
}
"""

window = PlotterWindow(axis=(3.0,5.0), origin=(-1.0,1.0),
    x_label='logistic function parameter r',
    y_label='x_200',
    bg_color=[.083,.03,.2,1])
cdomain = domain.Cartesian(500, min_y=0.01)
cdomain.transformation_matrix = cdomain.fixed_y_transformation

window.plotter.add_graph('bifurkation', graph.Discrete2d(cdomain, KERNEL))
window.plotter.get_graph('bifurkation').set_colors(color_min=[.9,0.5,.2,1], color_max=[1.0,.1,.1,1])
window.plotter.get_graph('bifurkation').set_dotsize(0.00101)


xdomain = domain.Axis(100000)
window.plotter.add_graph('lyapunov', graph.Discrete2d(xdomain, KERNEL_LY))
window.plotter.get_graph('lyapunov').set_colors(color_min=[0,0.8,0.8,1])
window.plotter.get_graph('lyapunov').set_dotsize(0.002)
uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('a', 0.0)
uniforms.set_global('eps', 0.00001)
uniforms.set_global('n_b', 200.0)
uniforms.set_global('n_l', 1000.0)
uniforms.set_global('n_l_min', 200.0)
window.add_widget('test', widget.Uniforms(uniforms, font_color=[.9, .5, .2, 1]))


window.run()
