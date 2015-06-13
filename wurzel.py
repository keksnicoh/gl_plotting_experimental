from functools import partial
import itertools

def series_next(func, x_0):
	yield x_0
	while True :
		x_0 = func(x_0)
		yield x_0

def wurzel(end, x=1.0):
	return (x+end/x) / 2

if __name__ == '__main__':
	series = series_next(partial(wurzel, 2.0), 1.0)
	print(list(itertools.islice(series, 0, 500000)))
