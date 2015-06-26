"""
plotting demo of bifurkationsdiagramme
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.plot2d import Plot2d
import math
import numpy

def bifurk(kernel, r_max = 8.0, r_min = 0.0, n = 100, x_n = 100, i_n = 100):
    """
    bifurkationsdiagramm data
    XXX refactor me and make me fast!
    """
    print('create init data with '+str((n+1)*x_n*2)+'entries')
    data = numpy.zeros((n+1)*x_n*i_n)
    data_index = 0
    for r in [r_max*float(r)/n+r_min for r in range(0,n+1)]:
        for x_0 in range(0,x_n):
            x_0 = r*float(x_0)/x_n-r/2
            for i in range(0,i_n):
                x_0 = kernel(r, x_0)
            data[data_index] = r
            data[data_index+1] = x_0
            data_index+=2
    return data

kernel_log = lambda r, x_0: r*x_0*(1-x_0)
kernel_sin = lambda r, x_0: r*math.cos(x_0)

if __name__ == '__main__':
    r_min = 0.0    # min r value
    r_max = 16.0    # max r value
    y_size = 32.0   # size of the y axis
    origin_y = 16.0 # posizion of origin_y on y axis

    # sinus fit
    n = 10000
    sinus = numpy.zeros(n*2)
    for i in range(0, n):
        sinus[2*i] = r_max/n*i
        sinus[2*i+1] = math.cos(r_max/n*i) * r_max/n*i

    data = {
        'main': {
            'points': bifurk(kernel_sin, r_min=r_min, r_max=r_max, n=100),
            'color': [0,0,0,0.09]
        },

        'fitted_sinus': {
            'points': sinus,
            'color': [0,0.6,0,0.05],
            'dot_size': 0.01
        }
    }
    print('start plotting...')
    plot = Plot2d(data, axis=(r_max-r_min, y_size), origin=(-r_min, origin_y))

    while plot.active(): plot.show()

