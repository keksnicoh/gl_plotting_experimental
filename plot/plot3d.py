from plotting.app import PlotterWindow
from plotting import graph, domain, widget, plot3d

KERNEL_X = """
uniform float t;
vec4 f(vec4 x) {
    
    return vec4(x.x, x.y, sin(5*t-sqrt(40*x.x*x.x+40*x.y*x.y))*sin(5*t-sqrt(40*x.x*x.x+40*x.y*x.y)), 1);
}
"""



window = PlotterWindow(axis=(2.0,2.0), origin=(1.0,1.0), plot_time=True,
    bg_color=[.083,.03,.2,1], plotter=plot3d.PlotPlane3d)


cdomain = domain.Cartesian(750, min_y=-1.0, max_y=1.0, min_x=-1.0, max_x=1.0, dimension=3)
cdomain.transformation_matrix = cdomain.fixed_x_transformation

window.plotter.add_graph('xporb', graph.Graph3d(cdomain, KERNEL_X))
window.plotter.get_graph('xporb').set_colors(color_min=[.9,0.0,.0,1], color_max=[0.0,1.0,.1,1])


window.run()


window.run()