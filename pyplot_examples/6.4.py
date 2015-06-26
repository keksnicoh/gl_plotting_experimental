#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import math

import matplotlib.pyplot as plt



class Duffing(object):
	"""docstring for Duffing"""
	def __init__(self, lambd, beta, omega, epsilon):
		super(Duffing, self).__init__()
		self.lambd = lambd
		self.beta = beta
		self.omega = omega
		self.epsilon = epsilon

	def plotScatter(self, listOfDataTuples, xLim=None, yLim=None):
		#plt.scatter(x,y, s=1)
		styles = [".", "-", "--", ":", ".-"]
		if len(listOfDataTuples) > len(styles):
			print "Too many Plots! Not enough styles to display"
			return
		for (x,y), style in zip(listOfDataTuples, styles):
			plt.plot(x, y, style, ms=2)
		if xLim:
			plt.xlim(xLim)
		if yLim:
			plt.ylim(yLim)

		#plt.plot([2,3], [0,0], "-")
		plt.show()


	# Wikipedia example
	# y' = y, y(0)=1
	# Algemein für gewähnlicihe Differentialgleichungen: y' = f(y,t)
	# --> f(y,t) = y
	# Euler methode: y_(n+1) = y_n + h*f(t_n, y_n)
	def simpleDifferentialExample(self):
		y = 1 # y_0
		h = 0.0125

		t_f = 4

		def f(t_value, y_value):
			return y

		iterations = int(1/h * t_f)
		for t in xrange(iterations):
			y = y + h * f(t, y)

		print y

	# Calucation for Exercise 6.2
	def calculation(self, awp, phasendiagramm=False):
		(x, y) = awp
		h = 0.001
		t_f = 200

		def f_x(y_value):
			return y_value

		def f_y(y_value, x_value, lambd, epsilon, theta, beta):
			return (epsilon * math.cos(theta)) - (lambd * y_value) - (beta * x_value * x_value * x_value)

		iterations = int(1/h * t_f)
		x_Data = []
		y_Data = []
		for i in xrange(iterations):
			t = i/float(iterations) * t_f
			theta = self.omega * t
			x = x + h * f_x(y)
			y = y + h * f_y(y, x, self.lambd, self.epsilon, theta, self.beta)

			x_Data.append(x)
			y_Data.append(y)

		if phasendiagramm:
			self.plotScatter([(x_Data, y_Data)])
		else:
			self.plotScatter([(xrange(iterations), x_Data)])



if __name__ == '__main__':
	app = Duffing(0.08, 1.0, 1.0, 1.2)

	afw = [
		(0.21, 0.02),
		(1.05, 0.77),
		(-0.67, 0.02),
		(-0.46, 0.30),
		(-0.43, 0.12)
	]


	app.calculation(afw[3], True)







