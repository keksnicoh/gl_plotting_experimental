#-*- coding: utf-8 -*-
"""
Test whether the alignment and transformations are working proper
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from plotting.app import PlotterWindow
from plotting import domain
from plotting import graph
from plotting import widget
from OpenGL.GL import *
KERNEL = """
uniform float t;
vec4 f(vec4 x) {
    float tx = x.x-0.5;
    float ty = x.y-0.5;
    return vec4(x.xy, 5*(
        0.2*exp(sin(t+sqrt(5*tx*tx*sin(t)*sin(t)+ty*ty)))
        +sin(t+sqrt(25*x.x*x.x*sin(t)*sin(t)+x.y*x.y))
    ), 1);
}
"""
KERNEL_SINUS = """
uniform float t;

vec4 f(vec4 x) {
    float tx = x.x +0.5;
    float ty = x.y +0.5;
    x.y = sin(6*tx*t/2)*sin(6*tx)*x.x;
    return vec4(x.xy, 1.0-sin(10*x.x)*sin(10*x.x), 1);
}
"""
KERNEL_TESTGERADE1 = """
vec4 f(vec4 x) {
    x.y = x.x;
    return vec4(x.xy, 0.0, 0.5);
}
"""

axis = domain.Axis(50000)
cartesian = domain.Cartesian(200)
# spawn fixed cartesian domains
minmax_no_y_translation = domain.Cartesian(4, min_y = 0.5, max_y=0.8)
minmax_no_y_translation.transformation_matrix = minmax_no_y_translation.fixed_y_transformation
minmax_no_x_translation = domain.Cartesian(4, min_x = 0.4, max_x=1.2)
minmax_no_x_translation.transformation_matrix = minmax_no_x_translation.fixed_x_transformation

window = PlotterWindow(
    axis=(8.0, 8.0),
    origin=(2.0,4.0),
    plot_time=True,
    x_label='some serious axis [Nm^2/T^3]',
    y_label='I(f(z(THETTA)))/42 [Kg]')

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('a', 5.0)
uniforms.set_global('b', 5.4)
uniforms.set_local('ball', 'b', 5.4)

# test some none coord mapping kernel
window.plotter.add_graph('ball', graph.Discrete2d(cartesian, KERNEL))
window.plotter.get_graph('ball').set_colors(color_min=[.0,0.0,0,1], color_max=[.1,.1,0.4,1])

# check two cartesian domains with either fixed x or fixed y axis
window.plotter.add_graph('translation_testy', graph.Discrete2d(minmax_no_y_translation)) # plot with identity kernel
window.plotter.get_graph('translation_testy').set_colors(color_max=[1.0,.0,0.0,1])
window.plotter.get_graph('translation_testy').set_dotsize(0.006)

window.plotter.add_graph('translation_testx', graph.Line2d(minmax_no_x_translation))# plot with identity kernel
window.plotter.get_graph('translation_testx').set_colors(color_max=[.0,1.0,0.0,1])
window.plotter.get_graph('translation_testx').set_dotsize(0.006)

# check whether coord mapping is transformed proper
window.plotter.add_graph('sinus', graph.Line2d(axis, KERNEL_SINUS))
window.plotter.get_graph('sinus').set_colors(color_min=[1,1,0,1], color_max=[0,0.5,1,1])

# should intersect with ball center and should be a "einhuellende" of sinus
window.plotter.add_graph('test1', graph.Discrete2d(axis, KERNEL_TESTGERADE1))
window.plotter.get_graph('test1').set_colors(color_min=[0.9,0.5,0.9,0.01])
window.plotter.get_graph('test1').set_dotsize(0.01)

window.add_widget('test', widget.Uniforms(uniforms))
window.add_widget('text1', widget.Text('test plot shows whether \neverything works as expected. \nthis text is a wiget, drag/drop \nme with right mouse button. \nyou can even resize me, \njust click my corners dude.', font_color=[1,1,0,1], pos=(.5, .7)))
window.run()

