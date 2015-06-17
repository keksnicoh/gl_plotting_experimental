"""
pretty rough plotting class experiment
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from OpenGL.GL import *
import numpy
import ImageFont
import os

from mygl import util
from mygl.app import BasicGl
from mygl.matricies import *
from mygl.font import GlFont

FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../resources/fonts'

class Plot2d():

    def __init__(self, data=[], axis=(1.0, 1.0), origin=(0.0,0.0)):
        self.app = BasicGl()

        self.plot_translation = translation_matrix(-1, 1)
        ft = ImageFont.truetype (FONT_RESOURCES_DIR+"/courier.ttf", 12)
        gl_font = GlFont('', ft)
        gl_font.color = [0.0, 0, 0, 1.0]
        self.gl_plot = PlotPlane2d(data, gl_font)
        self.gl_plot.i_axis = axis
        self.gl_plot.i_origin = origin
        self.gl_plot.i_axis_units = (axis[0]/10, axis[1]/10)
        self.gl_plot.prepare()
        self._render = True

    def active(self):
        """ indicates that the plot is active """
        return self.app.active()

    def show(self):
        if self._render:
            self.app.init_cycle()
            self.gl_plot.render(mat_modelview=self.plot_translation)
            self.app.swap()
            self._render = False
        else:
            self.app.glwf_cycle()

class PlotPlane2d():
    """
    renders a 2d plotting plane within a
    opengl render cycle
    """
    SHADER_PLANE = 'plane'
    SHADER_POINTS = 'points'

    def __init__(self, data, gl_font):
        """ size of the main plane in outer plane coords """
        self.o_wh = (2.0, 2.0)
        """ border sizes in outer plane coords """
        self.i_border = (.1, .0, .0, .1)
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

        self.set_data(data)
        self._gl_font = gl_font

    def set_data(self, data):
        self._prepare_data = True
        self._data = data

    def prepare(self):
        self._init_shaders()
        self._prepare_scalings()
        self._prepare_outer_matrix()
        self._prepare_plot_matrix()
        self._prepare_plane()
        self._prepare_data = True

    def _init_shaders(self):
        shader_plane = util.Shader()
        shader_plane.attachShader(GL_VERTEX_SHADER, VERTEX_SHADER)
        shader_plane.attachShader(GL_FRAGMENT_SHADER, FRAGMENT_SHADER)
        shader_plane.linkProgram()

        shader_points = util.Shader()
        shader_points.attachShader(GL_VERTEX_SHADER, POINT_VERTEX_SHADER)
        shader_points.attachShader(GL_FRAGMENT_SHADER, FRAGMENT_SHADER)
        shader_points.attachShader(GL_GEOMETRY_SHADER, GEOMETRY_SHADER)
        shader_points.linkProgram()

        self.shaders = {
            PlotPlane2d.SHADER_PLANE: shader_plane,
            PlotPlane2d.SHADER_POINTS: shader_points
        }

        self._uniforms['mat_plane'] = self.shaders[self.SHADER_PLANE].uniformLocation('mat_plane')
        self._uniforms['mat_modelview'] = self.shaders[self.SHADER_PLANE].uniformLocation('mat_modelview')
        self._uniforms['point_mat_plane'] = self.shaders[self.SHADER_PLANE].uniformLocation('mat_plane')
        self._uniforms['point_mat_modelview'] = self.shaders[self.SHADER_PLANE].uniformLocation('mat_modelview')
        self._uniforms['point_dot_size'] = self.shaders[self.SHADER_PLANE].uniformLocation('dot_size')

    def _prepare_scalings(self):
        self._unit_count = (int(self.i_axis[0]/self.i_axis_units[0]), int(self.i_axis[1]/self.i_axis_units[1]))
        self._unit_w = (self.o_wh[0]/self._unit_count[0], self.o_wh[1]/self._unit_count[1])
        self._scaling = (1.0-(self.i_border[0]+self.i_border[2])/self.o_wh[0], 1.0-(self.i_border[1]+self.i_border[3])/self.o_wh[1])

    def _prepare_plane(self):
        self.vao_id = glGenVertexArrays(1)
        self.vbo_id = glGenBuffers(2)

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
                1.0, 1.0, 1.0, 1.0, # outer box
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
                (self._unit_w[0]*u+self.i_border[0]-0.08)*self._scaling[0],
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
                (0)*self._scaling[0],
                (-self._unit_w[1]*u-self.i_border[1])*self._scaling[1]
            ])

        self._draw_plane_indicies = (0, 12)
        self._draw_line_indicies = (12, 4+self._unit_count[0]*2+self._unit_count[1]*2)

        verticies = numpy.array(verticies, dtype=numpy.float32)
        colors = numpy.array(colors, dtype=numpy.float32)
        glBindVertexArray(self.vao_id)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_id[0])
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(verticies), verticies, GL_STATIC_DRAW)
        glVertexAttribPointer(self.shaders[self.SHADER_PLANE].attributeLocation('vertex_position'), 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_id[1])
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(colors), colors, GL_STATIC_DRAW)
        glVertexAttribPointer(self.shaders[self.SHADER_PLANE].attributeLocation('vertex_color'), 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glBindVertexArray(0)

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
        # translation
        #
        #  |<------------------ o_wh[0] ---------------->|
        #  |
        #  |
        #  |          |<------- o_wh[0]*scaling[0] ----->|
        #  |<- b[0] ->|                                |
        #  |          | as[0]: x-axis in data space    |
        #  |          |======== X =====================|   <- X-AXIS
        # main        innner    origin[0]
        # border      border
        #
        tx = self.i_border[0]+self.o_wh[1]*self.i_origin[0]/self.i_axis[0]*self._scaling[0]
        # y translation need to to everything inverted since
        # the origin start at origin[1]-wh[1]
        ty = -self.i_border[1]-(self.o_wh[1]-self.o_wh[1]*self.i_origin[1]/self.i_axis[1])*self._scaling[1]

        # scaling
        sx = self.o_wh[0]*self._scaling[0]/self.i_axis[0]
        sy = self.o_wh[1]*self._scaling[1]/self.i_axis[1]

        # transaltion and scaling matrix of the plot plane
        self._mat_plot = numpy.array([
            sx, 0,  0, 0,
            0, sy,  0, 0,
            0, 0,   1, 0,
            tx, ty, 0, 1
        ], dtype=numpy.float32)


    def prepare_data(self):
        """
        prepares the data rendering
        """
        if not self._prepare_data: return

        # create gl buffer with data
        self.data_vao = glGenVertexArrays(1)
        self.data_vbo = glGenBuffers(2)

        verticies = numpy.array(self._data, dtype=numpy.float32)
        glBindVertexArray(self.data_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.data_vbo[0])
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(verticies), verticies, GL_STATIC_DRAW)
        glVertexAttribPointer(self.shaders[self.SHADER_POINTS].attributeLocation('vertex_position'), 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        # set state
        self._data_len = len(self._data)/2
        self._data = None
        self._prepare_data = False

    def render(self, mat_modelview=None):
        self.prepare_data()
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        if mat_modelview is None:
            mat_modelview = numpy.identity(4)

        # draw plane
        self.shaders[self.SHADER_PLANE].useProgram()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glUniformMatrix4fv(self._uniforms['mat_plane'], 1, GL_FALSE, self._mat_plane)
        glUniformMatrix4fv(self._uniforms['mat_modelview'], 1, GL_FALSE, mat_modelview)
        glBindVertexArray(self.vao_id)
        glDrawArrays(GL_TRIANGLES,*self._draw_plane_indicies)
        glDrawArrays(GL_LINES,*self._draw_line_indicies)
        glBindVertexArray(0)
        self.shaders[self.SHADER_PLANE].unuseProgram()

        # draw plot
        self.shaders[self.SHADER_POINTS].useProgram()
        glUniformMatrix4fv(self._uniforms['point_mat_plane'], 1, GL_FALSE, self._mat_plot)
        glUniformMatrix4fv(self._uniforms['point_mat_modelview'], 1, GL_FALSE, mat_modelview)
        glBindVertexArray(self.data_vao)
        glDrawArrays(0, 0, self._data_len)
        glBindVertexArray(0)
        self.shaders[self.SHADER_POINTS].unuseProgram()

        # draw fonts
        for text in self._fonts:
            self._gl_font.set_text(text[0], text[1], text[2])
            self._gl_font.render(mat_projection=mat_modelview)

#  ----- OPEN GL SHADERS ------------------------

VERTEX_SHADER = """
/**
 * simple shader performs transformation matricies
 * on verticies and passes vertex_color to fragment_shader
 */
