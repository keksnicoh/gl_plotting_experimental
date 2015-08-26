#-*- coding: utf-8 -*-
"""
@author Jesse Hinrichsen <jesse@j-apps.com>

"""

"""
Phasendiagramm screenshoots sind mit
h = pow(10.0f, -9.0f);
500.000 iterationen
Ab der 100.000 iteration gezeichnet

"""

"""
Oszillationen screenshoots sind mit
h = pow(10.0f, -9.0f);
100.000 iterationen

"""

from plotting.app import PlotterWindow
from plotting import graph, domain, widget
import math, numpy
#from prototyping.schwing import * 

OSZILATION_KERNEL = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(int iterations, int offset, float I_0, float V_0, float I_f, float V_t, float V_s, float C_f, float C_r, float R, float L, float w, float phi, __global float *result)
    {
        float time = 0.0f;
        float h = pow(10.0f, -9.0f);

        float I = I_0;
        float V_d = V_0;

        float theta = 0.0f;
        float new_I = 0.0f;
        float _exp = 0.0f;

        for(int i=0; i < iterations; i += 1) {
            time = time + h;
            theta = w*time;

            new_I = I + h * ( V_s*cos(theta) - V_d - R*I ) / L;

            _exp = exp(-V_d/V_t);
            if( V_d > -0.6f) {
                V_d = V_d + h * (I - I_f*(1.0f -_exp)) / (C_r*pow((1+V_d/phi),-0.44f) );
            }
            else {
                V_d = V_d + h * (I - I_f*(1.0f - _exp)) / (C_f*_exp);
            }


            I = new_I;

            result[2*i] = time*pow(10.0f, 5.0f);
            result[2*i+1] = V_d;//I*1000;
        }

    }
"""

PHASE_KERNEL = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(int iterations, int offset, float I_0, float V_0, float I_f, float V_t, float V_s, float C_f, float C_r, float R, float L, float w, float phi, __global float *result)
    {
        float time = 0.0f;
        float h = pow(10.0f, -9.0f);

        float I = I_0;
        float V_d = V_0;

        float theta = 0.0f;
        float new_I = 0.0f;
        float _exp = 0.0f;

        for(int i=0; i < iterations + offset; i += 1) {
            time = time + h;
            theta = w*time;

            new_I = I + h * ( V_s*cos(theta) - V_d - R*I ) / L;

            _exp = exp(-V_d/V_t);
            if( V_d > -0.6f) {
                V_d = V_d + h * (I - I_f*(1.0f -_exp)) / (C_r*pow((1+V_d/phi),-0.44f) );
            }
            else {
                V_d = V_d + h * (I - I_f*(1.0f - _exp)) / (C_f*_exp);
            }


            I = new_I;

            if(i > offset) {
                result[2*(i-offset)] = I*1000;
                result[2*(i-offset)+1] = V_d;
            }
        }

    }
"""

POINCARE = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(int iterations, int offset, float I_0, float V_0, float I_f, float V_t, float V_s, float C_f, float C_r, float R, float L, float w, float phi, __global float *result)
    {
        float time = 0.0f;
        float h = pow(10.0f, -9.0f);

        float I = I_0;
        float V_d = V_0;

        float theta = 0.0f;
        float new_I = 0.0f;
        float _exp = 0.0f;
        float last_point = 0.0f;
        float position = 0.0f;

        int k = 0;
        int i = 0;
        while(k < iterations) {
            time = time + h;
            theta = w*time;

            new_I = I + h * ( V_s*cos(theta) - V_d - R*I ) / L;

            _exp = exp(-V_d/V_t);
            if( V_d > -0.6f) {
                V_d = V_d + h * (I - I_f*(1.0f -_exp)) / (C_r*pow((1+V_d/phi),-0.44f) );
            }
            else {
                V_d = V_d + h * (I - I_f*(1.0f - _exp)) / (C_f*_exp);
            }


            I = new_I;

            position = sin(theta);
            if(i > offset && last_point*position < 0.0f) {
                result[2*k] = I*1000;
                result[2*k+1] = V_d;
                k += 1;
            }

            last_point = position;
            i += 1;
        }

    }
"""

R = 100 # Ohm
L = 2367*10**-6 # H

C_r = 82*10**-12 #F
C_f = 56*10**-18 #F

I_f = 2.8*10**-12 #A

phi = 0.6

V_s = 2.0 #V
V_t = 0.034 #V

w = 1.0 / math.sqrt(L*C_r)

V_d = 0.0
I = 0.0


iterations = 1500
iteration_offset = 10000
#h = 10**-8
#time = 0.0

cl_kernel_params = [
    numpy.int32(iterations),
    numpy.int32(iteration_offset),
    numpy.float32(I), 
    numpy.float32(V_d),

    numpy.float32(I_f),

    numpy.float32(V_t),
    numpy.float32(V_s),

    numpy.float32(C_f),
    numpy.float32(C_r),

    numpy.float32(R),
    numpy.float32(L),

    numpy.float32(w),
    numpy.float32(phi)
]


active_cl_kernel = PHASE_KERNEL


phase_axis = (2.0, 6.0)
phase_origin = (1.0, 3.0)
x_phase_label = "Strom in [mA]"
y_phase_label = "Spannung in [V]"


oszilation_axis = (2.0, 2.0)
oszilation_origin = (0.0, 1.0)
x_oszillation_label = "Zeit"
y_oszillation_label = "Spannung in [V]"

#window = PlotterWindow(axis=oszilation_axis, origin=oszilation_origin, bg_color=[.9,.9,.9,1], x_label=x_oszillation_label, y_label=y_oszillation_label)

window = PlotterWindow(axis=phase_axis, origin=phase_origin, bg_color=[.9,.9,.9,1], x_label=x_phase_label, y_label=y_phase_label)

cl_domain = domain.CLDomain(active_cl_kernel, iterations, cl_kernel_params, dimension=2)
#domain = domain.Domain(gl_buffer_length)
#domain.push_data(data)


window.plotter.add_graph('schwing', graph.Discrete2d(cl_domain))
window.plotter.get_graph('schwing').set_colors(color_min=[0.0, 0.0, 0.0, 1.0], color_max=[0.0, 0.0, 0.0, 1.0])
window.plotter.get_graph('schwing').set_dotsize(0.004)
window.plotter.gl_plot.precision_axis = (1,1)

def update_uniform(self, value):
    param = self[0].args[0]
    cl_domain.calculate_cl_buffer(param, value)

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('V_s', V_s, 1.0)
#uniforms.set_global('it_offset', iteration_offset, 1000)
widget = widget.Uniforms(uniforms, update_callback=update_uniform)
widget.floating_percision = 1
window.add_widget('manipulate', widget)

window.run()





