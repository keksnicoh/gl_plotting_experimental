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

n = 200
start_time = time()

if __name__ == '__main__':
    app = BasicGl(window_title='blurp')
    window = Window(size=(2,2), resolution=(1000, 1000)) # the maximum size seems to be a raise conditional problem
    move_origin_translation = translation_matrix(-1, 1)

    # XXX
    # - create helper functions
    # - inject vertex shader kernel (parse vertex shader)
    plot = create_plot_plane_2d(origin=(1.5,1.5), axis=(3.0,3.0))
    plot.init_point_buffer({'wave': n*n*2})
    plot.submit_data('wave', plot.init_cartesian_space(n, 3.0, 3.0))

    while app.active():
        app.init_cycle()

        with window:
            plot.buffer_configuration['wave']['shader'].uniform('time', time()-start_time)
            plot.render(mat_modelview=move_origin_translation)

        window.render(mat_modelview=move_origin_translation)
        app.swap()