#version 410
in vec2 vertex_position;
in vec4 vertex_color;
out vec4 fragment_color;
uniform mat4 mat_plane;
uniform mat4 mat_modelview;
void main() {
    fragment_color = vertex_color;
    gl_Position = mat_modelview*mat_plane*vec4(vertex_position, 0.0, 1.0);
}
"""
POINT_VERTEX_SHADER = """
/**
 * renders a given vertex and
 * passes geometry_color to geometry shader
 * XXX variable geometry_color
 */
#version 410
in vec2 vertex_position;
out vec4 geometry_color;

uniform mat4 mat_plane;
uniform mat4 mat_modelview;
void main() {
    geometry_color = vec4(0.0, .6, 0.0, 1.0);
    gl_Position = mat_modelview*mat_plane*vec4(vertex_position, 0.0, 1.0);
}
"""
FRAGMENT_SHADER = """
/**
 * renders a simple fragment by assigning
 * given input fragment_color to output_color
 */
#version 410
in vec4 fragment_color;
out vec4 output_color;
void main()
{
    output_color = fragment_color;
}
"""
GEOMETRY_SHADER = """
/**
 * renders a square around a given gl_Position.
 * also it passes the geometry_color[1] as fragment_color
 * to the fragment shader
 */
#version 410
layout (points) in;
layout (triangle_strip) out;
layout (max_vertices = 4) out;
in vec4 geometry_color[1];
out vec4 fragment_color;

uniform float dot_size;
void main(void)
{
    fragment_color = geometry_color[0];
    gl_Position = gl_in[0].gl_Position + vec4(-0.002,-0.002, 0, 0) ;
    EmitVertex();

    fragment_color = geometry_color[0];
    gl_Position = gl_in[0].gl_Position + vec4(-0.002,0.002, 0,0) ;
    EmitVertex();

    fragment_color = geometry_color[0];
    gl_Position = gl_in[0].gl_Position + vec4(0.002,-0.002, 0,0) ;
    EmitVertex();

    fragment_color = geometry_color[0];
    gl_Position = gl_in[0].gl_Position + vec4(0.002,0.002, 0,0) ;
    EmitVertex();

    EndPrimitive();
}
"""
