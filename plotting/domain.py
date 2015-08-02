#-*- coding: utf-8 -*-
"""
graph rendering classes.
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""

from mygl.util import *
from OpenGL.GL import *
import numpy
import math
import random

from opencl.cl_handler import BaseCalculator

class Domain():
    """
    a domain specifies the x,y values for each plotting point.
    basically a domain provides a vbo so the plotter can create
    a vao to render the points.
    """
    def __init__(self, length):
        """ init """
        self.vbo = None
        self.length = length

    def init_vbo(self, length):
        """ initializes vbo by given length """
        if self.vbo:
            raise RuntimeWarning("VBO already initializesed. better use get_vbo()")
        else:
            self.vbo = VBO()
            with self.vbo:
                glBufferData(GL_ARRAY_BUFFER, length*8, None, GL_STATIC_DRAW)
                self.length = length

    def push_data(self, data):
        """ pushes data into vbo """
        data = numpy.array(data, dtype=numpy.float32)
        byte_count = min(ArrayDatatype.arrayByteCount(data), self.length*8)
        self.get_vbo().get(0).glBufferSubData(0, byte_count, data)

    def get_vbo(self):
        """
        returns a mygl.util.VBO instance
        """
        if self.vbo is None:
            self.init_vbo(self.length)
        return self.vbo

    def transformation_matrix(self, axis, origin):
        """
        returns a 3x3 transformation/scaling matrix
        for the domain. if return value is None, the
        plotter should interpret this as identity matrix.
        """
        return None

    def get_dimension(self):
        """
        returns standard dimension 2 for
        """
        return 2

class Axis(Domain):
    """
    x-axis domain
    """
    def init_vbo(self, length):
        """ initializes vbo by given length """
        Domain.init_vbo(self, length)

        data = numpy.zeros(length*2)
        for x in range(0, length):
            data[2*x] = (float(x)/length)
            data[2*x+1] = 0.0

        self.push_data(data)

    def get_dot_size(self): return max(0.002, 1.0/self.length)
    def transformation_matrix(self, axis, origin):
        return numpy.array([
            axis[0], 0,   0,
            0, 0, 0,
            -origin[0], 0,   1.0,
        ], dtype=numpy.float32)

class Series(Domain):
    """
    series domain domain
    """
    def init_vbo(self, length):
        """ initializes vbo by given length """
        Domain.init_vbo(self, length)

        data = numpy.zeros(length*2)
        for x in range(0, length):
            data[2*x] = x
            data[2*x+1] = 0.0
        self.push_data(data)

    def get_dot_size(self): return max(0.002, 1.0/self.length)
    def transformation_matrix(self, axis, origin):
        return numpy.array([
            max(1, float(axis[0])/float(self.length)), 0,   0,
            0, 0, 0,
            -origin[0], 0,   1.0,
        ], dtype=numpy.float32)



class AxisGL(Domain):
    """
        Domain that only returns gl_buffer to be modified somewhere else
    """
    def __init__(self, length, calculator):
        Domain.__init__(self, length)
        vbo = self.get_vbo()
        self.buffer = calculator.getOpenGLBufferFromId(vbo.get(0).id)


class DuffingDomain(Domain):
    def __init__(self, kernel, length, time, lambd, epsilon, omega, beta, initial_conditions):
        Domain.__init__(self, length)
        self.kernel = kernel
        self.time = numpy.int32(time)
        self.lambd = numpy.float32(lambd)
        self.epsilon = numpy.float32(epsilon)
        self.omega = numpy.float32(omega)
        self.beta = numpy.float32(beta)
        self.initial_conditions = initial_conditions

    def init_vbo(self, length):
        Domain.init_vbo(self, length)

        calculator = BaseCalculator(sharedGlContext=True)
        awp = calculator.create2ComponentVektor(self.initial_conditions)

        gl_buffer = calculator.getOpenGLBufferFromId(self.vbo.get(0).id)

        calculator.calculateGL(self.kernel, [awp, numpy.int32(length), self.time, self.lambd, self.beta, self.omega, self.epsilon], [gl_buffer], (1,))

    def get_dot_size(self): return max(0.002, 1.0/self.length)

        

class Cartesian(Domain):
    def __init__(self, length, min_y=0.0, max_y=1.0, min_x=0.0, max_x=1.0):
        Domain.__init__(self, length)
        self.min_y = min_y
        self.max_y = max_y
        self.min_x = min_x
        self.max_x = max_x

    """
    cartesian space
    """
    def init_vbo(self, length, min_y=0.0, max_y=0.0, min_x=0.0, max_x=1.0):
        """ initializes vbo by given length """
        Domain.init_vbo(self, length*length)

        # fill data
        shift_x = 1.0/(2*length)
        shift_y = 1.0/(2*length)
        data = numpy.zeros(length*length*2)

        delta_x = self.max_x - self.min_x
        delta_y = self.max_y - self.min_y
        for x in range(0, length):
            for y in range(0, length):
                data[2*length*x+2*y] = delta_x*(float(x)/length + shift_x) + self.min_x
                data[2*length*x+2*y+1] = delta_y*(float(y)/length + shift_y) + self.min_y

        self.push_data(data)

    def get_dot_size(self): return 1.0/self.length

    def transformation_matrix(self, axis, origin):
        """
        default transformation does transform x and y coordinates into
        the current axis/origin configuration
        """
        return numpy.array([
            axis[0], 0,   0,
            0,   axis[1], 0,
            -origin[0], -origin[1],   1.0,
        ], dtype=numpy.float32)

    def fixed_x_transformation(self, axis, origin):
        """
        transformation to fix x axis
        """
        return numpy.array([
            1, 0, 0,
            0, axis[1], 0,
            0, -origin[1], 1,
        ], dtype=numpy.float32)

    def fixed_y_transformation(self, axis, origin):
        """
        transformation to fix y axis
        """
        return numpy.array([
            axis[0], 0, 0,
            0, 1, 0,
            -origin[0], 0, 1,
        ], dtype=numpy.float32)


class RandomCartesian(Cartesian):
    """docstring for RandomCartesian"""
    def __init__(self, length, min_y=0.0, max_y=1.0, min_x=0.0, max_x=1.0, randomPosition=False):
        Cartesian.__init__(self, length, min_y, max_y, min_x, max_x)
        self.randomPosition = randomPosition

    def get_dimension(self):
        return 3

    def get_random_array(self, length):
        return np.random.rand(length,1)

        #random.randint(0, length)
    def init_vbo(self, length, min_y=0.0, max_y=0.0, min_x=0.0, max_x=1.0):
        """ initializes vbo by given length """
        Domain.init_vbo(self, length*length*length)

        # fill data
        shift_x = 1.0/(2*length)
        shift_y = 1.0/(2*length)
        data = numpy.zeros(length*length*length*2)

        delta_x = self.max_x - self.min_x
        delta_y = self.max_y - self.min_y
        for x in range(0, length):
            for y in range(0, length):
                data[3*length*x+3*y] = delta_x*(float(x)/length + shift_x) + self.min_x
                if self.randomPosition:
                    y = random.randint(0, length)
                data[3*length*x+3*y+1] = delta_y*(float(y)/length + shift_y) + self.min_y
                data[3*length*x+3*y+2] = int(random.randint(0, 1))

        self.push_data(data)
