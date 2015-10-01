from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
import numpy

GERADE = """
vec4 f(vec4 x) {
    return vec4(x.x, x.y, x.z, 1.0);
}
"""
LEN = 30
window = PlotterWindow(axis=(LEN,1.0), origin=(0.0,-0.0),
    bg_color=[1.0,1.0,1.0,1], x_label='iterations', y_label='x_n')

window.plotter.set_precision_axis((0, 2))
uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('r', 3.8, 0.0001)
f = lambda x: uniforms.get_global('r')*x*(1-x)

data1=numpy.zeros(LEN*2)
data1[0] = 0
data1[1] = 0.2
for i in range(1, LEN):
    data1[i*2] = i 
    data1[i*2 +1] = f(data1[i*2 -1])

data2=numpy.zeros(LEN*2)
data2[0] = 0
data2[1] = 0.20003
for i in range(1, LEN):
    data2[i*2] = i 
    data2[i*2 +1] = f(data2[i*2 -1])

data3=numpy.zeros(LEN*2)
for i in range(0, LEN):
    data3[i*2] = i 
    data3[i*2 +1] = numpy.abs(data1[2*i+1]-data2[2*i+1])

d1 = domain.Domain(LEN)
d2 = domain.Domain(LEN)
d3 = domain.Domain(LEN)
d1.push_data(data1)
d2.push_data(data2)
d3.push_data(data3)

window.plotter.add_graph('iteration', graph.Discrete2d(d1, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[1.0,0.0,.0,1], color_max=[1.0,0.0,0.0,1])
window.plotter.get_graph('iteration').set_dotsize(0.01)

window.plotter.add_graph('iteration2', graph.Discrete2d(d2, GERADE))
window.plotter.get_graph('iteration2').set_colors(color_min=[0.0,0.0,.0,1], color_max=[0.0,0.0,0.0,1])
window.plotter.get_graph('iteration2').set_dotsize(0.005)

window.plotter.add_graph('iteration3', graph.Line2d(d3, GERADE))
window.plotter.get_graph('iteration3').set_colors(color_min=[0.0,0.0,.0,1], color_max=[0.0,0.0,0.0,1])
window.run()
