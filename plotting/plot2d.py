"""
vertex shader based 2d plot
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from OpenGL.GL import *

import numpy
from PIL import ImageFont
import os

from mygl import util
from mygl.matricies import *
from mygl.font import GlFont
from functools import partial
from collections import OrderedDict
from mygl.objects.frame import Window
from plotting.util import UniformManager
import math

FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../resources/fonts'
SHADER_DIR = os.path.dirname(os.path.abspath(__file__))+'/plot2d'

class Plotter():
    """
    class to handle PlotPlane2d
    """
    def __init__(self, axis=(1.0, 1.0), origin=(0.0,0.0), size=(2.0,2.0), x_label=None, y_label='y-axis',
        bg_color=[.9,.9,.9,1]):
        self.move_origin_translation = translation_matrix(-1, 1)
        self.domains = {}
        ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/arial.ttf", 25)
        gl_font = GlFont('', ft)
        gl_font.color = [0.0, 0, 0, 1.0]

        gl_label_font_x = None
        if x_label is not None:
            ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/arial.ttf", 25)
            gl_label_font_x = GlFont(x_label, ft)
            gl_label_font_x.color = [0.0, 0, 0, 1.0]
        gl_label_font_y = None
        if y_label is not None:
            gl_label_font_y = GlFont(y_label, ft)
            gl_label_font_y.color = [0.0, 0, 0, 1.0]

        self.gl_plot = PlotPlane2d(gl_font, gl_label_font_x, gl_label_font_y, bg_color=bg_color)
        self.gl_plot.i_axis = axis
        self.gl_plot.i_origin = origin
        self.gl_plot.o_wh = size
        self.gl_plot.i_axis_units = (axis[0]/5, axis[1]/5)
        self.gl_plot.prepare()
        self.plot_rendered = False



    def add_graph(self, name, graph):
        self.gl_plot.create_plot(name, graph)
    def translate_origin(self, tx, ty):
        tx *= self.gl_plot.i_axis[0]
        ty *= self.gl_plot.i_axis[1]
        tx /= 600*self.gl_plot._scaling[0]
        ty /= 600*self.gl_plot._scaling[1]
        origin = self.gl_plot.i_origin
        self.gl_plot.i_origin = (origin[0]+tx, origin[1]+ty)
        self.gl_plot.prepare()
    def zoom(self, zoom):
        axis = self.gl_plot.i_axis
        self.gl_plot.i_axis = (axis[0]*zoom, axis[1]*zoom)
        self.gl_plot.i_axis_units = (self.gl_plot.i_axis[0]/10, self.gl_plot.i_axis[1]/10)
        if self.gl_plot.i_axis != (0.0, 0.0):
            self.gl_plot.prepare()
    def render_graphs(self):
        self.gl_plot.render_graphs = True
    def get_graph(self, name):
        return self.gl_plot.get_graph(name)
    def render(self):
        self.gl_plot.render(mat_modelview=self.move_origin_translation)

    def get_uniform_manager(self):
        return self.gl_plot.get_uniform_manager()

class PlotPlane2d():
    """
    renders a 2d plotting plane within a
    opengl render cycle
    """
    def __init__(self, gl_font, gl_label_font_x, gl_label_font_y, bg_color):
        self._gl_font = gl_font
        self._gl_label_font_x = gl_label_font_x
        self._gl_label_font_y = gl_label_font_y
        self._mat_label_x = None
        self._mat_label_y = None
        """ size of the main plane in outer plane coords """
        self.o_wh = (2.0, 2.0)
        """ border sizes in outer plane coords """
        self.i_border = (.30, .025, .035, .20)
        """ axis size in plot plane coords """
        self.i_axis = (4.0, 4.0)
        """ axis unit size in plot plane coords """
        self.i_axis_units = (0.5, 0.1)
        """ axis origin position in plot plane coords """
        self.i_origin = (0.0, 0.0)

        """ decimal precision for axis """
        self.precision_axis = (2,2)

        """ internal stuff """
        self._uniforms = {}
        self._unit_count = None
        self._unit_w = None
        self._scaling = None
        self._draw_plane_indicies = None
        self._draw_line_indicies = None
        self._plane_vao = None
        self._plane_vbo = None
        self._uniform_manager = None
        self.widgets = OrderedDict()
        self.graphs = OrderedDict()
        self.plane_shader = None
        self.window = Window(size=(2,2), color=bg_color, resolution=(1000, 1000)) # the maximum size seems to be a raise conditional problem
        self.render_graphs = True
        self.render_first_time = True


    def prepare(self):
        self._prepare_scalings()
        self._prepare_outer_matrix()
        self._prepare_plot_matrix()
        self._prepare_window_matrix()
        self._prepare_plane()
        self.render_graphs = True


    def get_uniform_manager(self):
        if self._uniform_manager is None:
            self._uniform_manager = UniformManager()
        return self._uniform_manager

    def get_graph(self, name):
        return self.graphs[name]

    def _prepare_plane(self):
        """ XXX make me nice """
        self.plane_shader = util.Shader(
            vertex=open(SHADER_DIR+'/plane.vert.glsl').read(),
            fragment=open(SHADER_DIR+'/plane.frag.glsl').read(),
            link=True)

        self._uniforms['mat_plane'] = self.plane_shader.uniformLocation('mat_plane')
        self._uniforms['mat_modelview'] = self.plane_shader.uniformLocation('mat_modelview')

        verticies = [
                # main plane - note that the mainplane is scaled so the mat_plane
                # matrix will it transform to the correct coordinates
                -self.i_border[0]/self._scaling[0], self.i_border[1]/self._scaling[1],
                -self.i_border[0]/self._scaling[0], -(self.o_wh[1]-self.i_border[1])/self._scaling[1],
                (self.o_wh[0]-self.i_border[0])/self._scaling[0], -(self.o_wh[1]-self.i_border[1])/self._scaling[1],
                (self.o_wh[0]-self.i_border[0])/self._scaling[0], -(self.o_wh[1]-self.i_border[1])/self._scaling[1],
                (self.o_wh[0]-self.i_border[0])/self._scaling[0], self.i_border[1]/self._scaling[1],
                -self.i_border[0]/self._scaling[0], self.i_border[1]/self._scaling[1],

                # axes
                0, -self.o_wh[1], self.o_wh[0], -self.o_wh[1], #x
                0, 0, 0, -self.o_wh[1], #y
                ]

        colors = [
                1.0, 1.0, 1.0, 0.0, # outer box XXX Remove outer box...
                1.0, 1.0, 1.0, 0.0,
                1.0, 1.0, 1.0, 0.0,
                1.0, 1.0, 1.0, 0.0,
                1.0, 1.0, 1.0, 0.0,
                1.0, 1.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0, #lines
                0.0, 0.0, 0.0, 1.0,
                0.0, 0.0, 0.0, 1.0,
                0.0, 0.0, 0.0, 1.0,
        ]

        char_width=0.03
        x_len = 0
        y_len = 0

        if self._gl_label_font_x is not None:
            x_len = len(self._gl_label_font_x.text)
        if self._gl_label_font_y is not None:
            y_len = len(self._gl_label_font_y.text)
        self._mat_label_x = numpy.array([
            1,0,0,0,
            0,1,0,0,
            0,0,1,0,
            -x_len*char_width/2,-0.92,0,1,
        ], dtype=numpy.float32)
        self._mat_label_y = numpy.array([
            0,1,0,0,
            -1,0,0,0,
            0,0,1,0,
            -0.98,-y_len*char_width/2,0,1,
        ], dtype=numpy.float32)

        self._fonts = []
        for u in range(1, self._unit_count[0]+1):
            verticies.append(self._unit_w[0]*u)
            verticies.append(-self.o_wh[1]+0.02)
            verticies.append(self._unit_w[0]*u)
            verticies.append(-self.o_wh[1]-0.02)
            colors += [0.0, 0.0, 0.0, 1.0]
            colors += [0.0, 0.0, 0.0, 1.0]
            self._fonts.append([
                ('{:.'+str(self.precision_axis[0])+'f}').format(u*(self.i_axis[0]/self._unit_count[0])-self.i_origin[0]),
                (self._unit_w[0]*u+self.i_border[0]-0.05)*self._scaling[0],
                (-self.o_wh[1]+(self.i_border[3])*0.5+0.04)
            ])

        # y axis
        for u in range(0, self._unit_count[1]):
            verticies.append(0.02)
            verticies.append(-self._unit_w[1]*u)
            verticies.append(-0.02)
            verticies.append(-self._unit_w[1]*u)
            colors += [0.0, 0.0, 0.0, 1.0]
            colors += [0.0, 0.0, 0.0, 1.0]
            self._fonts.append([
                ('{:.'+str(self.precision_axis[1])+'f}').format(self.i_axis[1]-u*self.i_axis[1]/self._unit_count[1]-self.i_origin[1]),
                (0.025+0.10)*self._scaling[0],
                (-(self._unit_w[1])*u-self.i_border[1])*self._scaling[1]
            ])

        self._draw_plane_indicies = (0, 6)
        self._draw_line_indicies = (6, 4+self._unit_count[0]*2+self._unit_count[1]*2)

        # convert data into valid data format
        verticies = numpy.array(verticies, dtype=numpy.float32)
        colors = numpy.array(colors, dtype=numpy.float32)

        self._plane_vao = util.VAO()
        self._plane_vbo = util.VBO(2)

        with self._plane_vao:
            # plane verticies
            with self._plane_vbo.get(0):
                glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(verticies), verticies, GL_STATIC_DRAW)
                glVertexAttribPointer(self.plane_shader.attributeLocation('vertex_position'), 2, GL_FLOAT, GL_FALSE, 0, None)
                glEnableVertexAttribArray(0)

            # place vertex colors
            with self._plane_vbo.get(1):
                glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
                glVertexAttribPointer(self.plane_shader.attributeLocation('vertex_color'), 4, GL_FLOAT, GL_FALSE, 0, None)
                glEnableVertexAttribArray(1)

    def _prepare_scalings(self):
        # specifies the count of units to be rendered
        self._unit_count = (
            int(self.i_axis[0]/self.i_axis_units[0]),
            int(self.i_axis[1]/self.i_axis_units[1])
        )
        # specifies the unit width in plane space
        self._unit_w = (
            self.o_wh[0]/self._unit_count[0],
            self.o_wh[1]/self._unit_count[1]
        )
        # specifies the scaling S of a given vector from
        # plane space in plot space
        self._scaling = (
            1.0-(self.i_border[0]+self.i_border[2])/self.o_wh[0],
            1.0-(self.i_border[1]+self.i_border[3])/self.o_wh[1]
        )

    def _prepare_outer_matrix(self):
        """
        create a matrix that transforms a vector from
        space to outer plane space
        """
        self._mat_plane = numpy.array([
            self._scaling[0], 0, 0, 0,
            0, self._scaling[1], 0, 0,
            0, 0, 1, 0,
            self.i_border[0], -self.i_border[1], 0, 1
        ], dtype=numpy.float32)

    def _prepare_plot_matrix(self):
        """
        creates a matrix that transforms a vector from space
        to the plot plane space
        """
        sx = 2.0/self.i_axis[0]
        sy = 2.0/self.i_axis[1]
        tx = -1+sx*self.i_origin[0]
        ty = -1+sy*self.i_origin[1]
        self._mat_plot = numpy.array([
            sx, 0,  0, 0,
            0, sy,  0, 0,
            0, 0,   1, 0,
            tx, ty, 0, 1
        ], dtype=numpy.float32)

    def _prepare_window_matrix(self):
        self._mat_window = numpy.array([
            self._scaling[0], 0,  0, 0,
            0, self._scaling[1],  0, 0,
            0, 0,   1, 0,
            -1+self.i_border[0], 1-self.i_border[1], 0, 1
        ], dtype=numpy.float32)

    def create_plot(self, name, graph):
        """
        creates a plot from kernel and domain
        """
        self.graphs[name] = graph

    def render(self, mat_modelview=None):
        """
        renders the plane, plot and fonts.
        """
        if mat_modelview is None: mat_modelview = numpy.identity(4)
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if self._uniform_manager.has_updated():
            self.render_graphs = True
        if not self.render_first_time:
            # skip the first time rendering
            if self.render_graphs:
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

                        graph.space_translation(self.i_axis, self.i_origin)
                        #print self.i_origin, self.i_axis
                        # domain transformation matrix
                        #if hasattr(graph, 'domain'):
                        #    d_transform = graph.domain.transformation_matrix(self.i_axis, self.i_origin)
                        #    if d_transform is None:
                        #        d_transform = matrix_identity(3)
                        #    graph.shader.uniform('mat_domain', d_transform)
                        graph.render(self._mat_plot)

                self.render_graphs = False
            self.window.render(self._mat_window)

        # draw plane
        with self.plane_shader:
            glUniformMatrix4fv(self._uniforms['mat_plane'], 1, GL_FALSE, self._mat_plane)
            glUniformMatrix4fv(self._uniforms['mat_modelview'], 1, GL_FALSE, mat_modelview)
            with self._plane_vao:
                glDrawArrays(GL_TRIANGLES,*self._draw_plane_indicies) # draw planes
                glDrawArrays(GL_LINES,*self._draw_line_indicies)      # draw lines

        # draw fonts
        for text in self._fonts:
            self._gl_font.set_text(text[0], text[1], text[2])
            self._gl_font.render(mat_projection=mat_modelview)

        # draw labels
        if self._gl_label_font_x is not None:
            self._gl_label_font_x.render(mat_projection=self._mat_label_x)
        if self._gl_label_font_y is not None: 
            self._gl_label_font_y.render(mat_projection=self._mat_label_y)


        # draw widgets
        for name, widget in self.widgets:
            widget.render()

        self.render_first_time = False
