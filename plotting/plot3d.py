"""
vertex shader based 3d plot
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from OpenGL.GL import *
from mygl.matricies import * 
from pyrr.matrix44 import create_perspective_projection_matrix, multiply as m4dot, create_from_x_rotation, create_from_y_rotation, create_from_translation, create_from_z_rotation

from mygl import util
from mygl.matricies import *
from mygl.font import GlFont
from functools import partial
from collections import OrderedDict
from mygl.objects.frame import Window
from plotting.util import UniformManager
import math
class PlotPlane3d():

    def __init__(self,axis=(1.0, 1.0), 
        origin=(0.0,0.0), 
        size=(2.0,2.0), 
        x_label=None, 
        y_label='y-axis',
        bg_color=[.9,.9,.9,1]):

        self._uniform_manager = None
        self.plot_matrix = None
        self.graphs = OrderedDict()
        self._render_graphs = True
        self.render_first_time = True
        self.window = Window(size=(2,2), color=bg_color, resolution=(1000, 1000)) # the maximum size seems to be a raise conditional problem
        self._mat_window = None
        self.rotation_x = 0.0
        self.rotation_z = 0.0
        self._zoom = 9.0
        self.prepare()
    def get_uniform_manager(self):
        if self._uniform_manager is None:
            self._uniform_manager = UniformManager()
        return self._uniform_manager
    def render_graphs(self):
        self._render_graphs = True
    def projection_matrix(self):
        return create_perspective_projection_matrix(45.00, 3.0/4.0, 0.1, 1000)
    def zoom(self, zoom):
        self._zoom += zoom-1

    def translate_origin(self, x, z):
        self.rotation_x += float(z)/1000
        self.rotation_z -= float(x)/1000

    def get_plot_matrix(self):
        self.plot_matrix = create_from_x_rotation(self.rotation_x)
        self.plot_matrix = m4dot(self.plot_matrix, create_from_y_rotation(0))
        self.plot_matrix = m4dot(self.plot_matrix, create_from_z_rotation(self.rotation_z))
        self.plot_matrix = m4dot(self.plot_matrix, create_from_translation([1.7,self._zoom,-3]))
        self.plot_matrix = m4dot(self.plot_matrix, create_from_x_rotation(1.1))
        self.plot_matrix = m4dot(self.plot_matrix, create_from_y_rotation(0))
        self.plot_matrix = m4dot(self.plot_matrix, create_from_z_rotation(0.0))
        
        
        self.plot_matrix = m4dot(self.plot_matrix, self.projection_matrix())
        self.plot_matrix = self.plot_matrix.flatten()



        return self.plot_matrix



    def prepare(self):
        self._prepare_window_matrix()
        pass

    def add_graph(self, name, graph):
        """
        creates a plot from kernel and domain
        """
        self.graphs[name] = graph
        graph.set_mat_projection(self.get_plot_matrix())
    def get_graph(self, name):
        return self.graphs[name]

    def _prepare_window_matrix(self):
        self._mat_window = numpy.array([
            1, 0,  0, 0,
            0, 1,  0, 0,
            0, 0,  1, 0,
            -1, 1, 0, 1
        ], dtype=numpy.float32)

    def render(self, mat_modelview=None):
        """
        renders the plane, plot and fonts.
        """
        if mat_modelview is None: mat_modelview = numpy.identity(4)
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if self._uniform_manager.has_updated():
            self._render_graphs = True
        if not self.render_first_time:
            # skip the first time rendering
            if self._render_graphs:
                with self.window:
                    # draw plot
                    for name, graph in self.graphs.items():

                        # set uniforms
                        um = self.get_uniform_manager()
                        for name, value in um.get_global_uniforms().items():
                            graph.shader.uniform(name, value)
                        if name in um.get_local_uniforms():
                            for name, value in um.get_local_uniforms()[name].items():
                                graph.shader.uniform(name, value)

                        graph.set_mat_projection(self.get_plot_matrix())
                        #print self.i_origin, self.i_axis
                        # domain transformation matrix
                        #if hasattr(graph, 'domain'):
                        #    d_transform = graph.domain.transformation_matrix(self.i_axis, self.i_origin)
                        #    if d_transform is None:
                        #        d_transform = matrix_identity(3)
                        #    graph.shader.uniform('mat_domain', d_transform)
                        graph.render()

                self._render_graphs = False
            self.window.render(self._mat_window)

        self.render_first_time = False
