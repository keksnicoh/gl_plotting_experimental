#-*- coding: utf-8 -*-
"""
@author Jesse Hinrichsen <jesse@j-apps.com>

"""


from plotting.app import PlotterWindow
from plotting import graph, domain, widget
import math, numpy
from opencl.cl_handler import BaseCalculator

OSZILATION_KERNEL_STROM = """//#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(int iterations, int offset, float I_0, float V_0, float I_f, float V_t, float V_s, float C_f, float C_r, float R, float L, float w, float phi, __global float *result)
    {
        float time = 0.0f;
        float h = pow(10.0f, -8.0f);

        float I = I_0;
        float V_d = V_0;

        float new_I = 0.0f;

        float k_1 = 0.0f;
        float k_2 = 0.0f;
        float k_3 = 0.0f;
        float k_4 = 0.0f;

        for(int i=0; i < iterations; i += 1) {
            k_1 = h * ( V_s*cos(w*time) - V_d - R*I ) / L;
            k_2 = h * ( V_s*cos(w*(time + 0.5f*h)) - V_d - R*(I + 0.5f*k_1) ) / L;
            k_3 = h * ( V_s*cos(w*(time + 0.5f*h)) - V_d - R*(I + 0.5f*k_2) ) / L;
            k_4 = h * ( V_s*cos(w*(time + h)) - V_d - R*(I + k_3) ) / L;

            new_I = I + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;

            if( V_d > -0.6f) {
                k_1 = h * (I - I_f*(1.0f - exp(-V_d/V_t))) / (C_r/pow(rootn((1+V_d/phi),25), 11) );
                k_2 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_1)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_1)/phi),25), 11) );
                k_3 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_2)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_2)/phi),25), 11) );
                k_4 = h * (I - I_f*(1.0f - exp(-(V_d + k_3)/V_t))) / (C_r/pow(rootn((1+(V_d + k_3)/phi),25), 11) );

                V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }
            else {
                k_1 = h * (I - I_f*(1.0f - exp(-V_d/V_t))) / (C_f*exp(-V_d/V_t));
                k_2 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_1)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_1)/V_t));
                k_3 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_2)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_2)/V_t));
                k_4 = h * (I - I_f*(1.0f - exp(-(V_d + k_3)/V_t))) / (C_f*exp(-(V_d + k_3)/V_t));

                V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }


            I = new_I;
            time = time + h;

            result[2*i] = time*pow(10.0f, 5.0f);
            result[2*i+1] = I*1000;
        }

    }
"""

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

OSZILATION_KERNEL_SPANNUNG = """//#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(int iterations, int offset, float I_0, float V_0, float I_f, float V_t, float V_s, float C_f, float C_r, float R, float L, float w, float phi, __global float *result)
    {
        float time = 0.0f;
        float h = pow(10.0f, -8.0f);

        float I = I_0;
        float V_d = V_0;

        float new_I = 0.0f;

        float k_1 = 0.0f;
        float k_2 = 0.0f;
        float k_3 = 0.0f;
        float k_4 = 0.0f;

        for(int i=0; i < iterations; i += 1) {
            k_1 = h * ( V_s*cos(w*time) - V_d - R*I ) / L;
            k_2 = h * ( V_s*cos(w*(time + 0.5f*h)) - V_d - R*(I + 0.5f*k_1) ) / L;
            k_3 = h * ( V_s*cos(w*(time + 0.5f*h)) - V_d - R*(I + 0.5f*k_2) ) / L;
            k_4 = h * ( V_s*cos(w*(time + h)) - V_d - R*(I + k_3) ) / L;

            new_I = I + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;

            if( V_d > -0.6f) {
                k_1 = h * (I - I_f*(1.0f - exp(-V_d/V_t))) / (C_r/pow(rootn((1+V_d/phi),25), 11) );
                k_2 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_1)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_1)/phi),25), 11) );
                k_3 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_2)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_2)/phi),25), 11) );
                k_4 = h * (I - I_f*(1.0f - exp(-(V_d + k_3)/V_t))) / (C_r/pow(rootn((1+(V_d + k_3)/phi),25), 11) );

                V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }
            else {
                k_1 = h * (I - I_f*(1.0f - exp(-V_d/V_t))) / (C_f*exp(-V_d/V_t));
                k_2 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_1)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_1)/V_t));
                k_3 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_2)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_2)/V_t));
                k_4 = h * (I - I_f*(1.0f - exp(-(V_d + k_3)/V_t))) / (C_f*exp(-(V_d + k_3)/V_t));

                V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }

            I = new_I;
            time = time + h;

            result[2*i] = time*pow(10.0f, 5.0f);
            result[2*i+1] = V_d;

        }

    }
"""


