#-*- coding: utf-8 -*-
"""
OpenCL handler class
IMPORTANT: Apple CPU only supports workgroup_size = 1
Use GPU to work with workgroups
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
	def __init__(self, gpuOnly=True, sharedGlContext=False, hidePlatformDetails=False):
		super(BaseCalculator, self).__init__()
		self.platform = cl.get_platforms()[0]
		self.devices = self.platform.get_devices()

		if not hidePlatformDetails:
			for platform in cl.get_platforms():
				for device in platform.get_devices():
					print("===============================================================")
					print("Platform name:", platform.name)
					print("Platform profile:", platform.profile)
					print("Platform vendor:", platform.vendor)
					print("Platform version:", platform.version)
					print("---------------------------------------------------------------")
					print("Device name:", device.name)
					print("Device type:", cl.device_type.to_string(device.type))
					print("Device memory: ", device.global_mem_size//1024//1024, 'MB')
					print("Device max clock speed:", device.max_clock_frequency, 'MHz')
					print("Device compute units:", device.max_compute_units)
					print("Device max work group size:", device.max_work_group_size)
					print("Device max work item sizes:", device.max_work_item_sizes)

		properties = None
		if sharedGlContext:
			assert cl.have_gl()
			properties = get_gl_sharing_context_properties()

		devices = self.devices
		if gpuOnly and len(self.devices) > 1:
			devices = [self.devices[1]]

		print(properties, devices)
		self.context = cl.Context(properties=properties, devices=devices)

		self.queue = None

	def _buildKernel(self, kernel):
		program = cl.Program(self.context, kernel).build()
		if not self.queue:
			self.queue = cl.CommandQueue(self.context)
		return program

	def createLocalMemory(self, size):
		return cl.LocalMemory(size)

	def createArrayBuffer(self, array):
		return cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=array)

	def createArrayBufferWrite(self, array):
		return cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=array)

	def create2ComponentVektor(self, vec):
		if len(vec) != 2:
			raise InvalidArgument('Creating 2 component vector from list with %d elements', len(vec))

		return np.asarray(vec, dtype=cl_array.vec.float2)

	def getOpenGLBufferFromId(self, buffer_id):
		return cl.GLBuffer(self.context, cl.mem_flags.READ_WRITE, int(buffer_id))

	def releaseGlObjects(self, buffers):
		cl.enqueue_release_gl_objects(self.queue, buffers)

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



	def arrayFromBuffer(self, array, buffer):
		cl.enqueue_copy(self.queue, array, buffer)
		return array

	def calculateSimple(self, kernel, buffers, outputArray, globalsize=None, localsize=(1,)):
		"""
		Handles output buffer based on given numpy array
		"""
		program = self._buildKernel(kernel)

		outputBuffer = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, outputArray.nbytes)
		buffers.append(outputBuffer)

		if not globalsize:
			globalsize = outputArray.shape

		if self.queue:
			program.f(self.queue, globalsize, localsize, *buffers)
		else:
			print "No queue initialized"

		cl.enqueue_copy(self.queue, outputArray, outputBuffer)

		return outputArray
