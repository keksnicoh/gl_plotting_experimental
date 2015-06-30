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
            theta = i / (2.0 * iterations) * time * omega;
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
            theta = i / (2.0 * iterations) * time * omega;
            result[i] = (i / convert_float(iterations)) * time;
            result[i+1] = result[i-1] + h * y;
            y = y + h * (epsilon * cos(theta) - lambda * y - beta * result[i-1] * result[i-1] * result[i-1]);

        }
    }
"""

window = PlotterWindow(axis=(10.0,10.0), origin=(5.0,5.0))
duffing_domain = domain.DuffingDomain(OSZILATION_KERNEL, 50000, 60, 0.08, 1, 1, 1, (3,4))
window.plotter.add_graph('duffing', graph.Discrete2d(duffing_domain))
window.run()
