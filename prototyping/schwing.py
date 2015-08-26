import math, numpy

R = 100 # Ohm
L = 2367*10**-6 # H

C_r = 82*10**-12 #F
C_f = 56*10**-18 #F

I_f = 2.8*10**-12 #A

phi = 0.6

V_s = 2.0 #V
V_t = 0.034 #V

w = 1.0 / math.sqrt(L*C_r)

V_d = 0.0
I = 0.0


iterations = 1000000
h = 10**-8
time = 0.0

data = numpy.zeros(iterations*2)

for i in xrange(iterations):
	time = time + h
	theta = w*time

	new_I = I + h * ( V_s*math.cos(theta) - V_d - R*I ) / L

	_exp = math.exp(-V_d/V_t)
	if V_d > -0.6:
		#print "Sperrrichtung"
		V_d = V_d + h * (I - I_f*(1.0 -_exp)) / (C_r*(1+V_d/phi)**-0.44 )
	else:
		#print "Durchlass"
		V_d = V_d + h * (I - I_f*(1.0 - _exp)) / (C_f*_exp)


	I = new_I

	data[2*i] = time*10000
	data[2*i+1] = I

	#print I, V_d

#print data