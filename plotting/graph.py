#-*- coding: utf-8 -*-
"""
graph rendering classes.
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
from mygl import util
from OpenGL.GL import *
import os, numpy
from time import time
from mygl.objects import geometry
from mygl.matricies import *

SHADER_DIR = os.path.dirname(os.path.abspath(__file__))+'/plot2d'
class BaseGraph():
    def space_translation(self, axis, origin):
        d_transform = self.domain.transformation_matrix(axis, origin)
        if d_transform is None:
            d_transform = matrix_identity(3)
        self.shader.uniform('mat_domain', d_transform)

class Discrete2d(BaseGraph):
    """
    Renders descrete points from a given domain.
    The vertex shader takes a kernel function to modify
    the xy and fragment information during rendering.
    """
    IDENTITY_KERNEL = 'vec4 f(vec4 x){return vec4(x.xy, 1, 1);}'
    MAT_MODELVIEW = numpy.array([
        2.0, 0,   0, 0,
        0,   2.0, 0, 0,
        0,   0,   1, 0,
        -1, -1,   0, 1
    ], dtype=numpy.float32)

    def __init__(self, domain, kernel=None):
        """ takes a domain and an optional kernel function """
        self.kernel = kernel
        self.domain = domain
        self.vao    = None

        # create vertex shader source
        vertex_shader_kernel = open(SHADER_DIR+'/data.vert.glsl').read()
        if self.kernel is not None:
            vertex_shader_kernel = vertex_shader_kernel.replace(
                self.IDENTITY_KERNEL,
                self.kernel)

        # graph shader
        self.shader = util.Shader(
            vertex=vertex_shader_kernel,
            geometry=open(SHADER_DIR+'/data.geom.glsl').read(),
            fragment=open(SHADER_DIR+'/data.frag.glsl').read(),
            link=True
        )

        dot_size = 0.01
        if hasattr(domain, 'get_dot_size'):
            dot_size = domain.get_dot_size_xy()

        # configure default uniform values
        self.shader.uniform('color_min', [0,0,0,1])
        self.shader.uniform('color_max', [.0,.0,.0,1])
        self.shader.uniform('dot_size_x', dot_size[0])
        self.shader.uniform('dot_size_y', dot_size[1])
        self.shader.uniform('mat_modelview', Discrete2d.MAT_MODELVIEW) # default matrix
        self.shader.uniform('dot_size', dot_size)

    def get_vao(self):
        """
        initializes vao
        """
        if self.vao is None:
            start_time = time()
            print('creating vao ...')
            self.vao = util.VAO()
            with self.domain.get_vbo():
                vertex_position = self.shader.attributeLocation('vertex_position')
                with self.vao:
                    glVertexAttribPointer(vertex_position, self.domain.get_dimension(), GL_FLOAT, GL_FALSE, 0, None)
                    glEnableVertexAttribArray(0)
            time_took = time() - start_time
            print('done. took {:.02f}s'.format(time_took))
        return self.vao

    def set_colors(self, color_min=[0,0,0,1], color_max=[0,0,0,1]):
        """ sets dot base color """
        self.shader.uniform('color_min', color_min)
        self.shader.uniform('color_max', color_max)

    def set_dotsize(self, dotsize):
        """ sets dot size """
        self.shader.uniform('dot_size', dotsize)

    def render(self, mat_modelview=None):
        """ renders the graph """
        self.domain.pre_render()

        if mat_modelview is not None:
            self.shader.uniform('mat_modelview', mat_modelview)

        with self.shader:
            with self.get_vao():
                glDrawArrays(GL_POINTS, 0, self.domain.length)

class Line2d(BaseGraph):
    """
    Renders descrete points from a given domain.
    The vertex shader takes a kernel function to modify
    the xy and fragment information during rendering.
    """
    IDENTITY_KERNEL = 'vec4 f(vec4 x){return vec4(x.xy, 1, 1);}'
    MAT_MODELVIEW = numpy.array([
        2.0, 0,   0, 0,
        0,   2.0, 0, 0,
        0,   0,   1, 0,
        -1, -1,   0, 1
    ], dtype=numpy.float32)

    def __init__(self, domain, kernel=None, mode=GL_LINE_STRIP):
        """ takes a domain and an optional kernel function """
        self.kernel = kernel
        self.domain = domain
        self.vao    = None
        self.mode   = mode

        # create vertex shader source
        vertex_shader_kernel = open(SHADER_DIR+'/line.vert.glsl').read()
        if self.kernel is not None:
            vertex_shader_kernel = vertex_shader_kernel.replace(
                self.IDENTITY_KERNEL,
                self.kernel)

        # graph shader
        self.shader = util.Shader(
            vertex=vertex_shader_kernel,
            fragment=open(SHADER_DIR+'/line.frag.glsl').read(),
            link=True
        )

        dot_size = 0.01
        if hasattr(domain, 'get_dot_size'):
            dot_size = domain.get_dot_size()

        # configure default uniform values
        self.shader.uniform('color_min', [0,0,0,1])
        self.shader.uniform('color_max', [.0,.0,.0,1])
        self.shader.uniform('dot_size', dot_size)
        self.shader.uniform('mat_modelview', Discrete2d.MAT_MODELVIEW) # default matrix

    def get_vao(self):
        """
        initializes vao
        """
        if self.vao is None:
            start_time = time()
            print('creating vao ...')
            self.vao = util.VAO()
            with self.domain.get_vbo():
                vertex_position = self.shader.attributeLocation('vertex_position')
                with self.vao:
                    glVertexAttribPointer(vertex_position, self.domain.get_dimension(), GL_FLOAT, GL_FALSE, 0, None)
                    glEnableVertexAttribArray(0)
            time_took = time() - start_time
            print('done. took {:.02f}s'.format(time_took))
        return self.vao

    def set_colors(self, color_min=[0,0,0,1], color_max=[0,0,0,1]):
        """ sets dot base color """
        self.shader.uniform('color_min', color_min)
        self.shader.uniform('color_max', color_max)

    def set_dotsize(self, dotsize):
        """ sets dot size """
        self.shader.uniform('dot_size', dotsize)

    def render(self, mat_modelview=None):
        """ renders the graph """
        self.domain.pre_render()
        
        if mat_modelview is not None:
            self.shader.uniform('mat_modelview', mat_modelview)
        odl_line_width = glGetFloatv(GL_LINE_WIDTH)
        glEnable(GL_LINE_SMOOTH)


        #glLineWidth(0.3)
        with self.shader:
            with self.get_vao():
                glDrawArrays(self.mode, 0, self.domain.length)

class Field2d(BaseGraph):
    """
    Renders descrete points from a given domain.
    The vertex shader takes a kernel function to modify
    the xy and fragment information during rendering.
    """
    IDENTITY_KERNEL = 'vec4 f(vec2 pc) { return vec4(0, 0, 0, 1); }'
    def __init__(self, kernel=None):
        """ takes a domain and an optional kernel function """
        self.kernel = kernel

        # create vertex shader source
        fragment_shader = open(SHADER_DIR+'/field.frag.glsl').read();
        if self.kernel is not None:
            fragment_shader = fragment_shader.replace(self.IDENTITY_KERNEL, self.kernel)
        self.shader = util.Shader(
            vertex=open(SHADER_DIR+'/field.vert.glsl').read(),
            fragment=fragment_shader,
            link=True
        )
        identity = matrix_identity(4)
        self.shader.uniform('mat_projection', identity)
        self.shader.uniform('mat_modelview', translation_matrix(-1.0, 1.0))

        self._rectangle = geometry.Rectangle(2.0,2.0)
        self._rectangle.link_attr_position(self.shader)

    def space_translation(self, axis, origin):
        """ sets shader to transform fragment coords into plane coords """
        self.shader.uniform('mat_domain', numpy.array([
            axis[0]*0.5, 0,   0,
            0,   axis[1]*0.5, 0,
            -origin[0]+axis[0]*0.5, -origin[1]+axis[1]*0.5,   1.0,
        ], dtype=numpy.float32))

    def render(self, mat_modelview=None):
        """ renders the graph """
        with self.shader: self._rectangle.render()


class Graph3d(BaseGraph):
    """
    Renders descrete points from a given domain.
    The vertex shader takes a kernel function to modify
    the xy and fragment information during rendering.
    """
    IDENTITY_KERNEL = 'vec4 f(vec4 x){return vec4(x.xyz, 1);}'
    MAT_MODELVIEW = numpy.array([
        2.0, 0,   0, 0,
        0,   2.0, 0, 0,
        0,   0,   2.0, 0,
        -1, -1,   -1, 1
    ], dtype=numpy.float32)

    def __init__(self, domain, kernel=None, mode=GL_POINTS):
        """ takes a domain and an optional kernel function """
        self.kernel = kernel
        self.domain = domain
        self.vao    = None
        self.mode   = mode

        # create vertex shader source
        vertex_shader_kernel = open(SHADER_DIR+'/line3d.vert.glsl').read()
        if self.kernel is not None:
            vertex_shader_kernel = vertex_shader_kernel.replace(
                self.IDENTITY_KERNEL,
                self.kernel)

        # graph shader
        self.shader = util.Shader(
            vertex=vertex_shader_kernel,
            fragment=open(SHADER_DIR+'/line3d.frag.glsl').read(),
            link=True
        )

        dot_size = 0.01
        if hasattr(domain, 'get_dot_size'):
            dot_size = domain.get_dot_size()

        # configure default uniform values
        self.shader.uniform('color_min', [0,0,0,1])
        self.shader.uniform('color_max', [.0,.0,.0,1])
        self.shader.uniform('dot_size', dot_size)
        self.shader.uniform('mat_modelview', Discrete2d.MAT_MODELVIEW) # default matrix

    def set_mat_projection(self, mat_projection):
        self.shader.uniform('mat_projection', mat_projection) # default matrix

    def get_vao(self):
        """
        initializes vao
        """
        if self.vao is None:
            start_time = time()
            print('creating vao ...')
            self.vao = util.VAO()
            with self.domain.get_vbo():
                vertex_position = self.shader.attributeLocation('vertex_position')
                with self.vao:
                    glVertexAttribPointer(vertex_position, self.domain.get_dimension(), GL_FLOAT, GL_FALSE, 0, None)
                    glEnableVertexAttribArray(0)
            time_took = time() - start_time
            print('done. took {:.02f}s'.format(time_took))
        return self.vao

    def set_colors(self, color_min=[0,0,0,1], color_max=[0,0,0,1]):
        """ sets dot base color """
        self.shader.uniform('color_min', color_min)
        self.shader.uniform('color_max', color_max)

    def render(self, mat_modelview=None):
        """ renders the graph """
        self.domain.pre_render()
        
        if mat_modelview is not None:
            self.shader.uniform('mat_modelview', mat_modelview)

        glEnable(GL_LINE_SMOOTH)
        with self.shader:
            with self.get_vao():
                glDrawArrays(self.mode, 0, self.domain.length)
