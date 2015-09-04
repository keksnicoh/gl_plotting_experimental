from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from prak import numerical
from functools import partial
import numpy
from numpy import mean
GERADE = """
vec4 f(vec4 x) {
    return vec4(x.x, x.y, x.z, 1.0);
}
"""

NORMAL = """
vec4 f(vec4 x) {
    return vec4(x.x, 1-0-1.0/x.x, 0, 0.5);
}
"""

NORMAL2 = """
vec4 f(vec4 x) {
    float sqr = x.x*x.x-2.0*x.x-3.0;
    float y = 0.0;
    if(sqr >= 0.0) {
        y = (sqrt(sqr)+x.x+1.0)/(2*x.x);
    }
    return vec4(x.x, y, 0, 0.5);
}
"""

NORMAL3 = """
vec4 f(vec4 x) {
    float sqr = x.x*x.x-2.0*x.x-3.0;
    float y = 0.0;
    if(sqr >= 0.0) {
        y = (-sqrt(sqr)+x.x+1.0)/(2*x.x);
    }
    return vec4(x.x, y, 0, 0.5);
}
"""





log_fnc = lambda r, x: r*x*(1-x)

R = 3.0
START = 1000
N = 10000000
LEN = N - START
data = numpy.zeros(2*LEN/91)
data2 = numpy.zeros(2*LEN/91)

x0 = 0.4
j = 0
for k in range(0, LEN):
    x0 = log_fnc(R, x0)
    if k > START and k % 91 == 0:
        data[j*2] = k
        data[j*2+1] = x0 - 2.0/3.0

        #if j > 0:
        #    data2[j*2] = k
        #    data2[j*2+1] = abs(data[j*2+3] - data[j*2+1])/9.0
        j+=1
print(data[len(data)-261])
window = PlotterWindow(axis=(LEN-START,0.0025), origin=(-START,0.00125), x_label='iterations', y_label='x_n')
window.plotter.set_precision_axis((0, 6))
pydomain = domain.Domain(LEN)
pydomain.push_data(data)
window.plotter.add_graph('iteration', graph.Discrete2d(pydomain, GERADE))
window.plotter.get_graph('iteration').set_colors(color_min=[0.0,0.0,.0,1], color_max=[0.0,0.0,0.0,1])
window.plotter.get_graph('iteration').set_dotsize(0.0015)

#pydomain2 = domain.Domain(LEN)
#pydomain2.push_data(data2)
#window.plotter.add_graph('iteration2', graph.Discrete2d(pydomain2, GERADE))
#window.plotter.get_graph('iteration2').set_colors(color_min=[0.0,0.0,.0,1], color_max=[0.0,0.0,0.0,1])
#window.plotter.get_graph('iteration2').set_dotsize(0.0015)




#uniforms = window.plotter.get_uniform_manager()
#uniforms.set_global('r', r)
#uniforms.set_global('n', 1.0)
#window.add_widget('manipulate', widget.Uniforms(uniforms, update_callback=update_uniform))
window.run()
