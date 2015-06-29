from plotting.app import PlotterWindow
from plotting import graph, domain
import math
import numpy
class DglDomain(domain.Domain):

    def __init__(self, length):
        domain.Domain.__init__(self, length)
        self.lambd = 0.08
        self.epsilon = 0.2
        self.omega = 1
        self.beta = 1
        self.initial_condition = (3,4)

    def init_vbo(self, length):
        domain.Domain.init_vbo(self, length)
        # OPENGL BUFFER ID self.vbo.get(0).id
        (x, y) = self.initial_condition
        h = 0.001
        t_f = 200

        def f_x(y_value):
            return y_value

        def f_y(y_value, x_value, lambd, epsilon, theta, beta):
            return (epsilon * math.cos(theta)) - (lambd * y_value) - (beta * x_value * x_value * x_value)

        data = numpy.zeros(length*2)
        iterations = int(1/h * t_f)
        for i in xrange(length):
            t = i/float(length) * t_f
            theta =  self.omega * t
            x = x + h * f_x(y)
            y = y + h * f_y(y, x, self.lambd, self.epsilon, theta, self.beta)

            data[2*i] = x
            data[2*i+1] = y

        self.push_data(data)
    def get_dot_size(self): return max(0.002, 1.0/self.length)

window = PlotterWindow(axis=(10.0,10.0), origin=(5.0,5.0))
window.plotter.add_graph('bifurkation', graph.Discrete2d(DglDomain(500000)))
window.run()