PHASE_KERNEL_OPTIMIZED = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(int iterations, int offset, float I_0, float V_0, float I_f, float V_t, float V_s, float C_f, float C_r, float R, float L, float w, float phi, __global float *result)
    {
        float time = 0.0f;
        float h = pow(10.0f, -8.0f);

        float I = I_0;
        float V_d = V_0;

        float k_1 = 0.0f;
        float k_2 = 0.0f;
        float k_3 = 0.0f;
        float k_4 = 0.0f;

        float l_1 = 0.0f;
        float l_2 = 0.0f;
        float l_3 = 0.0f;
        float l_4 = 0.0f;

        for(int i=0; i < iterations + offset; i += 1) {

            if( V_d > -0.6f) {
                l_1 = h * ( V_s*cos(w*time) - V_d - R*I ) / L;
                k_1 = h * (I - I_f*(1.0f -exp(-V_d/V_t))) / (C_r/pow(rootn((1+V_d/phi),25), 11) );

                l_2 = h * ( V_s*cos(w*(time + 0.5f*h)) - (V_d+0.5f*k_1) - R*(I + 0.5f*l_1) ) / L;
                k_2 = h * ((I+0.5f*l_1) - I_f*(1.0f -exp(-(V_d + 0.5f*k_1)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_1)/phi),25), 11) );

                l_3 = h * ( V_s*cos(w*(time + 0.5f*h)) - (V_d+0.5f*k_2) - R*(I + 0.5f*l_2) ) / L;
                k_3 = h * ((I+0.5f*l_2) - I_f*(1.0f -exp(-(V_d + 0.5f*k_2)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_2)/phi),25), 11) );


                l_4 = h * ( V_s*cos(w*(time + h)) - (V_d+k_3) - R*(I + l_3) ) / L;
                k_4 = h * ((I+l_3) - I_f*(1.0f -exp(-(V_d + k_3)/V_t))) / (C_r/pow(rootn((1+(V_d + k_3)/phi),25), 11) );


                I = I + (l_1 + 2*l_2 + 2*l_3 + l_4) / 6.0f;
                V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }
            else {
                l_1 = h * ( V_s*cos(w*time) - V_d - R*I ) / L;
                k_1 = h * (I - I_f*(1.0f - exp(-V_d/V_t))) / (C_f*exp(-V_d/V_t));

                l_2 = h * ( V_s*cos(w*(time + 0.5f*h)) - (V_d+0.5f*k_1) - R*(I + 0.5f*l_1) ) / L;
                k_2 = h * ((I+0.5f*l_1) - I_f*(1.0f - exp(-(V_d + 0.5f*k_1)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_1)/V_t));

                l_3 = h * ( V_s*cos(w*(time + 0.5f*h)) - (V_d+0.5f*k_2) - R*(I + 0.5f*l_2) ) / L;
                k_3 = h * ((I+0.5f*l_2) - I_f*(1.0f - exp(-(V_d + 0.5f*k_2)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_2)/V_t));
                
                l_4 = h * ( V_s*cos(w*(time + h)) - (V_d+k_3) - R*(I + l_3) ) / L;
                k_4 = h * ((I+l_3) - I_f*(1.0f - exp(-(V_d + k_3)/V_t))) / (C_f*exp(-(V_d + k_3)/V_t));


                I = I + (l_1 + 2*l_2 + 2*l_3 + l_4) / 6.0f;
                V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }


            time = time + h;

            if(i > offset) {
                result[2*(i-offset)] = I*1000;
                result[2*(i-offset)+1] = V_d;
            }
        }

    }
