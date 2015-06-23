"""
frame demo will render a fps counter within
two frame buffer objects.
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.app import BasicGl
from mygl.matricies import *
from mygl.objects.plot2d import create_plot_plane_2d
from mygl.objects.frame import Window
from mygl.matricies import *
import math
import numpy
from mygl.app import BasicGl
from mygl.util import *
import numpy
from time import time
if __name__ == '__main__':
    app = BasicGl(window_title='frame demo. pres R to increase resolution')
    plot = create_plot_plane_2d(origin=(0.5,0.5))

    dim = 90
    data2 = numpy.zeros(dim*dim*3)
    for x in range(0, dim):
        for y in range(0, dim):
            xx = float(x)/dim -0.5
            yy = float(y)/dim -0.5
            data2[3*dim*x+3*y] = float(x)/dim -0.5
            data2[3*dim*x+3*y+1] = float(y)/dim -0.5
            data2[3*dim*x+3*y+2] = 0

    plot.init_point_buffer({
        'second': {
            'length': dim*dim*3,
            'enable_z': 1
        }
    })



    window = Window(size=(2,2), resolution=(1000, 1000)) # the maximum size seems to be a raise conditional problem
    move_origin_translation = translation_matrix(-1, 1)

    #plot.submit_data('main', sinus)


    start_time = time()
    while app.active():
        app.init_cycle()
        with window:
            # UPDATE ME IN SHADER :)
            for x in range(0, dim*dim):
                data2[3*x+2] = math.sin(math.sqrt(data2[3*x+0]**2+data2[3*x+1]**2)*50-(time()+start_time)*10)
                data2[3*x+2] += math.sin(math.sqrt((data2[3*x+0]-0.05)**2+(data2[3*x+1]+0.0)**2)*50-(time()+start_time)*10)
                data2[3*x+2] += math.sin(math.sqrt((data2[3*x+0]+0.05)**2+(data2[3*x+1]-0.0)**2)*50-(time()+start_time)*10)

            plot.submit_data('second', data2)
            plot.render(mat_modelview=move_origin_translation)
        window.render(mat_modelview=move_origin_translation)
        app.swap()
