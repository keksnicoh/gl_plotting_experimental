#-*- coding: utf-8 -*-
"""
some simple objects to reuse
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""

from mygl.util import VBO, VAO
from OpenGL.GL import *
import numpy
class Object():

    def link_attr_position(self, shader, location='vertex_position'):
        with self._vao:
            with self._vbo.get(0):
                glVertexAttribPointer(shader.attributeLocation(location), 3, GL_FLOAT, GL_FALSE, 0, None)
                glEnableVertexAttribArray(0)

    def link_attr_texcoord(self, shader, location='vertex_texcoord'):
        with self._vao:
            with self._vbo.get(1):
                glVertexAttribPointer(shader.attributeLocation(location), 2, GL_FLOAT, GL_FALSE, 0, None)
                glEnableVertexAttribArray(1)

class Rectangle(Object):
    def __init__(self, w, h):
        self._w = w
        self._h = h

        vertex_position = numpy.array([
            0, 0, 0,
            0, -h, 0,
            w, -h, 0,
            w, -h, 0,
            w, 0, 0,
            0, 0, 0,
        ], dtype=numpy.float32)

        vertex_texcoord = numpy.array([
            0, 1,
            0, 0,
            1, 0,
            1, 0,
            1, 1,
            0, 1
        ], dtype=numpy.float32)

        self._vao = VAO()
        self._vbo = VBO(2)

        with self._vao:
            with self._vbo.get(0):
                glBufferData(
                    GL_ARRAY_BUFFER,
                    ArrayDatatype.arrayByteCount(vertex_position),
                    vertex_position,
                    GL_STATIC_DRAW)

            with self._vbo.get(1):
                glBufferData(
                    GL_ARRAY_BUFFER,
                    ArrayDatatype.arrayByteCount(vertex_texcoord),
                    vertex_texcoord,
                    GL_STATIC_DRAW)

    def render(self):
        with self._vao:
            glDrawArrays(GL_TRIANGLES, 0, 6)


