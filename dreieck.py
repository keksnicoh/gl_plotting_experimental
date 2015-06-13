import mygl.app
import mygl.discrete2dplot
from time import sleep
import math, numpy
import itertools
from functools import partial

# main function
def dreieck(a, x): return 2*a*x if x < 0.5 else 2*a*(1-x)
def wurzel(end, x): return (x+end/x) / 2
kernel = dreieck


# program logic ------

def series_next(func, x_0):
	yield x_0
	while True: x_0 = func(x_0); yield x_0

def main():
	a = 0.5
	n = 10
	x_0 = 0.3

	app = mygl.app.BasicGl()
	plot = mygl.discrete2dplot.Plotter(app)
	plot.set_data(list(itertools.islice(series_next(partial(kernel, a), x_0), 0, n)))

	while app.active():
		plot.render()
		user_interaction = keyboard(plot, app, a, x_0, n)
		if user_interaction is None and plot.force_render == True:
			continue
		if user_interaction is None:
			sleep(0.1)
			continue
		(a, x_0, n) = user_interaction
		plot.set_data(list(itertools.islice(series_next(partial(kernel, a), x_0), 0, n)))

def keyboard(plot, app, a, x_0, n):
	# keyboard interaction
	active = app.keyboardActive
	if 256 in active: app.exit = True; return

	KEY_65 = 0.01
	KEY_78 = int(math.ceil(float(n) / 100))
	KEY_83 = 0.0005
	KEY_88 = 0.005
	KEY_68 = 0.01
	KEY_87 = 0.001
	KEY_82 = 0.05
	KEY_262 = 0.01
	KEY_263 = 0.01
	KEY_264 = 0.01
	KEY_265 = 0.01
	delta = lambda o, a: (1 if o else -1) * a

	if 262 in active: plot.translation[0] -= KEY_262; plot.force_render = True
	elif 263 in active: plot.translation[0] += KEY_263; plot.force_render = True
	elif 264 in active: plot.translation[1] += KEY_264; plot.force_render = True
	elif 265 in active: plot.translation[1] -= KEY_265; plot.force_render = True
	#elif 264 in active: plot.rot = plot.rot + delta(o, KEY_264)
	#elif 265 in active: plot.rot = plot.rot + delta(o, KEY_265)


	if 93 in active: o = True
	elif 47 in active: o = False
	else: return

	if 65 in active: a = a + delta(o, KEY_65)
	elif 78 in active: n = max(1.0, n + delta(o, KEY_78))
	elif 88 in active: x_0 = max(.0, x_0 + delta(o, KEY_88))
	elif 83 in active: plot.dot_size = max(.0, plot.dot_size + delta(o, KEY_83))
	elif 68 in active: plot.dot_alpha = max(.0, min(1., plot.dot_alpha + delta(o, KEY_68)))
	elif 87 in active: plot.width = max(0., min(1., plot.width + delta(o, KEY_87)))
	elif 82 in active: plot.rot = plot.rot + delta(o, KEY_82)

	else: return
	sleep(0.01)
	print("a={}, x_0={}, n={}, dot_size={}, dot_alpha={}".format(a, x_0, n, plot.dot_size, plot.dot_alpha))
	return (a, x_0, n)

if __name__ == '__main__': main()

