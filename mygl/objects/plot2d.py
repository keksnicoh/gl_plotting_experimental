"""
vertex shader based 2d plot
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from OpenGL.GL import *
from mygl import util
from mygl.matricies import *
from mygl.font import GlFont
from functools import partial

import numpy
import ImageFont
import os
import math

FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../../resources/fonts'
SHADER_DIR = os.path.dirname(os.path.abspath(__file__))+'/plot2d'

def create_plot_plane_2d(axis=(1.0, 1.0), origin=(0.0,0.0), size=(2.0,2.0)):
    """ helber function to create PlotPlane2d """
    ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", 12)
    gl_font = GlFont('', ft)
    gl_font.color = [0.0, 0, 0, 1.0]
    gl_plot = PlotPlane2d(gl_font)
    gl_plot.i_axis = axis
    gl_plot.i_origin = origin
    gl_plot.o_wh = size
    gl_plot.i_axis_units = (axis[0]/10, axis[1]/10)

    gl_plot.prepare()
    return gl_plot

def cartesian_domain(n, w=1.0, h=1.0):
    data = numpy.zeros(n*n*2)
    for x in range(0, n):
        for y in range(0, n):
            data[2*n*x+2*y] = (float(x)/n -0.5)*w
            data[2*n*x+2*y+1] = (float(y)/n -0.5)*h
    return (data, math.sqrt)
def x_axis_domain(n, w=5.0):
    data = numpy.zeros(n*2)
    for x in range(0, n):
        data[2*x] = (float(x)/n -0.5)*w
        data[2*x+1] = 0
    return (data, partial(max, 0.002))
class PlotPlane2d():
    """
    renders a 2d plotting plane within a
    opengl render cycle
    """
    KERNEL_PLACEHOLDER = 'vec4 f(vec4 x){return vec2(x.xy, 1, 0);}'
    def __init__(self, gl_font):
        self._gl_font = gl_font

        """ size of the main plane in outer plane coords """
        self.o_wh = (2.0, 2.0)
        """ border sizes in outer plane coords """
        self.i_border = (.15, .025, .025, .1)
        """ axis size in plot plane coords """
        self.i_axis = (4.0, 4.0)
        """ axis unit size in plot plane coords """
        self.i_axis_units = (0.5, 0.1)
        """ axis origin position in plot plane coords """
        self.i_origin = (0.0, 0.0)

        """ internal stuff """
        self._uniforms = {}
        self._unit_count = None
        self._unit_w = None
        self._scaling = None
        self._draw_plane_indicies = None
        self._draw_line_indicies = None
        self._plane_vao = None
        self._plane_vbo = None
        self.buffer_configuration = None
        self.plane_shader = None
        self.init_point_buffer()

    def prepare(self):
        self._init_shaders()
        self._prepare_scalings()
        self._prepare_outer_matrix()
        self._prepare_plot_matrix()
        self._prepare_plane()

    def _init_shaders(self):
        self.plane_shader = util.Shader(
            vertex=open(SHADER_DIR+'/plane.vert.glsl').read(),
            fragment=open(SHADER_DIR+'/plane.frag.glsl').read(),
            link=True)

        self._uniforms['mat_plane'] = self.plane_shader.uniformLocation('mat_plane')
        self._uniforms['mat_modelview'] = self.plane_shader.uniformLocation('mat_modelview')

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

    def _prepare_plane(self):
        """ XXX make me nice """
        verticies = [
                # main plane - note that the mainplane is scaled so the mat_plane
                # matrix will it transform to the correct coordinates
                -self.i_border[0]/self._scaling[0], self.i_border[1]/self._scaling[1],
                -self.i_border[0]/self._scaling[0], -(self.o_wh[1]-self.i_border[1])/self._scaling[1],
                (self.o_wh[0]-self.i_border[0])/self._scaling[0], -(self.o_wh[1]-self.i_border[1])/self._scaling[1],
                (self.o_wh[0]-self.i_border[0])/self._scaling[0], -(self.o_wh[1]-self.i_border[1])/self._scaling[1],
                (self.o_wh[0]-self.i_border[0])/self._scaling[0], self.i_border[1]/self._scaling[1],
                -self.i_border[0]/self._scaling[0], self.i_border[1]/self._scaling[1],

                # coord plane
                0, 0,
                0, -self.o_wh[1],
                self.o_wh[0], -self.o_wh[1],
                self.o_wh[0], -self.o_wh[1],
                self.o_wh[0], 0,
                0, 0,

                # axes
                0, -self.o_wh[1], self.o_wh[0], -self.o_wh[1], #x
                0, 0, 0, -self.o_wh[1], #y
                ]

        colors = [
                1.0, 1.0, 1.0, 1.0, # outer box XXX Remove outer box...
                1.0, 1.0, 1.0, 1.0,
                1.0, 1.0, 1.0, 1.0,
                1.0, 1.0, 1.0, 1.0,
                1.0, 1.0, 1.0, 1.0,
                1.0, 1.0, 1.0, 1.0,
                .9, .9, .9, 9.0, # plot box
                .9, .9, .9, 9.0,
                .9, .9, .9, 9.0,
                .9, .9, .9, 9.0,
                .9, .9, .9, 9.0,
                .9, .9, .9, 9.0,
                0.0, 0.0, 0.0, 1.0, #lines
                0.0, 0.0, 0.0, 1.0,
                0.0, 0.0, 0.0, 1.0,
                0.0, 0.0, 0.0, 1.0,
        ]

        self._fonts = []
        for u in range(1, self._unit_count[0]+1):
            verticies.append(self._unit_w[0]*u)
            verticies.append(-self.o_wh[1]+0.02)
            verticies.append(self._unit_w[0]*u)
            verticies.append(-self.o_wh[1]-0.02)
            colors += [0.0, 0.0, 0.0, 1.0]
            colors += [0.0, 0.0, 0.0, 1.0]
            self._fonts.append([
                '{:.2f}'.format(u*(self.i_axis[0]/self._unit_count[0])-self.i_origin[0]),
                (self._unit_w[0]*u+self.i_border[0]-0.05)*self._scaling[0],
                (-self.o_wh[1]+(self.i_border[3])*0.5)
            ])
        for u in range(0, self._unit_count[1]):
            verticies.append(0.02)
            verticies.append(-self._unit_w[1]*u)
            verticies.append(-0.02)
            verticies.append(-self._unit_w[1]*u)
            colors += [0.0, 0.0, 0.0, 1.0]
            colors += [0.0, 0.0, 0.0, 1.0]
            self._fonts.append([
                '{:.2f}'.format(self.i_axis[1]-u*self.i_axis[1]/self._unit_count[1]-self.i_origin[1]),
                (0.025)*self._scaling[0],
                (-(self._unit_w[1])*u-self.i_border[1]+0.01)*self._scaling[1]
            ])

        self._draw_plane_indicies = (0, 12)
        self._draw_line_indicies = (12, 4+self._unit_count[0]*2+self._unit_count[1]*2)

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
        tx = self.i_border[0]+self.o_wh[1]*self.i_origin[0]/self.i_axis[0]*self._scaling[0]
        ty = -self.i_border[1]-(self.o_wh[1]-self.o_wh[1]*self.i_origin[1]/self.i_axis[1])*self._scaling[1]

        sx = (self.o_wh[0])*self._scaling[0]/self.i_axis[0]
        sy = (self.o_wh[1])*self._scaling[1]/self.i_axis[1]

        self._mat_plot = numpy.array([
            sx, 0,  0, 0,
            0, sy,  0, 0,
            0, 0,   1, 0,
            tx, ty, 0, 1
        ], dtype=numpy.float32)

    def init_point_buffer(self, configurations={}):
        """
        initializes buffer configuration and allows
        to set uniform values for any given plot
        """

        # initialize buffer configuration to indicate that the
        # buffers are not setup in case this function got a problem
        self.buffer_configuration = None

        # create new buffer configuration
        buffer_configurations = {}
        for name, configuration in configurations.items():
            buffer_configurations[name] = self._init_plot_buffer(configuration)

        self.buffer_configuration = buffer_configurations

    def _init_plot_buffer(self, configuration):
        """
        creates vao, vbo and returns plot configuration dict
        """
        if not isinstance(configuration, dict):
            configuration = { 'length': configuration }

        # initialize vao/vbo
        vao, vbo = util.VAO(), util.VBO()

        # put kernel function into vertex shader
        vertex_shader = open(SHADER_DIR+'/data.vert.glsl').read()
        vertex_shader_kernel = vertex_shader.replace(self.KERNEL_PLACEHOLDER, configuration['kernel'])
        shader = util.Shader(
            vertex=vertex_shader_kernel,
            geometry=open(SHADER_DIR+'/data.geom.glsl').read(),
            fragment=open(SHADER_DIR+'/data.frag.glsl').read(),
            link=True
        )
        norm = configuration.get('norm', float)
        buffer_configuration = {
            'byte_count': configuration['length'] * 4,
            'vertex_count': configuration['length']/2,
            'point_base_color': configuration.get('point_base_color', [0,0,0.5,1]),
            'point_size': configuration.get('point_size', norm(2.0/configuration['length'])),
            'vao': vao,
            'vbo': vbo,
            'shader': shader
        }
        print(configuration['length']/2)
        # uniforms
        shader.uniform('mat_plane', self._mat_plot)
        shader.uniform('geometry_color', buffer_configuration['point_base_color'])
        shader.uniform('dot_size',  buffer_configuration['point_size'])

        # configure vbo
        with vbo.get(0):
            vertex_position = shader.attributeLocation('vertex_position')
            glBufferData(GL_ARRAY_BUFFER, buffer_configuration['byte_count'], None, GL_STATIC_DRAW)
            with vao:
                glVertexAttribPointer(vertex_position, 2, GL_FLOAT, GL_FALSE, 0, None)
                glEnableVertexAttribArray(0)

        return buffer_configuration

    def create_plot(self, name, kernel, domain):
        """
        creates a plot from kernel and domain
        """
        (domain, norm) = domain
        self.buffer_configuration[name] = self._init_plot_buffer({
            'kernel': kernel,
            'length': len(domain),
            'norm': norm,
        })
        self.submit_domain(name, domain, 0)
        return self.buffer_configuration[name]

    def submit_domain(self, name, data, byte_start=0):
        """
        submits the domain into vertex buffer
        """
        data = numpy.array(data, dtype=numpy.float32)
        byte_count = min(
            ArrayDatatype.arrayByteCount(data),
            self.buffer_configuration[name]['byte_count'])

        vbo = self.buffer_configuration[name]['vbo'].get(0)
        vbo.glBufferSubData(byte_start, byte_count, data)

    def render(self, mat_modelview=None):
        """
        renders the plane, plot and fonts.
        """
        if mat_modelview is None: mat_modelview = numpy.identity(4)
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # draw plane
        with self.plane_shader:
            glUniformMatrix4fv(self._uniforms['mat_plane'], 1, GL_FALSE, self._mat_plane)
            glUniformMatrix4fv(self._uniforms['mat_modelview'], 1, GL_FALSE, mat_modelview)
            with self._plane_vao:
                glDrawArrays(GL_TRIANGLES,*self._draw_plane_indicies) # draw planes
                glDrawArrays(GL_LINES,*self._draw_line_indicies)      # draw lines

        # draw plot
        for name, configuration in self.buffer_configuration.items():
            with configuration['shader']:
                configuration['shader'].uniform('mat_modelview', mat_modelview)
                with configuration['vao']:
                    glDrawArrays(GL_POINTS, 0, configuration['vertex_count'])

        # draw fonts
        for text in self._fonts:
            self._gl_font.set_text(text[0], text[1], text[2])
            self._gl_font.render(mat_projection=mat_modelview)





