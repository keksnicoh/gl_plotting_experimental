from plotting.app import PlotterWindow
from plotting import graph, domain, widget

KERNEL_X = """
uniform float t;
const float M_PI = 3.141592;
vec4 f(vec4 x) {
	if(x.x*x.x+x.y*x.y > 1)
		return vec4(x.x, 0, 0, 0.5);
	return vec4(x.x, exp(x.x*sin(t))*sin(x.x)*x.y, 0, 0.5);
}
"""

KERNEL_X_COS = """
uniform float t;
const float M_PI = 3.141592;
vec4 f(vec4 x) {
	if(x.x*x.x+x.y*x.y > 1)
		return vec4(x.x, 0, 0, 0.5);
	return vec4(x.x, exp(x.x*sin(t))*cos(x.x)*x.y, 0, 0.5);
}
"""

window = PlotterWindow(axis=(2.0,2.0), origin=(1.0,1.0), plot_time=True,
    bg_color=[.083,.03,.2,1])


cdomain = domain.Cartesian(500, min_y=-1.0, max_y=1.0, min_x=-1.0, max_x=1.0)
cdomain.transformation_matrix = cdomain.fixed_x_transformation

window.plotter.add_graph('xporb', graph.Discrete2d(cdomain, KERNEL_X))
window.plotter.get_graph('xporb').set_colors(color_min=[.9,0.5,.2,1], color_max=[1.0,.1,.1,1])

window.plotter.add_graph('xporb2', graph.Discrete2d(cdomain, KERNEL_X_COS))
window.plotter.get_graph('xporb2').set_colors(color_min=[.9,0.5,.2,1], color_max=[1.0,.1,.1,1])


uniforms = window.plotter.get_uniform_manager()
window.add_widget('test', widget.Uniforms(uniforms))
window.run()


window.run()