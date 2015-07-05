from plotting.app import PlotterWindow
from plotting import graph, domain, widget

KERNEL = """
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
    return vec4(x.x, x0, x.y, 0.2);
}
"""
KERNEL_LY = """

float l(float r, float x) {
    float v = r*(1-2*x);
    return v;
}
float L(float r, float x) {
    float v = r*x*(1-x);
    return v;
}

uniform float a;
uniform float eps = 0.0001;
vec4 f(vec4 x) {
    float y0 = 0.4;// = g(x.x, x.y);
    float summe = y0;
    float n = 1000;
    for (int i = 1; i < n - 1; i+=1) {
        y0 = L(x.x, y0);

        if (i > 200) {
            summe += log(abs(L(x.x, y0+eps)-L(x.x, y0))/eps);
        }

    }
    return vec4(x.x, summe/n+a, 0, 0.5);
}
"""

window = PlotterWindow(axis=(3.0,5.0), origin=(-1.0,1.0),
    x_label='logistic function parameter r',
    y_label='x_200',
    bg_color=[.083,.03,.2,1])
cdomain = domain.Cartesian(1000, min_y=0.01)
cdomain.transformation_matrix = cdomain.fixed_y_transformation

window.plotter.add_graph('bifurkation', graph.Discrete2d(cdomain, KERNEL))
window.plotter.get_graph('bifurkation').set_colors(color_min=[.9,0.5,.2,1], color_max=[1.0,.1,.1,1])
window.plotter.get_graph('bifurkation').set_dotsize(0.00101)


xdomain = domain.Axis(100000)
window.plotter.add_graph('lyapunov', graph.Discrete2d(xdomain, KERNEL_LY))
window.plotter.get_graph('lyapunov').set_colors(color_min=[0,0.8,0.8,1])
window.plotter.get_graph('lyapunov').set_dotsize(0.00101)
uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('a', 0.0)
uniforms.set_global('eps', 0.00001)

window.add_widget('test', widget.Uniforms(uniforms))


window.run()
