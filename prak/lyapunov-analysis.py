from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from numpy import log, abs
import numpy

EPS = 0.00001
X0 = 0.6
R = 3.00
N = 50000
TRACK = 10
_TRACK_LEN = int(float(N)/float(TRACK))

logf = lambda x : R*x*(1-x)
dlogf = lambda x : R-2*R*x

data1 = numpy.zeros(2*_TRACK_LEN)
data2 = numpy.zeros(2*_TRACK_LEN)

# RENORMIERT 

sum = 0.0 
x0 = X0
k = 0
for i in range(1, N):
    x0 = logf(x0)
    sum += log(abs(logf(x0+EPS)-logf(x0))/EPS)
    if not i % TRACK:
        data1[k*2] = i 
        data1[k*2+1] = sum/i
        k += 1

# ANALYTISCH

x0 = X0
sum = log(abs(dlogf(x0)))
k = 0
for i in range(1, N):
    x0 = logf(x0)
    sum += log(abs(dlogf(x0)))
    if not i % TRACK:
        data2[k*2] = i 
        data2[k*2+1] = sum/i
        k += 1

# R= 
#window = PlotterWindow(axis=(N, 0.004), origin=(0.0,-0.4085), x_label='iterations', y_label='lambda(x)')

# R = 3.05
#window = PlotterWindow(axis=(N, 0.005), origin=(0,0.116), x_label='iterations', y_label='lambda(x)')
window = PlotterWindow(axis=(N, 0.01), origin=(0,0.01), x_label='iterations', y_label='lambda(x)')
window.plotter.set_precision_axis((0, 3))


renormiert_domain = domain.Domain(_TRACK_LEN)
renormiert_domain.push_data(data1)
window.plotter.add_graph('renomiert', graph.Discrete2d(renormiert_domain))
window.plotter.get_graph('renomiert').set_dotsize(0.0025)
window.plotter.get_graph('renomiert').set_colors([0,0,0.8,1], [0,0,0.8,1])

analytisch_domain = domain.Domain(_TRACK_LEN)
analytisch_domain.push_data(data2)
window.plotter.add_graph('analytisch', graph.Discrete2d(analytisch_domain))
window.plotter.get_graph('analytisch').set_dotsize(0.0025)

origin_domain = domain.Domain(2)
origin_domain.push_data([0.0, 0.0, N, 0.0])
window.plotter.add_graph('origin', graph.Line2d(origin_domain))
window.plotter.get_graph('origin').set_colors(color_min=[0.0,0.0,.0,1.0], color_max=[0.0,0.0,0.0,1.0]) 

origin_domain = domain.Domain(2)
origin_domain.push_data([700, 0.0, 700, -0.2])
window.plotter.add_graph('marker700', graph.Line2d(origin_domain))
window.plotter.get_graph('marker700').set_colors(color_min=[0.0,0.0,.0,1.0], color_max=[0.0,0.0,0.0,1.0]) 

window.run()

