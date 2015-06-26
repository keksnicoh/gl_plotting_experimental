"""
plotting demo of bifurkationsdiagramme
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.plot2d import Plot2d
import math
import numpy

if __name__ == '__main__':

    # sinus fit
    n = 100000
    sinus = numpy.zeros(n*2)
    for i in range(0, n):
        sinus[2*i] = 1.0/n * i
        sinus[2*i+1] = math.cos(20*1.0/n*i)/2+1.0/2

    data = {
        'sinus': {
            'points': sinus,
            'color': [0.0,0.6,0,0.2],
            'dot_size': 0.005
        }
    }
    plot = Plot2d(data)
    while plot.active(): plot.show()

