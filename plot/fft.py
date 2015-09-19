import numpy as np
import pylab as pl
from matplotlib import pyplot as plt
from plotting.app import PlotterWindow
from plotting import graph, domain, widget

img = pl.imread('3-1ort.bmp',0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))
y_length = len(magnitude_spectrum)
x_length = len(magnitude_spectrum[0])

data = []
for index, x in enumerate(magnitude_spectrum):
	for y in x:
		#print 'x', x
		#print 'y', y
		data.append(index)
		data.append(y)

print len(data), x_length*y_length

window = PlotterWindow(axis=(1.0,1.0), origin=(0.0,0.0), x_label='x_n', y_label='x_n')
fft_domain = domain.Domain(y_length*x_length)
fft_domain.push_data(data)

window.plotter.add_graph('foo', graph.Discrete2d(fft_domain))

window.run()
