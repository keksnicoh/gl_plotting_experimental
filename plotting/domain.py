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
        self.calculator = None

    def init_vbo(self, length):
        """ initializes vbo by given length """
        if self.vbo:
            raise RuntimeWarning("VBO already initializesed. better use get_vbo()")
        else:
            self.vbo = VBO()
            with self.vbo:
                glBufferData(GL_ARRAY_BUFFER, length*4*self.get_dimension(), None, GL_STATIC_DRAW)
                self.length = length

    def push_data(self, data):
        """ pushes data into vbo """
        data = numpy.array(data, dtype=numpy.float32)
        byte_count = min(ArrayDatatype.arrayByteCount(data), self.length*4*self.get_dimension())
        self.get_vbo().get(0).glBufferSubData(0, byte_count, data)

    def get_vbo(self):
        """
        returns a mygl.util.VBO instance
        """
        if self.vbo is None:
            self.init_vbo(self.length)
        return self.vbo

    def pre_render(self):
        """
        gets invoked before a graph is rendered
        """
        pass

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

    def getDomainBuffer(self):
        """
        returns opengl buffer to be modiefied elsewhere
        """
        if not self.calculator:
            self.calculator = BaseCalculator(sharedGlContext=True)
        return self.calculator.getOpenGLBufferFromId(self.vbo.get(0).id)

class Axis(Domain):
    """
    x-axis domain
    """
    def __init__(self, length, dot_size=0.002):
        """ init """
        Domain.__init__(self, length)
        self.dot_size = dot_size

    def init_vbo(self, length):
        """ initializes vbo by given length """
        Domain.init_vbo(self, length)

        data = numpy.zeros(length*2)
        for x in range(0, length):
            data[2*x] = (float(x)/(length-1))
            data[2*x+1] = 0.0

        self.push_data(data)

    def get_dot_size(self): return max(self.dot_size, 1.0/self.length)
    def transformation_matrix(self, axis, origin):
        return numpy.array([
            axis[0], 0,   0,
            0, 0, 0,
            -origin[0], 0,   1.0,
        ], dtype=numpy.float32)

class Logistic(Domain):
    def __init__(self, length, x_0, r):
        Domain.__init__(self, length)
        self.x_0 = x_0
        self.r = r
        self.gl_buffer = None

    def updateParameterR(self, value, kernel):
        if not self.gl_buffer:
            self.gl_buffer = self.getDomainBuffer()
        self.calculator.calculateGL(kernel, [numpy.int32(self.length), numpy.float32(value)], [self.gl_buffer], (1,))

    def _logFunction(self, x):
        return self.r*x*(1-x)

    def init_vbo(self, length):
        Domain.init_vbo(self, length)

        data = numpy.zeros(length*2)
        
        data[0] = self.x_0
        data[1] = self._logFunction(self.x_0)
        for i in range(1, length):
            data[2*i] = data[2*(i-1)+1]
            data[2*i+1] = self._logFunction(data[2*i])

        self.push_data(data)

    def get_dot_size(self): return max(0.005, 1.0/self.length)
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


class CLDomain(Domain):
    def __init__(self, kernel, gl_buffer_length, cl_params, dimension=2):
        Domain.__init__(self, gl_buffer_length)
        self.kernel = kernel
        self.dimension = dimension
        self.cl_params = cl_params

    def get_dimension(self):
        return self.dimension

    def init_vbo(self, length):
        Domain.init_vbo(self, length)
        self.calculator = BaseCalculator(sharedGlContext=True)
        self.gl_buffer = self.calculator.getOpenGLBufferFromId(self.get_vbo().get(0).id)
        self.calculate_cl_buffer()

    def calculate_cl_buffer(self, param=None, value=None):
        if param == 'V_s':
            print "V_s:", value
            self.cl_params[6] = numpy.float32(value)
        if param == 'it_offset':
            self.cl_params[1] = numpy.int32(value)
        if param == 'iterations':
            self.cl_params[0] = numpy.int32(value)

        self.calculator.calculateGL(self.kernel, self.cl_params, [self.gl_buffer], (1,))


