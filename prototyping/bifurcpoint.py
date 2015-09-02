def logAbbildung(x, r):
		return r*x*(1-x)

x_real=2.0/3.0
x=0.2
r=3

iterations = [
	30*10**3,
	30*10**4,
	30*10**5
]

#iterations = [x*x for x in range(190, 200)]

result = []

for iteration in iterations:
	for i in xrange(iteration):
		x=logAbbildung(x, r)
	result.append(x)


diff = [x_real - x for x in result]

print result
print diff