"""
plotting demo of bifurkationsdiagramme
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.plot2d import Plot2d
from mygl.app import BasicGl
import math
import numpy

if __name__ == '__main__':

    # sinus fit
    n = 100000
    sinus = numpy.zeros(n*2)
    for i in range(0, n):
        sinus[2*i] = 1.0/n * i
        sinus[2*i+1] = math.sin(20*1.0/n*i)/2+1.0/2
    cos = numpy.zeros(n*2)
    for i in range(0, n):
        cos[2*i] = 1.0/n * i
        cos[2*i+1] = math.cos(20*1.0/n*i)/2+1.0/2
    sincos = numpy.zeros(n*2)
    for i in range(0, n):
        sincos[2*i] = 1.0/n * i
        sincos[2*i+1] = math.cos(20*1.0/n*i)/2+1.0/2
    sinx2 = numpy.zeros(n*2)
    for i in range(0, n):
        sinx2[2*i] = 1.0/n * i
        sinx2[2*i+1] = math.cos(4*(5.0/n*i)**2)/2+1.0/2

    app = BasicGl()
    plot1 = Plot2d({
        'sinus': {
            'points': sinus,
            'color': [0.0,0.6,0,0.2],
        }
    }, size=(1.0, 1.0), app=app)
    plot2 = Plot2d({
        'sinus': {
            'points': cos,
            'color': [0.7,0.6,0,0.2],
        }
    }, size=(1.0, 1.0), app=app, xy=(0,1))
    plot3 = Plot2d({
        'sinus': {
            'points': sincos,
            'color': [0.6,0.0,0.4,0.2],
        }
    }, size=(1.0, 1.0), app=app, xy=(-1,0))
    plot4 = Plot2d({
        'sinus': {
            'points': sinx2,
            'color': [0.3,0.1,9,0.2],
        }
    }, size=(1.0, 1.0), app=app, xy=(0,0))
    while plot1.active():
        app.init_cycle()
        plot1.gl_plot.render(mat_modelview=plot1.plot_translation)
        plot2.gl_plot.render(mat_modelview=plot2.plot_translation)
        plot3.gl_plot.render(mat_modelview=plot3.plot_translation)
        plot4.gl_plot.render(mat_modelview=plot4.plot_translation)
        app.swap()

