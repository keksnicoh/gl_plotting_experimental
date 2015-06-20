
# Example Plot from Script
import matplotlib.pyplot as plt
import math

import numpy as np

class chaos(object):
	"""docstring for chaos"""
	def __init__(self):
		super(chaos, self).__init__()


	def log_dr(self, x, a):
		if x < 0.5:
			return 2*a*x
		else:
			return 2*a*(1-x)

	def logAbbildung(self, x, r):
		return r*x*(1-x)

	def zweiteLogAbbildung(self, x, r):
		return r**2*x*(1-x)*(1-r*x*(1-x))

	def sinAbblidung(self, x, r):
		return r*math.sin(x)

	def ableitungSinAbblidung(self, x, r):
		return r*math.cos(x)

	def ableitungLogAbbildung(self, x, r):
		return r-2*r*x

	def bifrac(self, abbildung, paramRange, d_r, iterationCount):
		yData = []
		xData = []

		for x in range(1, 100):
			x_0 = x / 100.0
			r = paramRange[0]
			while r < paramRange[1]:
				(x,y) = self.iterate(abbildung, x_0, (r,), iterationCount)
				yData.append(y[-1])
				xData.append(r)
				r += d_r
		self.plotScatter([(xData,yData)])


	def iterate(self, abbildung, x_n, abbildungArgs, iterationCount):
		n = 0
		y = [x_n]
		x = [0]
		while n < iterationCount:
			x_n = abbildung(x_n, *abbildungArgs)
			y.append(x_n)
			n += 1
			x.append(n)

		return (x, y)

	def fastIterate(self, abbildung, x_n, abbildungArgs, iterationCount):
		n = 0
		y = [x_n]
		while n < iterationCount:
			x_n = abbildung(x_n, *abbildungArgs)
			y.append(x_n)
			n += 1

		return y

	def dreieckPlot(self, x_0, a):
		(x,y) = self.iterate(self.log_dr, x_0, (a,), 300)
		self.plotScatter([(x,y,".")], (200,300))

	def plotScatter(self, tupleOfDataTuples, xLim=None, yLim=None):
		#plt.scatter(x,y, s=1)
		styles = [".", "-", "--", ":", ".-"]
		if len(tupleOfDataTuples) > len(styles):
			print "Too many Plots! Not enough styles to display"
			return
		for (x,y), style in zip(tupleOfDataTuples, styles):
			plt.plot(x, y, style, ms=2)
		if xLim:
			plt.xlim(xLim)
		if yLim:
			plt.ylim(yLim)

		#plt.plot([2,3], [0,0], "-")
		plt.show()

	def lyapunovExponent(self, ableitung, x_i, abbildungArgs, n):
		i = 0
		summe = 0
		while i < n - 1:
			x_i = ableitung(x_i, *abbildungArgs)
			summe += math.log(math.fabs(x_i)) if x_i != 0.0 else 0
			i += 1

		return (1/float(n))*summe

	def plotLyapunovExponent(self, ableitung, paramRange, d_r, x_0, n):
		xData = []
		yData = []
		r = paramRange[0]
		while r < paramRange[1]:
			lyap = self.lyapunovExponent(ableitung, x_0, (r,), n)
			xData.append(r)
			yData.append(lyap)
			r += d_r

		self.plotScatter([(xData,yData)])

	def approx(self, value1, value2, eps):
		if abs(value1 - value2) <= eps:
			return True
		return False


	def inifinityPeriodenverdopplung(self):
		r = 1
		d_r = 0.1
		epsilon = 0.00001
		lastCount = 0

		values = []

		while r < 4:
			(x,y) = self.iterate(self.logAbbildung, 0.1, (r,), 1000)
			#Analyse Fixpoints
			last = 0
			count = 0
			for p in reversed(y):
				if not last:
					last = p
				elif self.approx(last, p, epsilon):
					break
				count += 1
			if lastCount != count:
				if lastCount and lastCount*2 != count:
					if len(values) > 3:
						feig = (values[-3][1] - values[-2][1]) / (values[-2][1] - values[-1][1])
						print "Feigenbaumkonstante: %.15f" % feig
					d_r = d_r / 10
					r = values[-1][1]
					print "Reached chaos! Start with %.15f steps from r=%.15f" % (d_r, r)
					continue
				print "Got %i paths at r=%.15f" % (count, r)
				values.append((count, r))
				lastCount = count
			r += d_r

	# Trying to find all r where there is "periodenverdopplung"
	# Continuisly scanning through the range untill reaching chaos, then slicing the range adjust the parameters
	# *goal indicates how many periodenverdopllungen we are looking for, thus we know how many y values at the end we have to analyse
	def optimizedPeriodenverdopplung(self, rRange, abbildung, x_0, iterations):
		d_r = np.float32(0.1)
		r = np.float32(rRange[0])
		end = np.float32(rRange[1])

		lastCount = 1
		fixpoints = []
		realFP = []
		while r < end:
			y = self.fastIterate(abbildung, x_0, (r,), iterations)

			count = 0
			last = 0
			for p in reversed(y):
				if last and np.isclose([y[-1]], [p], rtol=1e-5, atol=1e-8):
					#print "%.20f, %.20f" % (last, p)
					#print "Got something r: %f periods: %d" % (r, count)
					fixpoints.append(r)
					break
				count += 1
				last = 1

			if count == lastCount*2:
				realFP.append((r, count))
				print "%.20f, %d " % (r, count)
				if len(realFP) > 2:
					print "Feigenbaum: %.8f" % ((realFP[-2][0] - realFP[-3][0]) / (realFP[-1][0] - realFP[-2][0]))

			if count > lastCount*2 and len(fixpoints) > 2:
				print "reached chaos"
				rLength = r - fixpoints[-2]
				r = fixpoints[-2]
				d_r = rLength / 10.
			lastCount = count

			r += d_r

	# Trying to find periodenverdopplung by searching specified ranges
	def findVerdopplung(self):
		r = 3.4
		data = []
		for periods in [2] * 100:
			subdata = []
			d_r = (3.57 - r) / 4000.
			while r < 3.57:
				(x,y) = self.iterate(self.logAbbildung, 0.5, (r,), 5000)

				if np.isclose([y[-1]], [y[-(periods + 1)]], rtol=1e-20, atol=1e-20) and not np.isclose([y[-1]], [y[-periods]], rtol=1e-20, atol=1e-20):
					subdata.append((r, periods))
					#print r, periods

				r += d_r
			data.append(subdata[1])
			r = subdata[-1][0]

			#if len(data) > 2:
				#print "Feigenbaum: %.8f based on %s" % ((data[-2][0] - data[-3][0]) / (data[-1][0] - data[-2][0]), data)
			print data[-1]
		#print data

	def estimatePeriodenverdopplung(self):
		r = 3.4
		d_r = 0.000005
		epsilon = 0.00001
		lastCount = 0

		values = []

		while r < 3.57:
			(x,y) = self.iterate(self.logAbbildung, 0.1, (r,), 1000)
			#Analyse Fixpoints
			last = 0
			count = 0
			for p in reversed(y):
				if not last:
					last = p
				elif self.approx(last, p, epsilon):
					break
				count += 1
			if lastCount != count:
				if lastCount and lastCount*2 != count:
					break
				values.append((count, r))
				lastCount = count
			r += d_r
		print values

		feig = (values[-3][1] - values[-2][1]) / (values[-2][1] - values[-1][1])
		print feig

		#self.plotScatter([(x,y)], (990,1000), (0,1))

if __name__ == '__main__':
	#dreieckPlot()
	app = chaos()
	#app.optimizedPeriodenverdopplung((1,4), app.logAbbildung, 0.3, 20000)
	app.findVerdopplung()
	#app.dreieckPlot(0.8, 0.98)
	#app.bifrac(app.logAbbildung, (1, 4), 0.002, 500)
	#app.bifrac(app.sinAbblidung, (1,4), 0.002, 500)
	#print app.lyapunovExponent(app.ableitungLogAbbildung, 0.5, (1,), 2000)
	#app.plotLyapunovExponent(app.ableitungLogAbbildung, (1,4), 0.01, 0.5, 5000)
	#app.plotLyapunovExponent(app.ableitungSinAbblidung, (1,4), 0.0002, 0.5, 5000)
	#app.inifinityPeriodenverdopplung()




