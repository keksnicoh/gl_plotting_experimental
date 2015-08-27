#-*- coding: utf-8 -*-
"""
OpenCL implementation for domain calculation on Duffing equation
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget
import math
import numpy as np

"""
Kernel to calculate duffing equation and writes (x, y) data to given GLBuffer
"""
PHASE_KERNEL = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, int start_iteration, __global float *result)
    {
        //iterations = iterations + start_iteration;
        float h = time / convert_float(iterations);
        float theta = 0;
        float new_x = 0;

        float t = 0;
        float x = awp.x;
        float y = awp.y;

        for(int i=2; i < (iterations+start_iteration)*2; i += 2) {
            t = i / (2.0f * iterations) * time;
            theta = t * omega;
            new_x = x + h * y;

            y = y + h * (epsilon * cos(theta) - lambda * y - beta * x * x * x);

            x = new_x;

            if(i > start_iteration) {
                result[i-start_iteration] = x;
                result[i+1-start_iteration] = y;
            }
        }

    }
"""

"""
Kernel to calculate duffing equation and writes (t, x) data to given GLBuffer
"""
OSZILATION_KERNEL = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, int start_iteration, __global float *result)
    {
        float h = time / convert_float(iterations);
        float t = 0.0;
        float theta = 0;
        result[0] = 0.0;
        result[1] = awp.x;
        float y = awp.y;
        for(int i=2; i < iterations*2; i += 2) {
            t = i / (2.0f*iterations) * time;
            theta = t * omega;
            result[i] = t;
            result[i+1] = result[i-1] + h * y;
            y = y + h * (epsilon * cos(theta) - lambda * y - beta * result[i-1] * result[i-1] * result[i-1]);
        }
    }
"""

"""
Kernel to calculate duffing equation via Runge Kutter of grade 4
TODO:
- stop time to compare
- calculate error compared to euler-cauchy
- implement adaptive schrittweitenkontrolle
"""
OSZILATION_KERNEL_RK = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, int start_iteration, __global float *result)
    {
        float h = time / convert_float(iterations);

        float t = 0.0f;
        float x = awp.x;
        float y = awp.y;

        float new_x = 0.0f;

        float k1 = 0.0f;
        float k2 = 0.0f;
        float k3 = 0.0f;
        float k4 = 0.0f;
        for(int i=0; i < iterations*2; i += 2) {
            new_x = x + h * y;

            k1 = h * (epsilon * cos(t * omega) - lambda * y - beta * x * x * x);
            k2 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k1) - beta * x * x * x);
            k3 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k2) - beta * x * x * x);
            k4 = h * (epsilon * cos((t + h) * omega) - lambda * (y + k3) - beta * x * x * x);

            y = y + (k1 + 2*k2 + 2*k3 + k4) / 6.0f;


            x = new_x;
            t = i / (2.0f*iterations) * time;
            result[i] = t;
            result[i+1] = x;
        }
    }
"""

PHASE_KERNEL_RK = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, int start_iteration, __global float *result)
    {
        float h = time / convert_float(iterations);

        float t = 0.0f;
        float x = awp.x;
        float y = awp.y;

        float new_x = 0.0f;

        float k1 = 0.0f;
        float k2 = 0.0f;
        float k3 = 0.0f;
        float k4 = 0.0f;
        for(int i=0; i < iterations*2; i += 2) {
            new_x = x + h * y;

            k1 = h * (epsilon * cos(t * omega) - lambda * y - beta * x * x * x);
            k2 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k1) - beta * x * x * x);
            k3 = h * (epsilon * cos((t + 0.5f*h) * omega) - lambda * (y + 0.5f*k2) - beta * x * x * x);
            k4 = h * (epsilon * cos((t + h) * omega) - lambda * (y + k3) - beta * x * x * x);

            y = y + (k1 + 2*k2 + 2*k3 + k4) / 6.0f;


            x = new_x;
            t = i / (2.0f*iterations) * time;
            result[i] = x;
            result[i+1] = y;
        }
    }
"""

COLOR_KERNEL = """
vec4 f(vec4 x) {
    return vec4(x.x, x.y, x.z, 0.5);
}
"""

NORMAL = """
uniform float x_0;
uniform float y_0;
vec4 f(vec4 x) {
    return vec4(x_0, y_0, 0, 0.5);
}
"""

active_cl_kernel = PHASE_KERNEL_RK

(x_0, y_0) = (0.21, 0.02) #small
#(x_0, y_0) = (1.05, 0.77) #gone
#(x_0, y_0) = (-0.67, 0.02) #small
#(x_0, y_0) = (-0.46, 0.30) #big
#(x_0, y_0) = (-0.43, 0.12) #small
#(x_0, y_0) = (3.0,4.0)

#(lambd, epsilon) = (0.2, 0.0)
#(lambd, epsilon) = (0.2, 1.0)
(lambd, epsilon) = (0.08, 0.2)

offset = 10000
length = 100000
time = 1000 

phase_axis = (2.0, 6.0)
phase_origin = (1.0, 3.0)
x_phase_label = "Strom in [mA]"
y_phase_label = "Spannung in [V]"


oszilation_axis = (20.0, 2.0)
oszilation_origin = (0.0, 1.0)
x_oszillation_label = "Zeit"
y_oszillation_label = "Spannung in [V]"


window = PlotterWindow(axis=phase_axis, origin=phase_origin, bg_color=[1.0,1.0,1.0,1])
#window = PlotterWindow(axis=oszilation_axis, origin=oszilation_origin, bg_color=[1.0,1.0,1.0,1.0])


duffing_domain = domain.DuffingDomain(active_cl_kernel, length, time, lambd, epsilon, 1, 1, (x_0, y_0), offset)
window.plotter.add_graph('duffing', graph.Line2d(duffing_domain, COLOR_KERNEL))
window.plotter.get_graph('duffing').set_colors(color_min=[0.0, 0.0, 0.0, 1.0], color_max=[0.0, 0.0, 0.0, 1.0])

axis_domain = domain.Axis(50)
#window.plotter.add_graph('start', graph.Discrete2d(axis_domain, NORMAL))


def update_uniform(self, value):
    param = self[0].args[0]
    duffing_domain.updateParameter(param, value, active_cl_kernel)

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('x_0', x_0, 0.01)
uniforms.set_global('y_0', y_0, 0.01)
#uniforms.set_global('s', start_iteration, 10)
uniforms.set_global('t', time, 10)
uniforms.set_global('length', length, 100)
uniforms.set_global('offset', offset, 100)
widget = widget.Uniforms(uniforms, update_callback=update_uniform)
widget.floating_percision = 2
window.add_widget('manipulate', widget)

window.run()





