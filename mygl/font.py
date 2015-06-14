#-*- coding: utf-8 -*-
"""
font rendering utilities.
XXX optimize texture rendering...
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
import mygl.app
from mygl.util import Shader
from matricies import translation_matrix
from OpenGL.GL import *
import ImageFont
import numpy

VERTEX_SHADER = """
#version 410
in vec2 vert;
in vec2 vertTexCoord;
out vec2 fragTexCoord;
uniform mat4 mat_projection;
uniform mat4 mat_modelview;
void main() {
    fragTexCoord = vertTexCoord;
    gl_Position = mat_projection * mat_modelview * vec4(vert, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 410
uniform sampler2D tex;
in vec2 fragTexCoord;
uniform vec4 color;
out vec4 finalColor;
void main() {
    finalColor = color * texture(tex, fragTexCoord);
}
"""

class GlFont():
    NEWLINE = '\n'
    SCALING = 400.0
    def __init__(self, text, font):
        self.font = font
        self.color = [1.0, 1.0, 1.0, 1.0]
        self.shader = None
        self.length = None
        self._render_data = []
        self._texture_cache = {}
        self._prepare_gl()
        self._is_prepared = False

        """ local modelview matrix. """
        self.mat_modelview_f = lambda rel_xy, n, l: translation_matrix(*rel_xy)
        self.set_text(text)

    def set_color(self, color):
        self.color = color
    def set_text(self, text):
        self.text = text
        self._is_prepared = False

    def _prepare_gl(self):
        """
        prepares shaders and vao/vbo
        """
        # init gl
        shader = Shader()
        shader.attachShader(GL_VERTEX_SHADER, VERTEX_SHADER)
        shader.attachShader(GL_FRAGMENT_SHADER, FRAGMENT_SHADER)
        shader.linkProgram()
        self.shader = shader

        self.vao_id = glGenVertexArrays(1)
        self.vbo_id = glGenBuffers(2)

    def prepare(self):
        """
        prepares font rendering.
        this method is quiet expensive, avoid invokation as much as possible.
        """
        vertex_data     = numpy.zeros(len(self.text)*2*6, dtype=numpy.float32)
        text_coord_data = numpy.zeros(len(self.text)*2*6, dtype=numpy.float32)

        rel_xy = (0.0, 0.0)
        line_height_factor = 6.0/5.0
        self._render_data = []
        max_line_height = 0.0
        for n, char in enumerate(self.text):
            glyph = self.font.getmask(char)
            glyph_width, glyph_height = glyph.size
            glyph_offset_x, glyph_offset_y = self.font.getoffset(char)

            # calculate the next power of two.
            # this is required to define a valid texture buffer
            # size.
            width = next_p2 (glyph_width + 1)
            height = next_p2 (glyph_height + 1)

            # fragment coordinates
            frag_x = float (glyph_width) / float (width)
            frag_y = float (glyph_height) / float (height)
            frag_size = (frag_x, frag_y)

            # vertex dimensions
            vert_size = (glyph_width / self.SCALING, glyph_height / self.SCALING)
            vert_offset = (-glyph_offset_x / self.SCALING, -glyph_offset_y / self.SCALING)

            # if there is a newline, skip to next line.
            if char == GlFont.NEWLINE:
                self._render_data.append(GlFont.NEWLINE)
                rel_xy = (0.0, rel_xy[1]-max_line_height*line_height_factor)
                continue

            # vertex data. note that opengl interpret this
            # data counter clockwise...
            #    5   6
            #  1 +---+        -
            #    |\  |        |
            #    | \ |        | (offset_y - size_y)
            #    |  \|        |
            #  2 +---+ 3,4    -
            #    |   |
            #   (offset_x + size_x)
            vertex_data[n*12:(n+1)*12] = numpy.array([
                vert_offset[0],              vert_offset[1],              #1 #left triangle
                vert_offset[0],              vert_offset[1]-vert_size[1], #2
                vert_offset[0]+vert_size[0], vert_offset[1]-vert_size[1], #3
                vert_offset[0]+vert_size[0], vert_offset[1]-vert_size[1], #4 #right triangle
                vert_offset[0]+vert_size[0], vert_offset[1],              #5
                vert_offset[0],              vert_offset[1]               #6
            ], dtype=numpy.float32)

            # text coord data implies the coords in fragment shader
            # for the texture. note that this must be inverse to the
            # vertex_data since opengl vertex_data is interpreted counter
            # clockwise, and text_data is clockwise.
            text_coord_data[n*12:(n+1)*12] = numpy.array([
                0,0,                          0,frag_size[1],   frag_size[0],frag_size[1],
                frag_size[0], frag_size[1],   frag_size[0],0,   0,0,
            ], dtype=numpy.float32)

            # prepare opengl texture and append prepared data.
            ID = self._create_texture(char, glyph, width, height, glyph_width, glyph_height)

            # assign texture id and rel_xy to render_data
            self._render_data.append([ID, rel_xy])
            rel_xy = (rel_xy[0]+vert_size[0]+vert_offset[0], rel_xy[1])
            max_line_height = max(max_line_height, vert_size[1])

        # bind all data to buffers.
        # later glDrawArrays specifies which letter to draw. each letter
        # gets a texture assigned during render cycle.
        # XXX optimize me!
        glBindVertexArray(self.vao_id)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_id[0])
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertex_data), vertex_data, GL_STATIC_DRAW)
        glVertexAttribPointer(self.shader.attributeLocation('vert'), 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_id[1])
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(text_coord_data), text_coord_data, GL_STATIC_DRAW)
        glVertexAttribPointer(self.shader.attributeLocation('vertTexCoord'), 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glBindVertexArray(0)
        self._is_prepared = True

    def _create_texture(self, char, glyph, width, height, glyph_width, glyph_height):
        """
        creates an opengl 2d texture from a TTF font object.
        XXX optimize this, we only need a 2 channel i guess...
        """

        if char not in self._texture_cache:
            ID = glGenTextures (1)
            glBindTexture (GL_TEXTURE_2D, ID)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            tex2d = ""
            for j in xrange (height):
                for i in xrange (width):
                    if (i >= glyph_width) or (j >= glyph_height):
                        value = chr (0)
                        tex2d += value*4
                    else:
                        value = chr (glyph.getpixel ((i, j)))
                        tex2d += value*4

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex2d)
            self._texture_cache[char] = ID

        return self._texture_cache[char]

    def _uloc(self, name):
        return self.shader.uniformLocation(name)

    def set_render_length(self, length=None):
        self.length = length

    def render(self, mat_projection=None):
        if not self._is_prepared:
            self.prepare()
        mat_projection = mat_projection if mat_projection is not None else numpy.identity(4)
        length = len(self._render_data) if self.length is None else self.length
        char = (0.0, 0.0)

        self.shader.useProgram()
        glActiveTexture(GL_TEXTURE1) # XXX disale texture later??
        glBindVertexArray(self.vao_id)

        # NOTE: if you assign glUniform1i within the for-loop
        # you will get heavy performance issues. note that this
        # uniform assignments seem to kill your performance. try
        # to assign them as less as possible...
        glUniform1i(self._uloc('tex'), 1)
        glUniform4f(self._uloc('color'), *self.color)
        glUniformMatrix4fv(self._uloc('mat_projection'), 1, GL_FALSE, mat_projection)
        for n, data in enumerate(self._render_data[0:length]):
            # newline
            if data == GlFont.NEWLINE: char = (0, char[1]+1); continue
            (gl_tex_id, rel_xy) = data

            model_view_matrix = self.mat_modelview_f(rel_xy, *char)
            glUniformMatrix4fv(self._uloc('mat_modelview'), 1, GL_FALSE, model_view_matrix)

            glBindTexture (GL_TEXTURE_2D, gl_tex_id)
            glDrawArrays(GL_TRIANGLES, n*6, 6)
            char = (char[0]+1, char[1])

        glBindVertexArray(0)
        self.shader.unuseProgram()

def next_p2 (num):
    """ If num isn't a power of 2, will return the next higher power of two """
    rval = 1
    while rval<num:
        rval <<= 1
    return rval