class DuffingDomain(Domain):
    def __init__(self, kernel, length, time, lambd, epsilon, omega, beta, initial_conditions, start_iteration):
        Domain.__init__(self, length)
        self.kernel = kernel
        self.time = numpy.int32(time)
        self.lambd = numpy.float32(lambd)
        self.epsilon = numpy.float32(epsilon)
        self.omega = numpy.float32(omega)
        self.beta = numpy.float32(beta)
        self.initial_conditions = initial_conditions
        self.start_iteration = numpy.int32(start_iteration)
        self.dimension = 2

    def get_dimension(self):
        return self.dimension

    def updateParameter(self, param, value, kernel):
        if not self.gl_buffer:
            self.gl_buffer = self.getDomainBuffer()

        if param == 'x_0':
            self.initial_conditions = (value, self.initial_conditions[1])
        elif param == 'y_0':
            self.initial_conditions = (self.initial_conditions[0], value)
        elif param == 's':
            self.start_iteration = numpy.int32(value)
        elif param == 't':
            self.time = numpy.int32(value)
        else:
            return

        awp = self.calculator.create2ComponentVektor(self.initial_conditions)
        self.calculator.calculateGL(self.kernel, [awp, numpy.int32(self.length), self.time, self.lambd, self.beta, self.omega, self.epsilon, self.start_iteration], [self.gl_buffer], (1,))


    def init_vbo(self, length):
        Domain.init_vbo(self, length)

        self.calculator = BaseCalculator(sharedGlContext=True)
        self.gl_buffer = self.calculator.getOpenGLBufferFromId(self.get_vbo().get(0).id)

        awp = self.calculator.create2ComponentVektor(self.initial_conditions)

        self.calculator.calculateGL(self.kernel, [awp, numpy.int32(length), self.time, self.lambd, self.beta, self.omega, self.epsilon, self.start_iteration], [self.gl_buffer], (1,))

    def get_dot_size(self): return max(0.002, 1.0/self.length)

        

class Cartesian(Domain):
    def __init__(self, length, min_y=0.0, max_y=1.0, min_x=0.0, max_x=1.0, dimension=2):
        Domain.__init__(self, length)
        self.min_y = min_y
        self.max_y = max_y
        self.min_x = min_x
        self.max_x = max_x
        self.dimension = dimension

    def get_dimension(self):
        return self.dimension

    """
    cartesian space
    """
    def init_vbo(self, length, min_y=0.0, max_y=0.0, min_x=0.0, max_x=1.0):
        """ initializes vbo by given length """
        Domain.init_vbo(self, length*length)

        # fill data
        shift_x = 1.0/(2*length)
        shift_y = 1.0/(2*length)
        data = numpy.zeros(length*length*self.dimension)

        delta_x = self.max_x - self.min_x
        delta_y = self.max_y - self.min_y
        for x in range(0, length):
            for y in range(0, length):
                data[self.dimension*length*x+self.dimension*y] = delta_x*(float(x)/length + shift_x) + self.min_x
                data[self.dimension*length*x+self.dimension*y+1] = delta_y*(float(y)/length + shift_y) + self.min_y
                if self.dimension == 3:
                    data[self.dimension*length+self.dimension*y+2] = 0.0

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

class PythonCodeDomain(Domain):

    def __init__(self, length):
        Domain.__init__(self, length)
        self.recalculate_on_prerender = True
        self._is_calculated = False
    def calculata_domain(): return numpy.zeros(2)

    def pre_render(self):
        """
        gets invoked before a graph is rendered
        """
        if not self._is_calculated or self.recalculate_on_prerender:
            data = self.calculata_domain()
            self.push_data(data)
            self._is_calculated = True
