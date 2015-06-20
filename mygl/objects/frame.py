#-*- coding: utf-8 -*-
"""
frame buffer classes
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""

from mygl.matricies import *
from mygl.objects import geometry
from mygl.util import *
from OpenGL.GL import *

class Window():
    """
    window provides a very easy usage of framebuffers.
    it captures all rendered stuff to a color and a
    depth texture and renders it to a rectangular plane.

    XXX check alpha behavior
    """
    def __init__(self, size=(1,1), resolution=(512, 512), color=[0,0,0,1], shader=None):
        """
        .size is the size of the rectangular screen plane
        .resulution inside the window (must be power of 2)
        .color background color of the window
        .shader custom shader to render window
        """
        if shader is None: shader = self.create_default_shader()
        self.resolution = resolution
        self.size = size

        # create default shader if shader is none

        self.shader = shader
        self.shader.uniform('tex[0]', 0)
        self.shader.uniform('depth_tex', 1)
        self.shader.uniform('color', color)

        self.shader = shader
        self._rectangle = geometry.Rectangle(*self.size)
        self._rectangle.link_attr_position(self.shader)
        self._rectangle.link_attr_texcoord(self.shader)

        self._color_tex = Texture2D(self.resolution[0], self.resolution[1])
        self._depth_tex = Texture2D(self.resolution[0], self.resolution[1], GL_DEPTH_COMPONENT)
        self._framebuffer = Framebuffer(self.resolution[0], self.resolution[1], self._color_tex, self._depth_tex)

        self._old_viewport = None

    def __enter__(self): self.record()
    def __exit__(self, type, value, tb): self.stop()

    def record(self):
        """ start rendering to framebuffer """
        self._old_viewport = glGetIntegerv(GL_VIEWPORT)
        self._framebuffer.bind()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, *self.resolution)

    def stop(self):
        """ stop rendering to frame buffer """
        self._framebuffer.unbind()
        glViewport(*self._old_viewport)

    def render(self):
        """ render  window """
        glActiveTexture(GL_TEXTURE0);
        glBindTexture (GL_TEXTURE_2D, self._color_tex.gl_id())
        glActiveTexture(GL_TEXTURE1);
        glBindTexture (GL_TEXTURE_2D, self._depth_tex.gl_id())

        with self.shader:
            self._rectangle.render()

    @classmethod
    def create_default_shader(cls):
        """ creates a default shader instance """
        identity = matrix_identity(4)
        shader = Shader()
        shader.attachShader(GL_VERTEX_SHADER, VERTEX_SHADER)
        shader.attachShader(GL_FRAGMENT_SHADER, FRAGMENT_SHADER)
        shader.linkProgram()
        shader.uniform('mat_projection', identity)
        shader.uniform('mat_modelview', identity)
        return shader

VERTEX_SHADER = """
#version 410
uniform mat4 mat_projection;
uniform mat4 mat_modelview;

in vec2 vertex_position;
in vec2 vertex_texcoord;
out vec2 fragTexCoord;

void main()
{
    fragTexCoord = vertex_texcoord;
    gl_Position = mat_projection * mat_modelview * vec4(vertex_position, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 410

uniform sampler2D tex[1];
uniform sampler2D depth_tex;
uniform vec4 color;

in vec2 fragTexCoord;
out vec4 finalColor;

void main()
{
    finalColor = texture(tex[0], fragTexCoord);
    finalColor = mix(color, finalColor, .5);
    return;
}
"""
