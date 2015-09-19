#-*- coding: utf-8 -*-
"""
@author Jesse Hinrichsen <jesse@j-apps.com>

"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget
import math, numpy

OSZILATION_KERNEL = """
    __kernel void f(float x, float y, int iterations, float lambda, float beta, float omega, float epsilon, int start_iteration, float h, __global float *result)
    {
        float t = 0.0;
        float theta = 0;
        result[0] = 0.0;
        result[1] = x;
        for(int i=2; i < iterations*2; i += 2) {
            t = t + h;
            theta = t * omega;
            result[i] = t;
            result[i+1] = result[i-1] + h * y;
            y = y + h * (epsilon * cos(theta) - lambda * y - beta * result[i-1] * result[i-1] * result[i-1]);
        }

    }
"""


PHASE_KERNEL = """
    __kernel void f(float x, float y, int iterations, float lambda, float beta, float omega, float epsilon, int start_iteration, float h, __global float *result)
    {
        float theta = 0;
        float new_x = 0;

        float t = 0;

        for(int i=0; i < (iterations+start_iteration)*2; i += 2) {
            t = t + h;
            theta = t * omega;
            new_x = x + h * y;

            y = y + h * (epsilon * cos(theta) - lambda * y - beta * x * x * x);

            x = new_x;

            if(i > start_iteration) {
                result[i-start_iteration*2] = x;
                result[i+1-start_iteration*2] = y;
            }
        }

    }
"""

PHASE_KERNEL_RK = """
    __kernel void f(float x, float y, int iterations, float lambda, float beta, float omega, float epsilon, int start_iteration, float h, __global float *result)
    {
        float t = 0.0f;

        float k1 = 0.0f;
        float k2 = 0.0f;
        float k3 = 0.0f;
        float k4 = 0.0f;

        float l1 = 0.0f;
        float l2 = 0.0f;
        float l3 = 0.0f;
        float l4 = 0.0f;

        for(int i=0; i < (iterations+start_iteration)*2; i += 2) {
            
            k1 = h * (epsilon * cos(t * omega) - lambda * y - beta * x * x * x);
            l1 = h * y;

            k2 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k1) - beta * pow(x+ 0.5f*l1, 3));
            l2 = h * (y + 0.5f*k1);

            k3 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k2) - beta * pow(x+ 0.5f*l2, 3));
            l3 = h * (y + 0.5f*k2);

            k4 = h * (epsilon * cos((t + h) * omega) - lambda * (y + k3) - beta * pow(x + l3, 3));
            l4 = h * (y + k3);

            y = y + (k1 + 2.0f*k2 + 2.0f*k3 + k4) / 6.0f;
            x = x + (l1 + 2.0f*l2 + 2.0f*l3 + l4) / 6.0f;

            t = t + h;

            if(i > start_iteration) {
                result[i-start_iteration*2] = x;
                result[i+1-start_iteration*2] = y;
            }
        }
    }
"""

POINCARE_EULER = """
    __kernel void f(float x, float y, int iterations, float lambda, float beta, float omega, float epsilon, int start_iteration, float h, __global float *result)
    {
        float theta = 0;
        float t = 0;
        float last_point = 0.0f;
        float position = 0.0f;

        float last_x = x;
        float new_x = x;
        float last_y = y;

        for(int i=0; i < iterations*2; i += 2) {
            t = t + h;
            theta = t * omega;
            new_x = last_x + h * last_y;
            last_y = last_y + h * (epsilon * cos(theta) - lambda * last_y - beta * new_x * new_x * new_x);
            last_x = new_x;

            position = sin(theta);
            if (i > start_iteration && last_point*position < 0.0f) {
                result[i] = last_x;
                result[i+1] = last_y;
            }else {
                result[i] = 30.0f;
                result[i+1] = 30.0f;
            }
            
            last_point = position;
        }

    }
"""

POINCARE_RK = """
    __kernel void f(float x, float y, int iterations, float lambda, float beta, float omega, float epsilon, int start_iteration, float h, __global float *result)
    {
        float t = 0.0f;

        float k1 = 0.0f;
        float k2 = 0.0f;
        float k3 = 0.0f;
        float k4 = 0.0f;

        float l1 = 0.0f;
        float l2 = 0.0f;
        float l3 = 0.0f;
        float l4 = 0.0f;

        float position = 0.0f;
        float last_point = 0.0f;
        for(int i=0; i < (iterations+start_iteration)*2; i += 2) {
            
            k1 = h * (epsilon * cos(t * omega) - lambda * y - beta * x * x * x);
            l1 = h * y;

            k2 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k1) - beta * pow(x+ 0.5f*l1, 3));
            l2 = h * (y + 0.5f*k1);

            k3 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k2) - beta * pow(x+ 0.5f*l2, 3));
            l3 = h * (y + 0.5f*k2);

            k4 = h * (epsilon * cos((t + h) * omega) - lambda * (y + k3) - beta * pow(x + l3, 3));
            l4 = h * (y + k3);

            y = y + (k1 + 2.0f*k2 + 2.0f*k3 + k4) / 6.0f;
            x = x + (l1 + 2.0f*l2 + 2.0f*l3 + l4) / 6.0f;

            t = t + h;

            position = sin(t);
            if(i > start_iteration && last_point*position < 0.0f) {
                result[i-start_iteration*2] = x;
                result[i+1-start_iteration*2] = y;
            }
            else {
                result[i-start_iteration*2] = 0.0f;
                result[i+1-start_iteration*2] = 0.0f;
            }

            last_point = position;
            i += 1;
        }
    }
