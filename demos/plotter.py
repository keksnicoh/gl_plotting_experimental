"""
frame demo will render a fps counter within
two frame buffer objects.
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.app import BasicGl
from mygl.matricies import *
from mygl.objects.plot2d import create_plot_plane_2d, cartesian_domain
from mygl.objects.frame import Window
from mygl.matricies import *
import math
import numpy
from mygl.app import BasicGl
from mygl.util import *
import numpy
from time import time

def plotter_app(kernel, domain):
    app = BasicGl(window_title='Plot2d')
    window = Window(size=(2,2), resolution=(1000, 1000)) # the maximum size seems to be a raise conditional problem
    move_origin_translation = translation_matrix(-1, 1)

    plot = create_plot_plane_2d(origin=(1.5,1.5), axis=(3.0,3.0))
    plot.create_plot('main', kernel, domain)

    start_time = time()
    while app.active():
        app.init_cycle()

        with window:
            plot.buffer_configuration['main']['shader'].uniform('time', time()-start_time)
            plot.render(mat_modelview=move_origin_translation)

        window.render(mat_modelview=move_origin_translation)
        app.swap()

if __name__ == '__main__':
    KERNEL = """
    float c;
    float tx;
    float ty;
    vec2 f(vec2 x) {
        c = 0.0;
        for (i=0;i < 50;i+=1) {
            tx = x.x + 0.5 -0.02*i;
            ty = x.y - 0.1 + 0.001*i;
            c += sin(50*sqrt(tx*tx + ty*ty)-5*time);
        }
        return vec2(c / 7, vertex_position.w);
    }
    """
    plotter_app(KERNEL, cartesian_domain(200, 3.0, 3.0))
