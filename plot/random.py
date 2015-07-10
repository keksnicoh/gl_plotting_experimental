from plotting.app import PlotterWindow
from plotting import graph, domain, widget

KERNEL_X = """
uniform float t;
uniform float c;
const float M_PI = 3.141592;
vec4 f(vec4 x) {
	//Anlegen eines inhomogenen Magnetfeldes
	float kraft = x.x*t;
	if(kraft > c) {
		x.z = 1.0;
	}
	return vec4(x.x, x.y, x.z, 0.5);
}
"""

window = PlotterWindow(axis=(1.0,1.0), origin=(0,0),
    bg_color=[.083,.03,.2,1])


cdomain = domain.RandomCartesian(50, min_y=0.0, max_y=1.0, min_x=0.0, max_x=1.0, randomPosition=True)
cdomain.transformation_matrix = cdomain.fixed_y_transformation

window.plotter.add_graph('xporb', graph.Discrete2d(cdomain, KERNEL_X))
window.plotter.get_graph('xporb').set_colors(color_min=[.9,0.5,.2,1], color_max=[1.0,.1,.1,1])


uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('t', 1.0)
uniforms.set_global('c', 1.0)
window.add_widget('test', widget.Uniforms(uniforms))
window.run()


window.run()