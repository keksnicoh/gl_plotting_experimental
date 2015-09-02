from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
import numpy


KERNEL = """
vec4 f(vec4 x) {
    return vec4(x.x, 0.0, 0, 0.5);
}
"""


window = PlotterWindow(axis=(10**5,0.0001), origin=(0.0,0.0),
    bg_color=[1.0,1.0,1.0,1])

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('r', 3.113, 0.001)
window.add_widget('test', widget.Uniforms(uniforms, font_color=[.0, .0, .0, 1]))

xdomain = domain.Axis(100000)
window.plotter.add_graph('straight', graph.Discrete2d(xdomain, KERNEL))

def logAbbildung(x, r):
		return r*x*(1-x)

x_real=2.0/3.0
x=0.2
r=3

max_it = 10**8
modul = 10**3
length = int(max_it/modul)

result = []

for i in xrange(max_it):
	x=logAbbildung(x, r)
	if i % modul == 0:
		result.append(i)
		result.append(x_real - x)


#diff = [x_real - x for x in result]

print length
pydomain = domain.Domain(length)
pydomain.push_data(result)

window.plotter.add_graph('iteration', graph.Discrete2d(pydomain))
window.plotter.get_graph('iteration').set_colors(color_min=[.0,0.0,.0,1], color_max=[0.0,.0,.0,1])
window.plotter.get_graph('iteration').set_dotsize(0.005)

window.run()