"""

OSZILATION_KERNEL_BIFURC = """//#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(int iterations, int offset, float I_0, float V_0, float I_f, float V_t, float V_s, float C_f, float C_r, float R, float L, float w, float phi, __global float *inital,__global float *result)
    {
        float time = 0.0f;
        float h = pow(10.0f, -8.0f);

        float I = I_0;
        float V_d = V_0;

        float new_I = 0.0f;

        float k_1 = 0.0f;
        float k_2 = 0.0f;
        float k_3 = 0.0f;
        float k_4 = 0.0f;

        int piek_index = 0;
        int piek_count = 5;

        float piek_data[piek_count];
        //float last_piek = 0.0f;

        float diff = 0.0f;
        float last_i_diff = 0.0f;

        int global_id = get_global_id(0);
        V_s = inital[global_id];

        for(int i=0; i < iterations; i += 1) {
            k_1 = h * ( V_s*cos(w*time) - V_d - R*I ) / L;
            k_2 = h * ( V_s*cos(w*(time + 0.5f*h)) - V_d - R*(I + 0.5f*k_1) ) / L;
            k_3 = h * ( V_s*cos(w*(time + 0.5f*h)) - V_d - R*(I + 0.5f*k_2) ) / L;
            k_4 = h * ( V_s*cos(w*(time + h)) - V_d - R*(I + k_3) ) / L;

            new_I = I + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;

            if( V_d > -0.6f) {
                k_1 = h * (I - I_f*(1.0f - exp(-V_d/V_t))) / (C_r/pow(rootn((1+V_d/phi),25), 11) );
                k_2 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_1)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_1)/phi),25), 11) );
                k_3 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_2)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_2)/phi),25), 11) );
                k_4 = h * (I - I_f*(1.0f - exp(-(V_d + k_3)/V_t))) / (C_r/pow(rootn((1+(V_d + k_3)/phi),25), 11) );

                V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }
            else {
                k_1 = h * (I - I_f*(1.0f - exp(-V_d/V_t))) / (C_f*exp(-V_d/V_t));
                k_2 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_1)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_1)/V_t));
                k_3 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_2)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_2)/V_t));
                k_4 = h * (I - I_f*(1.0f - exp(-(V_d + k_3)/V_t))) / (C_f*exp(-(V_d + k_3)/V_t));

                V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }


            diff = new_I - I;
            if(diff * last_i_diff < 0.0f) {
                //last_piek = I;
                piek_data[piek_index] = I;
                piek_index += 1;
                if(piek_index > piek_count) {
                    piek_index = 0;
                }
            }

            last_i_diff = diff;

            I = new_I;
            time = time + h;

        }

            result[10*global_id] = V_s;
            result[10*global_id+1] = piek_data[0]*1000.0f;

            result[10*global_id+2] = V_s;
            result[10*global_id+1+2] = piek_data[1]*1000.0f;

            result[10*global_id+4] = V_s;
            result[10*global_id+1+4] = piek_data[2]*1000.0f;

            result[10*global_id+6] = V_s;
            result[10*global_id+1+6] = piek_data[3]*1000.0f;

            result[10*global_id+8] = V_s;
            result[10*global_id+1+8] = piek_data[4]*1000.0f;
    }
"""

OSZILATION_KERNEL_BIFURC_SPANNUNG = """//#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(int iterations, int offset, float I_0, float V_0, float I_f, float V_t, float V_s, float C_f, float C_r, float R, float L, float w, float phi, __global float *inital,__global float *result)
    {
        float time = 0.0f;
        float h = pow(10.0f, -8.0f);

        float I = I_0;
        float V_d = V_0;

        float new_I = 0.0f;
        float new_V_d = 0.0f;

        float k_1 = 0.0f;
        float k_2 = 0.0f;
        float k_3 = 0.0f;
        float k_4 = 0.0f;

        int piek_index = 0;
        int piek_count = 5;

        float piek_data[piek_count];
        //float last_piek = 0.0f;

        float diff = 0.0f;
        float last_i_diff = 0.0f;

        int global_id = get_global_id(0);
        V_s = inital[global_id];

        for(int i=0; i < iterations; i += 1) {
            k_1 = h * ( V_s*cos(w*time) - V_d - R*I ) / L;
            k_2 = h * ( V_s*cos(w*(time + 0.5f*h)) - V_d - R*(I + 0.5f*k_1) ) / L;
            k_3 = h * ( V_s*cos(w*(time + 0.5f*h)) - V_d - R*(I + 0.5f*k_2) ) / L;
            k_4 = h * ( V_s*cos(w*(time + h)) - V_d - R*(I + k_3) ) / L;

            new_I = I + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;

            if( V_d > -0.6f) {
                k_1 = h * (I - I_f*(1.0f - exp(-V_d/V_t))) / (C_r/pow(rootn((1+V_d/phi),25), 11) );
                k_2 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_1)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_1)/phi),25), 11) );
                k_3 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_2)/V_t))) / (C_r/pow(rootn((1+(V_d + 0.5f*k_2)/phi),25), 11) );
                k_4 = h * (I - I_f*(1.0f - exp(-(V_d + k_3)/V_t))) / (C_r/pow(rootn((1+(V_d + k_3)/phi),25), 11) );

                new_V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }
            else {
                k_1 = h * (I - I_f*(1.0f - exp(-V_d/V_t))) / (C_f*exp(-V_d/V_t));
                k_2 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_1)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_1)/V_t));
                k_3 = h * (I - I_f*(1.0f - exp(-(V_d + 0.5f*k_2)/V_t))) / (C_f*exp(-(V_d + 0.5f*k_2)/V_t));
                k_4 = h * (I - I_f*(1.0f - exp(-(V_d + k_3)/V_t))) / (C_f*exp(-(V_d + k_3)/V_t));

                new_V_d = V_d + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6.0f;
            }


            diff = new_V_d - V_d;
            if(diff * last_i_diff < 0.0f) {
                piek_data[piek_index] = V_d;
                piek_index += 1;
                if(piek_index > piek_count) {
                    piek_index = 0;
                }
            }

            last_i_diff = diff;

            I = new_I;
            V_d = new_V_d;
            time = time + h;

        }

            result[10*global_id] = V_s;
            result[10*global_id+1] = piek_data[0];

            result[10*global_id+2] = V_s;
            result[10*global_id+1+2] = piek_data[1];

            result[10*global_id+4] = V_s;
            result[10*global_id+1+4] = piek_data[2];

            result[10*global_id+6] = V_s;
            result[10*global_id+1+6] = piek_data[3];

            result[10*global_id+8] = V_s;
            result[10*global_id+1+8] = piek_data[4];
    }
