#-*- coding: utf-8 -*-
"""
@author Jesse Hinrichsen <jesse@j-apps.com>

"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget
import math, numpy

OSZILATION_KERNEL = """//#pragma OPENCL EXTENSION cl_khr_fp64 : enable
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

PHASE_KERNEL = """//#pragma OPENCL EXTENSION cl_khr_fp64 : enable
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

PHASE_KERNEL_RK = """//#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(float x, float y, int iterations, float lambda, float beta, float omega, float epsilon, int start_iteration, float h, __global float *result)
    {
        float t = 0.0f;

        float new_x = 0.0f;

        float runge_x = 0.0f;
        float runge_x_k2 = 0.0f;

        float k1 = 0.0f;
        float k2 = 0.0f;
        float k3 = 0.0f;
        float k4 = 0.0f;
        for(int i=0; i < (iterations+start_iteration)*2; i += 2) {
            
            new_x = x + h * y;

            runge_x = x + 0.5f*h;
            runge_x_k2 = runge_x*runge_x*runge_x;

            k1 = h * (epsilon * cos(t * omega) - lambda * y - beta * x * x * x);
            k2 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k1) - beta * runge_x_k2);
            k3 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k2) - beta * runge_x_k2);
            k4 = h * (epsilon * cos((t + h) * omega) - lambda * (y + k3) - beta * (x+h) * (x+h) * (x+h));

            y = y + (k1 + 2.0f*k2 + 2.0f*k3 + k4) / 6.0f;


            x = new_x;
            t = t + h;

            if(i > start_iteration) {
                result[i-start_iteration*2] = x;
                result[i+1-start_iteration*2] = y;
            }
        }
    }
"""

active_cl_kernel = PHASE_KERNEL

(x_0, y_0) = (0.21, 0.02) #small
#(x_0, y_0) = (1.05, 0.77) #gone
#(x_0, y_0) = (-0.67, 0.02) #small
#(x_0, y_0) = (-0.46, 0.30) #big
#(x_0, y_0) = (-0.43, 0.12) #small
#(x_0, y_0) = (3.0,4.0)

#(lambd, epsilon) = (0.2, 0.0)
#(lambd, epsilon) = (0.2, 1.0)
(lambd, epsilon) = (0.08, 0.2)

offset = 50000
length = 500000

h = 10**-4

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

phase_axis = (2.0, 2.0)
phase_origin = (1.0, 1.0)
x_phase_label = "x"
y_phase_label = "y"


oszilation_axis = (20.0, 2.0)
oszilation_origin = (0.0, 1.0)
x_oszillation_label = "Zeit"
y_oszillation_label = "Spannung in [V]"

#window = PlotterWindow(axis=oszilation_axis, origin=oszilation_origin, bg_color=[1.0,1.0,1.0,1], x_label=x_oszillation_label, y_label=y_oszillation_label)

window = PlotterWindow(axis=phase_axis, origin=phase_origin, bg_color=[1.0, 1.0, 1.0,1], x_label=x_phase_label, y_label=y_phase_label)

cl_domain = domain.CLDomain(active_cl_kernel, length, cl_kernel_params, dimension=2)
#domain = domain.Domain(gl_buffer_length)
#domain.push_data(data)


window.plotter.add_graph('duffing', graph.Line2d(cl_domain))
window.plotter.get_graph('duffing').set_colors(color_min=[0.0, 0.0, 0.0, 1.0], color_max=[0.0, 0.0, 0.0, 1.0])
window.plotter.get_graph('duffing').set_dotsize(0.001)
window.plotter.gl_plot.precision_axis = (1,1)

def update_uniform(self, value):
    param = self[0].args[0]

    if param == 'h':
        cl_domain.cl_params[8] = numpy.float32(value)
    if param == 'offset':
        cl_domain.cl_params[7] = numpy.int32(value)

    cl_domain.calculator.calculateGL(cl_domain.kernel, cl_domain.cl_params, [cl_domain.gl_buffer], (1,))


uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('h', h, 10**-4)
uniforms.set_global('offset', offset, 100)
#uniforms.set_global('it_offset', iteration_offset, 1000)
widget = widget.Uniforms(uniforms, update_callback=update_uniform)
widget.floating_percision = 4
window.add_widget('manipulate', widget)

window.run()





