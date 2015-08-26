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
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, int start_iteration, __global float *dummy, __global float *result)
    {
        float h = time / convert_float(iterations);
        float theta = 0;
        float t = 0;

        dummy[0] = awp.x;
        dummy[1] = awp.y;
        dummy[2] = 0.0f;

        result[0] = awp.x;
        result[1] = awp.y;
        result[2] = 0.0f;
        for(int i=3; i < iterations*3; i += 3) {
            t = i / (3.0f * iterations) * time;
            theta = t * omega;
            dummy[i] = dummy[i-3] + h * dummy[i-2];
            dummy[i+1] = dummy[i-2] + h * (epsilon * cos(theta) - lambda * dummy[i-2] - beta * dummy[i-3] * dummy[i-3] * dummy[i-3]);
            dummy[i+2] = i/(iterations*3);
            //if(i > start_iteration) {
                result[i] = dummy[i];
                result[i+1] = dummy[i+1];
                result[i+2] = dummy[i+2];
            //}

            if(t < 50.0f) {
                result[i+2] = 1.0f;
            }
        }

    }
"""

"""
Kernel to calculate duffing equation and writes (t, x) data to given GLBuffer
"""
OSZILATION_KERNEL = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, int start_iteration, __global float *dummy, __global float *result)
    {
        float h = time / convert_float(iterations);
        float t = 0.0;
        float theta = 0;
        result[0] = 0.0;
        result[1] = awp.x;
        result[2] = 0.0f;
        float y = awp.y;
        for(int i=3; i < iterations*3; i += 3) {
            t = i / (3.0f*iterations) * time;
            theta = t * omega;
            result[i] = t;
            result[i+1] = result[i-2] + h * y;
            y = y + h * (epsilon * cos(theta) - lambda * y - beta * result[i-2] * result[i-2] * result[i-2]);
            result[i+2] = 0.0f;
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
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, int start_iteration, __global float *dummy, __global float *result)
    {
        float h = time / convert_float(iterations);
        float theta = 0;
        result[0] = 0.0;
        result[1] = awp.x;
        result[2] = 0.0f;

        dummy[0] = 0.0;
        dummy[1] = awp.x;
        dummy[2] = 0.0f;

        float y = awp.y;
        float k1;
        float k2;
        float k3;
        float k4;
        for(int i=3; i < iterations*3; i += 3) {
            t = i / (3.0f*iterations) * time;
            theta = i / (3.0f * iterations) * time * omega;
            k1 = h * y;
            k2 = h * (y + k1/2.0f);
            k3 = h * (y + k2/2.0f);
            k4 = h * (y + k3);
            dummy[i] = t;
            dummy[i+1] = dummy[i-2] + (k1 + 2*k2 + 2*k3 + k4)/6.0f;
            dummy[i+2] = 0.0f;
            y = y + h * (epsilon * cos(theta) - lambda * y - beta * dummy[i-2] * dummy[i-2] * dummy[i-2]);

            if(i > start_iteration) {
                result[i] = dummy[i];
                result[i+1] = dummy[i+1];
                result[i+2] = dummy[i+2];
            }
            else {
                result[i] = 0.0f;
                result[i+1] = 0.0f;
                result[i+2] = 0.0f;
            }
        }
    }
"""

PHASE_KERNEL_RK = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, int start_iteration, __global float *dummy, __global float *result)
    {
        float h = time / convert_float(iterations);
        float t = 0;
        float theta = 0;
        result[0] = awp.x;
        result[1] = awp.y;
        result[2] = 0.0f;

        dummy[0] = awp.x;
        dummy[1] = awp.y;
        dummy[2] = 0.0f;

        float k1;
        float k2;
        float k3;
        float k4;
        for(int i=3; i < iterations*3; i += 3) {
            t = i / (3.0f * iterations) * time;
            theta = t * omega;
            k1 = h * dummy[i-2];
            k2 = h * (dummy[i-2] + k1/2.0f);
            k3 = h * (dummy[i-2] + k2/2.0f);
            k4 = h * (dummy[i-2] + k3);
            dummy[i] = dummy[i-3] + (k1 + 2*k2 + 2*k3 + k4)/6.0f;
            dummy[i+1] = dummy[i-2] + h * (epsilon * cos(theta) - lambda * dummy[i-2] - beta * dummy[i-3] * dummy[i-3] * dummy[i-3]);
            dummy[i+2] = i/(iterations*3);

            

            if(i > start_iteration) {
                result[i] = dummy[i];
                result[i+1] = dummy[i+1];
                result[i+2] = dummy[i+2];
            }
            else {
                result[i] = 0.0f;
                result[i+1] = 0.0f;
                //result[i+2] = 0.0f;
            }

            if(t < 50.0f) {
                result[i+2] = 1.0f;
            }
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

#(x_0, y_0) = (0.21, 0.02) #small
#(x_0, y_0) = (1.05, 0.77) #gone
#(x_0, y_0) = (-0.67, 0.02) #small
#(x_0, y_0) = (-0.46, 0.30) #big
#(x_0, y_0) = (-0.43, 0.12) #small
(x_0, y_0) = (0.0,0.0)

(lambd, epsilon) = (0.2, 0.0)
(lambd, epsilon) = (0.2, 1.0)
(lambd, epsilon) = (0.2, 7.72)

start_iteration = 0
length = 10000
time = 100

active_cl_kernel = PHASE_KERNEL

phase_axis = (1.4, 1.2)
phase_origin = (0.8, 0.6)

oszilation_axis = (70.0, 8.0)
oszilation_origin = (0.0, 4.0)


window = PlotterWindow(axis=phase_axis, origin=phase_origin, bg_color=[.0,.0,.0,1])
duffing_domain = domain.DuffingDomain(active_cl_kernel, length, time, lambd, epsilon, 1, 1, (x_0, y_0), start_iteration)
duffing_domain.dimension = 3
window.plotter.add_graph('duffing', graph.Line2d(duffing_domain, COLOR_KERNEL))
window.plotter.get_graph('duffing').set_colors(color_min=[1.0, 0.0, 0.0, 1.0], color_max=[0.0, 1.0, 0.0, 1.0])

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
uniforms.set_global('length', length, 10)
widget = widget.Uniforms(uniforms, update_callback=update_uniform)
widget.floating_percision = 2
window.add_widget('manipulate', widget)

window.run()





