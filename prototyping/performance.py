#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from pymongo import MongoClient

import numpy as np
import sys, os, getopt


import pyopencl as cl
from pyopencl import array

import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

class Performance(object):
	"""docstring for Performance"""

	def __init__(self, gpuOnly=True):
		super(Performance, self).__init__()
		self.platform = cl.get_platforms()[0]
		self.devices = self.platform.get_devices()

		self.r = 3.2
		self.x = 0.4
		self.iterations = 100000

		if gpuOnly and len(self.devices) > 1:
			self.context = cl.Context([self.devices[1]])
		else:
			self.context = cl.Context(self.devices)

		self.queue = None


	# buffers = [ {"mem_flag": "", ""}, {} ]
	#
	#
	#
	def buildKernel(self, kernel):
		kernel = cl.Program(self.context, kernel).build()
		self.queue = cl.CommandQueue(self.context)
		return kernel


	def iterateForRRange(self, start, end, steps, periods):
		r_values = np.arange(start, end, steps, dtype="float32")
		result_np = np.empty_like(r_values)

		x = np.float32(self.x)

		r_buffer = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=r_values)
		result_buffer = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, result_np.nbytes)

		program = self.buildKernel("""
			__kernel void log_function(__global const float *r, float x, int iterations, int periods, __global float *result)
			{
				int gid = get_global_id(0);
				for (int i=0; i < iterations; i++) {
					x = r[gid] * x - r[gid] * x * x;
				}
				// Calculate periods more
				float x_p = x;
				for (int a=0; a < periods; a++) {
					x_p = r[gid] * x_p - r[gid] * x_p * x_p;
				}
				
				if (x == x_p) {
					result[gid] = r[gid];
				}
				else {
					result[gid] = 0;
				}
			}
			""")

		
		if app.queue:
			program.log_function(self.queue, result_np.shape, None, r_buffer, x, np.int32(self.iterations), np.int32(periods), result_buffer)
		else:
			print "No queue initialized"

		cl.enqueue_copy(app.queue, result_np, result_buffer)

		return result_np


	def runTest(self):
		r = np.float32(self.r)
		result_np = np.array([0], dtype=np.float32)

		x = np.float32(self.x)
		#x_buffer = cl.Buffer(app.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=x),
		#r_buffer = cl.Buffer(app.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=np.float32(3.2)),
		result_buffer = cl.Buffer(app.context, cl.mem_flags.WRITE_ONLY, result_np.nbytes)

		program = self.buildKernel("""
			__kernel void log_function(float x, float r, int iterations, __global float *result)
			{
				for (int i=0; i < iterations; i++) {
					x = r * x - r * x * x;
				}
					
				result[0] = x;
			}
			""")

		if app.queue:
			program.log_function(app.queue, result_np.shape, None, x, r, np.int32(self.iterations), result_buffer)
		else:
			print "No queue initialized"

		cl.enqueue_copy(app.queue, result_np, result_buffer)

		return result_np[0]








	def nplogFunction(self, x, r):
		return np.multiply(np.multiply(r,x), (np.subtract(1, x)))

	def npdoubleLogFunction(self, x, r):
		return np.multiply(np.multiply(r, np.multiply(np.multiply(r,x), (np.subtract(1, x)))), (np.subtract(1, np.multiply(np.multiply(r,x), (np.subtract(1, x))))))

	def logFunction(self, x, r):
		return r*x*(1-x)

	def doubleLogFunction(self, x, r):
		return r*r*x*(1-x)*(1-r*x*(1-x))

	def fourLogFunction(self, x, r):
		return r*r*r*r*x*(1-x)*(1-r*x*(1-x))*(1-r*r*x*(1-x)*(1-r*x*(1-x)))*(1-r*r*r*x*(1-x)*(1-r*x*(1-x))*(1-r*r*x*(1-x)*(1-r*x*(1-x))))


	def regularTest(self):
		r = np.float32(2.2)
		iterations = 50000

		x_1 = np.float32(0.3)
		start_time = time.time()
		for i in xrange(iterations):
			if np.isclose(self.nplogFunction(x_1, r), x_1, rtol=0.0, atol=0.0):
				print i
				break
			else:
				x_1 = self.nplogFunction(x_1, r)
		print "Numpy Simple: %.55f in %f seconds" % (x_1, time.time() - start_time)

		x_1 = np.float32(0.3)
		start_time = time.time()
		for i in xrange(iterations - 1):
			if np.isclose(self.nplogFunction(x_1, r), x_1, rtol=0.0, atol=0.0):
				print i
				break
			else:
				x_1 = self.nplogFunction(x_1, r)
		print "Numpy Simple: %.55f in %f seconds (-1 iterations)" % (x_1, time.time() - start_time)


		x_1 = np.float32(0.5)
		start_time = time.time()
		for i in xrange(iterations/2):
			x_1 = self.npdoubleLogFunction(x_1, r)
		print "Numpy Double: %.55f in %f seconds" % (x_1, time.time() - start_time)

		r = 2.2



		x_1 = 0.3
		start_time = time.time()
		for i in xrange(iterations):
			x_1 = self.logFunction(x_1, r)
		print "----- Simple: %.55f in %f seconds" % (x_1, time.time() - start_time)

		x_1 = 0.3
		start_time = time.time()
		for i in xrange(iterations - 1):
			x_1 = self.logFunction(x_1, r)
		print "----- Simple: %.55f in %f seconds (-2 iterations)" % (x_1, time.time() - start_time)

		exit(0)


		x_1 = 0.5
		start_time = time.time()
		for i in xrange(iterations/2):
			x_1 = self.doubleLogFunction(x_1, r)
		print "----- Double: %.20f in %f seconds" % (x_1, time.time() - start_time)

		x_1 = 0.5
		start_time = time.time()
		for i in xrange(iterations/4):
			x_1 = self.fourLogFunction(x_1, r)
		print "----- Four--: %.20f in %f seconds" % (x_1, time.time() - start_time)

	def compareRegualrAndOpenCL(self):
		start_time = time.time()
		result = app.runTest()
		print "Result: %.55f in %f seconds" % (result, time.time() - start_time)

		x_1 = app.x
		start_time = time.time()
		for i in xrange(app.iterations):
			x_1 = app.logFunction(x_1, app.r)
		print "Result: %.55f in %f seconds" % (x_1, time.time() - start_time)

# Sehr interessantes Ergebnis!
# Zunaechst ergibt sich ein erheblicher Unterschied ob man numpy benutzt oder nicht. Dabei stellt man fest, dass
# numpy gut 20 mal langsamer ist.
# Wir vermuten allerdings, dass bei der reinen Python berechnung gerundet wird.
# Auffällig ist ausserdem, dass bei der numpy berechnung bereits bei einem Parameter von r=2.3 eine 2er Periode
# festzustellen ist (iteration - 1 ergibt anderen Wert, iteration - 2 gibt selben Wert)
# Bei der Python Berechnung zeigt sich das periodische Verhalten für alle Parameter r
if __name__ == "__main__":
	
	app = Performance()

	for foo in app.iterateForRRange(3.434, 3.5, 0.0000001, 2):
		if foo != 0.0:
			print foo
	




