#-*- coding: utf-8 -*-
"""
OpenCL implementation for domain calculation on Duffing equation
@author Jesse Hinrichsen <jesse@j-apps.com>
"""

from plotting.app import PlotterWindow
from plotting import graph, domain
import math
import numpy as np

"""
Kernel to calculate duffing equation and writes (x, y) data to given GLBuffer
"""
PHASE_KERNEL = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, __global float *result)
    {

        float h = time / convert_float(iterations);
        float theta = 0;
        result[0] = awp.x;
        result[1] = awp.y;
        for(int i=2; i < iterations; i += 2) {
            theta = i / (2.0f * iterations) * time * omega;
            result[i] = result[i-2] + h * result[i-1];
            result[i+1] = result[i-1] + h * (epsilon * cos(theta) - lambda * result[i-1] - beta * result[i-2] * result[i-2] * result[i-2]);
        }
    }
"""

"""
Kernel to calculate duffing equation and writes (t, x) data to given GLBuffer
"""
OSZILATION_KERNEL = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, __global float *result)
    {
        float h = time / convert_float(iterations);
        float theta = 0;
        result[0] = 0.0;
        result[1] = awp.x;
        float y = awp.y;
        for(int i=2; i < iterations; i += 2) {
            theta = i / (2.0f * iterations) * time * omega;
            result[i] = (i / convert_float(iterations)) * time;
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
    __kernel void f(float2 awp, int iterations, int time, float lambda, float beta, float omega, float epsilon, __global float *result)
    {
        float h = time / convert_float(iterations);
        float theta = 0;
        result[0] = 0.0;
        result[1] = awp.x;
        float y = awp.y;
        float k1;
        float k2;
        float k3;
        float k4;
        for(int i=2; i < iterations; i += 2) {
            theta = i / (2.0f * iterations) * time * omega;
            k1 = h * y;
            k2 = h * (y + k1/2.0f);
            k3 = h * (y + k2/2.0f);
            k4 = h * (y + k3);
            result[i] = (i / convert_float(iterations)) * time;
            result[i+1] = result[i-1] + (k1 + 2*k2 + 2*k3 + k4)/6.0f;
            y = y + h * (epsilon * cos(theta) - lambda * y - beta * result[i-1] * result[i-1] * result[i-1]);
        }
    }
"""

COLORIZE_ME = """
vec4 f(vec4 p) {

    return vec4(p.xy, 1- gl_VertexID/100000, 1);
}
"""

window = PlotterWindow(axis=(10.0,10.0), origin=(5.0,5.0))
duffing_domain = domain.DuffingDomain(PHASE_KERNEL, 500000, 300, 0.04, 1, 1, 1, (1,1))
window.plotter.add_graph('duffing', graph.Line2d(duffing_domain, COLORIZE_ME))
window.plotter.get_graph('duffing').set_colors(color_min=[.0,0.0,.0,1], color_max=[1.0,0,0,1])

window.run()