"""

active_cl_kernel = PHASE_KERNEL_RK

(x_0, y_0) = (0.21, 0.02) #small 1
#(x_0, y_0) = (0.17, 0.02) #custom

#(x_0, y_0) = (1.05, 0.77) #gone 2
#(x_0, y_0) = (-0.67, 0.02) #small 3
#(x_0, y_0) = (-0.46, 0.30) #big 4
#(x_0, y_0) = (-0.43, 0.12) #small 5
#(x_0, y_0) = (3.0,4.0)

(lambd, epsilon) = (0.08, 0.2)
#(lambd, epsilon) = (0.2, 1.0)
#(lambd, epsilon) = (0.4, 7.5)
#(lambd, epsilon) = (0.04, 7.5)

offset = 100000
length = 500000

h = 0.01

def calculate_pythone():
    data = numpy.zeros(length, dtype=numpy.float32)
    theta = 0.0
    new_x = 0.0
    omega = 1.0
    beta = 1.0
    t = 0.0
    x = x_0
    y = y_0
    for i in xrange(length/2):
        new_x = x + h * y
        y = y + h * (epsilon * math.cos(theta) - lambd * y - beta * x * x * x)

        theta = t * omega
        t = t + h
        x = new_x

        data[2*i] = x
        data[2*i + 1] = y

    print(x, y)
    return data

cl_kernel_params = [
    numpy.float32(x_0),
    numpy.float32(y_0),
    numpy.int32(length), 
    numpy.float32(lambd),

    numpy.float32(1.0),

    numpy.float32(1.0),
    numpy.float32(epsilon),

    numpy.int32(offset),
    numpy.float32(h),
]

phase_axis = (7.0, 10.0)
phase_origin = (-0.25, 0.25)
x_phase_label = "x"
y_phase_label = "y"


oszilation_axis = (20.0, 2.0)
oszilation_origin = (0.0, 1.0)
x_oszillation_label = "Zeit"
y_oszillation_label = "Spannung in [V]"

#window = PlotterWindow(axis=oszilation_axis, origin=oszilation_origin, bg_color=[1.0,1.0,1.0,1], x_label=x_oszillation_label, y_label=y_oszillation_label)

window = PlotterWindow(axis=phase_axis, origin=phase_origin, bg_color=[1.0, 1.0, 1.0,1], x_label=x_phase_label, y_label=y_phase_label)

cl_domain = domain.CLDomain(active_cl_kernel, length, cl_kernel_params, dimension=2)
cl_domain.calculate()
#domain = domain.Domain(length)
#domain.push_data(calculate_pythone())
#cl_domain = domain


window.plotter.add_graph('duffing', graph.Discrete2d(cl_domain))
window.plotter.get_graph('duffing').set_colors(color_min=[0.0, 0.0, 0.0, 1.0], color_max=[0.0, 0.0, 0.0, 1.0])
window.plotter.get_graph('duffing').set_dotsize(0.001)
window.plotter.gl_plot.precision_axis = (2,2)

def update_uniform(self, value):
    param = self[0].args[0]

    if param == 'h':
        cl_domain.cl_params[8] = numpy.float32(value)
        print("h: %f" % cl_domain.cl_params[8])
    elif param == 'offset':
        cl_domain.cl_params[7] = numpy.int32(value)
    elif param == 'x_0':
        cl_domain.cl_params[0] = numpy.float32(value)
        print("x_0: %f" % cl_domain.cl_params[0])
    elif param == 'e':
        cl_domain.cl_params[6] = numpy.float32(value)
        print("e: %f" % cl_domain.cl_params[8])
    
    cl_domain.calculator.calculateGL(cl_domain.kernel, cl_domain.cl_params, [cl_domain.gl_buffer], (1,))


uniforms = window.plotter.get_uniform_manager()
#uniforms.set_global('h', h, 10**-2)
uniforms.set_global('x_0', x_0, 10**-1)
uniforms.set_global('e', epsilon, 10**-1)
uniforms.set_global('y_0', y_0, 10**-1)
#uniforms.set_global('offset', offset, 100)
#uniforms.set_global('it_offset', iteration_offset, 1000)
widget = widget.Uniforms(uniforms, update_callback=update_uniform)
widget.floating_percision = 2
window.add_widget('manipulate', widget)

window.run()





