#-*- coding: utf-8 -*-
"""
@author Nicolas 'keksnicoh' Heimann <nicolas.heimann@googlemail.com>
"""

from mygl.app import BasicGl
from mygl.fps import GlFPS
from mygl.util import Shader
from mygl.matricies import *
from OpenGL.GL import *
import numpy
import ImageFont, os
FONT_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))+'/../resources/fonts'

VERTEX_SHADER = """
#version 410
in vec2 vert;
in vec2 vertTexCoord;
uniform mat4 mat_projection;
out vec2 fragTexCoord;
void main() {
    fragTexCoord = vertTexCoord;
    gl_Position = mat_projection * vec4(vert, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 410
out vec4 finalColor;
in vec2 fragTexCoord;
uniform vec4 color_bg;
uniform vec2 origin;
uniform vec4 color_axis;
uniform float axis_width;
uniform vec4 grid_color;
uniform float grid_width;
uniform vec2 unit_count;

void main() {
/*
    if (abs(fragTexCoord.x-origin.x) <= axis_width) {
        finalColor = color_axis;
        return;
    }
    if (1-abs(fragTexCoord.y-origin.y) <= axis_width) {
        finalColor = color_axis;
        return;
    }*/
    if (pow(mod(fragTexCoord.x,unit_count.x),3) <= grid_width) {
        finalColor = grid_color;
        return;
    }
    //if (abs(mod(fragTexCoord.y, unit_count.y)) <= grid_width) {
    //    finalColor = grid_color;
    //    return;
    //}

    finalColor = color_bg;

}
"""

class glPlottingPlane2D():

    def __init__(self):
        self._is_prepared = False

    def prepare(self):
        shader = Shader()
        shader.attachShader(GL_VERTEX_SHADER, VERTEX_SHADER)
        shader.attachShader(GL_FRAGMENT_SHADER, FRAGMENT_SHADER)
        shader.linkProgram()
        self.shader = shader

        self.vao_id = glGenVertexArrays(1)
        self.vbo_id = glGenBuffers(2)

        vertex_data = numpy.array([
            0,              0,              #1 #left triangle
            0,              -1, #2
            1, -1, #3
            1, -1, #4 #right triangle
            1, 0,              #5
            0, 0                            #6
        ], dtype=numpy.float32)

        text_coord_data = numpy.array([
            0,0,   0,25,   25,25,
            25,25,   25,0,   0,0,
        ], dtype=numpy.float32)

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
        self._is_prepared = True

    def render(self, mat_projection=None):
        if not self._is_prepared:
            self.prepare()
        mat_projection = mat_projection if mat_projection is not None else numpy.identity(4)

        self.shader.useProgram()
        unit_count = (7,7)
        origin = (0.0, 0.0)
        glUniformMatrix4fv(self._uloc('mat_projection'), 1, GL_FALSE, mat_projection)
        glUniform4f(self._uloc('color_bg'), *[0.0, 0.0, 0.0, 0.0])
        glUniform4f(self._uloc('color_axis'), *[0.4, 0.0, 1.0, 0.0])
        glUniform1f(self._uloc('axis_width'), 0.001)
        glUniform4f(self._uloc('grid_color'), 0.0, 1.0, 0.0, 0.0)
        glUniform1f(self._uloc('grid_width'), 0.0001)
        glUniform2f(self._uloc('origin'), *origin)
        glUniform2f(self._uloc('unit_count'), *unit_count)
        glBindVertexArray(self.vao_id)
        glDrawArrays(GL_TRIANGLES, 0, 6)


        glBindVertexArray(0)
        self.shader.unuseProgram()

    def _uloc(self, name):
        return self.shader.uniformLocation(name)

if __name__ == '__main__':
    app = BasicGl()
    plane = glPlottingPlane2D()
    plane.prepare()
    while app.active():
        app.init_cycle()
        plane.render(mat_projection=translation_matrix(-.5, .5))
        app.swap()


