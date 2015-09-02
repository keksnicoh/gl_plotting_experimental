from plotting.app import PlotterWindow
from plotting import graph, domain, widget
from numpy import log, abs, mean
import numpy


X0 = 0.6
R_MIN = 2.0
R_MAX = 4.0
EPS = 0.001
N_ITER = 10000 
_TRACK_LEN = int((R_MAX-R_MIN)/EPS)

logf = lambda r, x : r*x*(1-x)
dlogf = lambda r, x : r-2*r*x

data1 = numpy.zeros(2*_TRACK_LEN)
data2 = numpy.zeros(2*_TRACK_LEN)
print(_TRACK_LEN)
# RENORMIERT 
"""
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
"""
# ANALYTISCH
k = 0
r = R_MIN + EPS
while r < R_MAX:
    x0 = X0
    sum = log(abs(dlogf(r, x0)))
    
    last = []
    for i in range(1, N_ITER):
        x0 = logf(r, x0)
        sum += log(abs(dlogf(r, x0)))
        if i > N_ITER - 6:
            last.append(sum/i)

    data2[k*2] = r 
    data2[k*2+1] = abs(mean(last) - sum/N_ITER)
    r+=EPS
    k+=1
# R= 
#window = PlotterWindow(axis=(N, 0.004), origin=(0.0,-0.4085), x_label='iterations', y_label='lambda(x)')

# R = 3.05
#window = PlotterWindow(axis=(N, 0.005), origin=(0,0.116), x_label='iterations', y_label='lambda(x)')
window = PlotterWindow(axis=(R_MAX - R_MIN, .02), origin=(-R_MIN,0.00), x_label='iterations', y_label='lambda(x)')
#window.plotter.set_precision_axis((0, 3))


#renormiert_domain = domain.Domain(_TRACK_LEN)
#renormiert_domain.push_data(data1)
#window.plotter.add_graph('renomiert', graph.Discrete2d(renormiert_domain))
#window.plotter.get_graph('renomiert').set_dotsize(0.0025)
#window.plotter.get_graph('renomiert').set_colors([0,0,0.8,1], [0,0,0.8,1])

analytisch_domain = domain.Domain(_TRACK_LEN)
analytisch_domain.push_data(data2)
window.plotter.add_graph('analytisch', graph.Line2d(analytisch_domain))
window.plotter.get_graph('analytisch').set_dotsize(0.0025)

origin_domain = domain.Domain(2)
origin_domain.push_data([R_MIN, 0.0, R_MAX, 0.0])
window.plotter.add_graph('origin', graph.Line2d(origin_domain))
window.plotter.get_graph('origin').set_colors(color_min=[0.0,0.0,.0,1.0], color_max=[0.0,0.0,0.0,1.0]) 

window.run()

