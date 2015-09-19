def f(x,r):
	return x*r*(1.0-x)


x = 1.1
for i in xrange(1000):
	x = f(x, 0.9)
	print(x)