"""

R = 100 # Ohm
L = 2367*10**-6 # H

C_r = 82*10**-12 #F
C_f = 56*10**-18 #F

I_f = 2.8*10**-12 #A

phi = 0.6


V_s = 4.62 #V

V_t = 0.034 #V

w = 1.0 / math.sqrt(L*C_r)
print w

V_d = 0.0
I = 0.0

V_s_values = numpy.arange(6.3, 6.4, 0.001, dtype=numpy.float32)
parallels = V_s_values.size


iterations = 300000
iteration_offset = 0
#h = 10**-8
#time = 0.0

buffer_size = parallels*5

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
    numpy.float32(phi),
]

active_cl_kernel = OSZILATION_KERNEL_BIFURC
#active_cl_kernel = OSZILATION_KERNEL_STROM
#active_cl_kernel = PHASE_KERNEL_OPTIMIZED


phase_axis = (2.0, 6.0)
phase_origin = (1.0, 3.0)
x_phase_label = "Strom in [mA]"
y_phase_label = "Spannung in [V]"


oszilation_axis = (2.0, 2.0)
oszilation_origin = (0.0, 1.0)
x_oszillation_label = "Eingangsspannung V_s in [V]"
y_oszillation_label = "Strompieks I in [mA]"

window = PlotterWindow(axis=oszilation_axis, origin=oszilation_origin, bg_color=[1.0,1.0,1.0,1], x_label=x_oszillation_label, y_label=y_oszillation_label)

#window = PlotterWindow(axis=phase_axis, origin=phase_origin, bg_color=[1.0,1.0,1.0,1], x_label=x_phase_label, y_label=y_phase_label)

cl_domain = domain.CLDomain(active_cl_kernel, buffer_size, cl_kernel_params, dimension=2, parallel=(parallels,))
cl_domain.append_array(V_s_values)
cl_domain.calculate()
#cl_domain_2 = domain.CLDomain(OSZILATION_KERNEL_STROM, iterations, cl_kernel_params, dimension=2)
#domain = domain.Domain(gl_buffer_length)
#domain.push_data(data)

window.plotter.add_graph('schwing2', graph.Discrete2d(cl_domain))
window.plotter.get_graph('schwing2').set_colors(color_min=[0.0, 0.0, 0.0, 1.0], color_max=[0.0, 0.0, 0.0, 1.0])
window.plotter.get_graph('schwing2').set_dotsize(0.002)


#window.plotter.add_graph('schwing', graph.Line2d(cl_domain_2))
#window.plotter.get_graph('schwing').set_colors(color_min=[0.0, 0.0, 0.0, 1.0], color_max=[0.0, 0.0, 0.0, 1.0])
#window.plotter.get_graph('schwing').set_dotsize(0.004)
window.plotter.gl_plot.precision_axis = (1,1)

def update_uniform(self, value):
    param = self[0].args[0]
    cl_domain.calculate_cl_buffer(param, value)

uniforms = window.plotter.get_uniform_manager()
uniforms.set_global('V_s', V_s, 1)
#uniforms.set_global('iterations', iterations, 10)
#uniforms.set_global('it_offset', iteration_offset, 1000)
widget = widget.Uniforms(uniforms, update_callback=update_uniform)
widget.floating_percision = 1
#window.add_widget('manipulate', widget)

window.run()





