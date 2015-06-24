"""
plotter 2d application
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.app import BasicGl
from mygl.objects.plot2d import create_plot_plane_2d, cartesian_domain, x_axis_domain
from mygl.objects.frame import Window
from mygl.matricies import *
from mygl.util import *
from time import time

def plotter_app(kernel, domain, origin=(0.5,0.5), axis=(2.0,2.0)):
    """ single 2d plot """
    app = BasicGl(window_title='Plot2d')

    window = Window(size=(2,2), resolution=(1000, 1000)) # the maximum size seems to be a raise conditional problem
    move_origin_translation = translation_matrix(-1, 1)

    plot = create_plot_plane_2d(origin=origin, axis=axis)
    plot.create_plot('main', kernel, domain)

    start_time = time()
    last_render = 0
    while app.active():
        app.init_cycle()

        if time() - last_render > 1.0/30:
            last_render = time()
            with window:
                plot.buffer_configuration['main']['shader'].uniform('time', time()-start_time)
                plot.render(mat_modelview=move_origin_translation)

        window.render(mat_modelview=move_origin_translation)
        app.swap()


def simplified_plotter_app(kernel, details=5000, xRange=(0.0, 1.0), yRange=(0.0, 1.0)):
    x_length = xRange[1] - xRange[0]
    y_length = yRange[1] - yRange[0]
    plotter_app(kernel, x_axis_domain(details, x_length, xRange[0]), origin=(-xRange[0], abs(yRange[0])), axis=(x_length,y_length))
