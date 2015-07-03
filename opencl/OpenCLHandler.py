#-*- coding: utf-8 -*-
"""
OpenCL handler class
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

import pyopencl as cl
import pyopencl.array as cl_array
from pyopencl.tools import get_gl_sharing_context_properties
import numpy as np

import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

class BaseCalculator(object):
	"""docstring for BaseCalculator"""
	def __init__(self, gpuOnly=True, sharedGlContext=False):
		super(BaseCalculator, self).__init__()
		self.platform = cl.get_platforms()[0]
		self.devices = self.platform.get_devices()

		properties = None
		if sharedGlContext:
			assert cl.have_gl()
			properties = get_gl_sharing_context_properties()

		devices = self.devices
		if gpuOnly and len(self.devices) > 1:
			devices = [self.devices[0]]

		self.context = cl.Context(properties=properties, devices=devices)

		self.queue = None

	def _buildKernel(self, kernel):
		program = cl.Program(self.context, kernel).build()
		self.queue = cl.CommandQueue(self.context)
		return program

	def createArrayBuffer(self, array):
		return cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=array)

	def create2ComponentVektor(self, vec):
		if len(vec) != 2:
			raise InvalidArgument('Creating 2 component vector from list with %d elements', len(vec))

		return np.asarray(vec, dtype=cl_array.vec.float2)

	def getOpenGLBufferFromId(self, buffer_id):
		return cl.GLBuffer(self.context, cl.mem_flags.READ_WRITE, int(buffer_id))

	def calculateGL(self, kernel, clBuffers, glBuffers, outputShape):
		"""
		Writes directly to OpenGL Buffers
		"""
		program = self._buildKernel(kernel)
		buffers = clBuffers + glBuffers

		if self.queue:
			program.f(self.queue, outputShape, None, *buffers)
		else:
			print "No queue initialized"

		self.queue.finish()
		cl.enqueue_release_gl_objects(self.queue, glBuffers)


	def calculateSimple(self, kernel, buffers, outputArray):
		"""
		Handles output buffer based on given numpy array
		"""
		program = self._buildKernel(kernel)

		outputBuffer = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, outputArray.nbytes)
		buffers.append(outputBuffer)

		if self.queue:
			program.f(self.queue, outputArray.shape, None, *buffers)
		else:
			print "No queue initialized"

		cl.enqueue_copy(self.queue, outputArray, outputBuffer)

		return outputArray
