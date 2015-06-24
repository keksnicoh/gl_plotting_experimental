"""
pretty rough plotting class experiment
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from OpenGL.GL import *
import numpy
from PIL import ImageFont
import os

from mygl import util
from mygl.matricies import *
from mygl.font import GlFont

FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../../resources/fonts'
SHADER_DIR = os.path.dirname(os.path.abspath(__file__))+'/plot2d'

def create_plot_plane_2d(axis=(1.0, 1.0), origin=(0.0,0.0), size=(2.0,2.0)):

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

class PlotPlane2d():
    """
    renders a 2d plotting plane within a
    opengl render cycle
    """
    SHADER_PLANE = 'plane'
    SHADER_POINTS = 'points'

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
        self._prepare_data = None
        self._draw_plane_indicies = None
        self._draw_line_indicies = None
        self._plane_vao = None
        self._plane_vbo = None
        self._plot_vao = None
        self._plot_vbo = None
        self._metadata = None

    def set_data(self, data):
        self._prepare_data = True
        self._data = data
    def set_metadata(self, meta):
        self._metadata = meta
    def prepare(self):
        self._init_shaders()
        self._prepare_scalings()
        self._prepare_outer_matrix()
        self._prepare_plot_matrix()
        self._prepare_plane()
        self._prepare_data = True

    def _init_shaders(self):
        self.shaders = {
            PlotPlane2d.SHADER_PLANE: util.Shader(
                vertex=open(SHADER_DIR+'/plane.vert.glsl').read(),
                fragment=open(SHADER_DIR+'/plane.frag.glsl').read(),
                link=True
            ),

            # XXX Todo custom shader
            PlotPlane2d.SHADER_POINTS: util.Shader(
                vertex=open(SHADER_DIR+'/data.vert.glsl').read(),
                geometry=open(SHADER_DIR+'/data.geom.glsl').read(),
                fragment=open(SHADER_DIR+'/data.frag.glsl').read(),
                link=True
            ),
        }

        self._uniforms['mat_plane'] = self.shaders[self.SHADER_PLANE].uniformLocation('mat_plane')
        self._uniforms['mat_modelview'] = self.shaders[self.SHADER_PLANE].uniformLocation('mat_modelview')
        self._uniforms['point_dot_size'] = self.shaders[self.SHADER_POINTS].uniformLocation('dot_size')
        self._uniforms['point_mat_plane'] = self.shaders[self.SHADER_POINTS].uniformLocation('mat_plane')
        self._uniforms['point_mat_modelview'] = self.shaders[self.SHADER_POINTS].uniformLocation('mat_modelview')
        self._uniforms['point_dot_color'] = self.shaders[self.SHADER_POINTS].uniformLocation('geometry_color')

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
                .9, .9, .9, 1.0, # plot box
                .9, .9, .9, 1.0,
                .9, .9, .9, 1.0,
                .9, .9, .9, 1.0,
                .9, .9, .9, 1.0,
                .9, .9, .9, 1.0,
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
                glVertexAttribPointer(self.shaders[self.SHADER_PLANE].attributeLocation('vertex_position'), 2, GL_FLOAT, GL_FALSE, 0, None)
                glEnableVertexAttribArray(0)

            # place vertex colors
            with self._plane_vbo.get(1):
                glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
                glVertexAttribPointer(self.shaders[self.SHADER_PLANE].attributeLocation('vertex_color'), 4, GL_FLOAT, GL_FALSE, 0, None)
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

        sx = self.o_wh[0]*self._scaling[0]/self.i_axis[0]
        sy = self.o_wh[1]*self._scaling[1]/self.i_axis[1]

        self._mat_plot = numpy.array([
            sx, 0,  0, 0,
            0, sy,  0, 0,
            0, 0,   1, 0,
            tx, ty, 0, 1
        ], dtype=numpy.float32)

    def init_point_buffer(self, configurations):
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

        buffer_configuration = {
            'byte_count': configuration['length'] * 4,
            'vertex_count': configuration['length'],
            'point_base_color': configuration.get('point_base_color', [0,0,0.5,1]),
            'point_size': configuration.get('point_size', 0.02),
            'enable_z': configuration['enable_z'] if 'enable_z' in configuration else False,
            'enable_w': configuration['enable_w'] if 'enable_w' in configuration else False,
            'vao': vao,
            'vbo': vbo,
            'shader': util.Shader(
                vertex=open(SHADER_DIR+'/data.vert.glsl').read(),
                geometry=open(SHADER_DIR+'/data.geom.glsl').read(),
                fragment=open(SHADER_DIR+'/data.frag.glsl').read(),
                link=True
            )
        }

        with buffer_configuration['shader']:
            dot_color = numpy.array(buffer_configuration['point_base_color'], dtype=numpy.float32)
            dot_size = numpy.array(buffer_configuration['point_size'], dtype=numpy.float32)

            # XXX CUSTOM SHADERS!!!
            glUniformMatrix4fv(self._uniforms['point_mat_plane'], 1, GL_FALSE, self._mat_plot)
            glUniform4f(self._uniforms['point_dot_color'], *dot_color)
            glUniform1f(self._uniforms['point_dot_size'], dot_size)

        # enable extra attributes
        extra_attributes = 0
        if buffer_configuration['enable_z']: extra_attributes += 1
        if buffer_configuration['enable_w']: extra_attributes += 1

        # configure vbo
        with vbo.get(0):
            vertex_position = self.shaders[self.SHADER_POINTS].attributeLocation('vertex_position')
            glBufferData(GL_ARRAY_BUFFER, buffer_configuration['byte_count'], None, GL_STATIC_DRAW)
            with vao:
                glVertexAttribPointer(vertex_position, 2+extra_attributes, GL_FLOAT, GL_FALSE, 0, None)
                glEnableVertexAttribArray(0)

        return buffer_configuration

    def submit_data(self, name, data, byte_start=0):
        """
        submit data to vertex buffer object
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
        with self.shaders[self.SHADER_PLANE]:
            glUniformMatrix4fv(self._uniforms['mat_plane'], 1, GL_FALSE, self._mat_plane)
            glUniformMatrix4fv(self._uniforms['mat_modelview'], 1, GL_FALSE, mat_modelview)
            with self._plane_vao:
                glDrawArrays(GL_TRIANGLES,*self._draw_plane_indicies) # draw planes
                glDrawArrays(GL_LINES,*self._draw_line_indicies)      # draw lines

        # draw plot
        for name, configuration in self.buffer_configuration.items():
            with configuration['shader']:
                # XXX different shaders
                glUniformMatrix4fv(self._uniforms['point_mat_modelview'], 1, GL_FALSE, mat_modelview)
                with configuration['vao']:
                    glDrawArrays(GL_POINTS, 0, configuration['vertex_count'])

        # draw fonts
        for text in self._fonts:
            self._gl_font.set_text(text[0], text[1], text[2])
            self._gl_font.render(mat_projection=mat_modelview)


    @classmethod
    def init_cartesian_space(cls, n, w=1.0, h=1.0):
        data = numpy.zeros(n*n*2)
        for x in xrange(n):
            for y in xrange(n):
                data[2*n*x+2*y] = (float(x)/n -0.5)*w
                data[2*n*x+2*y+1] = (float(y)/n -0.5)*h
        return data





