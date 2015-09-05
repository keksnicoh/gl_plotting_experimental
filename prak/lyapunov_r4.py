from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from numpy import log, abs
import numpy

EPS = 0.00001
X0 = 0.9
R = 4.00
N = 200
_TRACK_LEN = N

logf = lambda x : R*x*(1-x)
dlogf = lambda x : R-2*R*x

data1 = numpy.zeros(2*_TRACK_LEN)
data2 = numpy.zeros(2*_TRACK_LEN)
data3 = numpy.zeros(2*_TRACK_LEN)

# RENORMIERT 

sum = 0.0 
x0 = X0
for i in range(1, N):
    x0 = logf(x0)
    sum += log(abs(logf(x0+EPS)-logf(x0))/EPS)
    data1[i*2] = i 
    data1[i*2+1] = sum/i

# ANALYTISCH
x0 = X0
sum = log(abs(dlogf(x0)))
for i in range(1, N):
    x0 = logf(x0)
    sum += log(abs(dlogf(x0)))
    data2[i*2] = i 
    data2[i*2+1] = sum/i

# DEF
x0 = X0
x0_eps = x0 + EPS
for i in range(1, N):
    x0 = logf(x0)
    x0_eps = logf(x0_eps)
    data3[i*2] = i 
    data3[i*2+1] = log(abs(x0_eps-x0)/EPS)/i

window = PlotterWindow(axis=(N, 0.78), origin=(0,0.0), x_label='iterations', y_label='lambda(x)')
window.plotter.set_precision_axis((0, 3))

renormiert_domain = domain.Domain(_TRACK_LEN)
renormiert_domain.push_data(data1)
window.plotter.add_graph('renomiert', graph.Discrete2d(renormiert_domain))
window.plotter.get_graph('renomiert').set_colors([1.0,0,0.0,1], [1.0,0,0.0,1])

analytisch_domain = domain.Domain(_TRACK_LEN)
analytisch_domain.push_data(data2)
window.plotter.add_graph('analytisch', graph.Discrete2d(analytisch_domain))

analytisch_domain = domain.Domain(_TRACK_LEN)
analytisch_domain.push_data(data3)
window.plotter.add_graph('def', graph.Discrete2d(analytisch_domain))

window.run()

