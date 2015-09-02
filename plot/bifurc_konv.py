#-*- coding: utf-8 -*-
"""
@author Jesse Hinrichsen <jesse@j-apps.com>

"""


from plotting.app import PlotterWindow
from plotting import graph, domain, widget
import math, numpy
from opencl.cl_handler import BaseCalculator

BIFURC_KONV = """
#pragma OPENCL EXTENSION cl_khr_fp64 : enable
//#pragma OPENCL SELECT_ROUNDING_MODE rtn
//#define DOUBLE_SUPPORT_AVAILABLE
    __kernel void f(__global int *iterations,__global float *result)
    {
        int global_id = get_global_id(0);

        int iteration = iterations[global_id];
        double r = 3.0;
        double eps = 0.001;
        double x = 0.2;
        double new_x = 0.0;
        double nnew_x = 0.0;
        for(int i=0; i < iteration; i += 1) {
            x = r*x - r*x*x-eps;
        }
        float x_real = (float)2.0f/3.0f;
        result[2*global_id] = iteration;
        result[2*global_id+1] = x+eps/2.0;
    }
"""

BIFURC = """
//#pragma OPENCL EXTENSION cl_khr_fp64 : enable
#pragma OPENCL SELECT_ROUNDING_MODE rtn
    __kernel void f(int iterations, __global float *r_values, __global float *result)
    {
        int global_id = get_global_id(0);

        float r = r_values[global_id];

        float x = 0;
        for(int i=0; i < iterations; i += 1) {
            x = x*r*(1.0f-x);
        }

        result[2*global_id] = r;
        result[2*global_id+1] = x;
    }
"""

KERNEL = """
vec4 f(vec4 x) {
    return vec4(x.x, 2.0/3.0, 0, 0.5);
}
"""




iterations = [100*x+x%2 for x in range(0, 10000)]

iterations = numpy.array(iterations, dtype=numpy.int32)

buffer_size = len(iterations)
parallels = buffer_size

cl_kernel_params = [
    #numpy.int32(10**5)
]

r_values = numpy.arange(2.99, 3, 0.00001, dtype=numpy.float32)
buffer_size = r_values.size
parallels = buffer_size

oszilation_axis = (1000000, 0.01)
oszilation_origin = (-2.9, -0.666)
x_oszillation_label = "r"
y_oszillation_label = "x"

window = PlotterWindow(axis=oszilation_axis, origin=oszilation_origin, bg_color=[1.0,1.0,1.0,1], x_label=x_oszillation_label, y_label=y_oszillation_label)

window.plotter.set_precision_axis((0, 10))
#def logAbbildung(x, r):
#        return r*x*(1-x)
#
#x_real=2.0/3.0
#x=0.6
#r=3.0
#
#max_it = 10**7
#modul = 10**4-1
#length = int(max_it/modul)
#
#result = []
#
#for i in xrange(max_it):
#    x=logAbbildung(x, r)
#    if i % modul == 0:
#        result.append(i)
#        result.append(x)
#
#
##diff = [x_real - x for x in result]
#
#pydomain = domain.Domain(length)
#pydomain.push_data(result)

#window.plotter.add_graph('iteration', graph.Discrete2d(pydomain))
#window.plotter.get_graph('iteration').set_colors(color_min=[.0,0.0,.0,1], color_max=[0.0,.0,.0,1])
#window.plotter.get_graph('iteration').set_dotsize(0.005)


cl_domain = domain.CLDomain(BIFURC_KONV, buffer_size, cl_kernel_params, dimension=2, parallel=(parallels,))
cl_domain.append_array(iterations)
#cl_domain.append_array(r_values)
cl_domain.calculate()

xdomain = domain.Axis(100000)
window.plotter.add_graph('straight', graph.Discrete2d(xdomain, KERNEL))


window.plotter.add_graph('schwing2', graph.Discrete2d(cl_domain))
window.plotter.get_graph('schwing2').set_colors(color_min=[0.0, 0.0, 0.0, 1.0], color_max=[0.0, 0.0, 0.0, 1.0])
window.plotter.get_graph('schwing2').set_dotsize(0.004)


#window.plotter.add_graph('schwing', graph.Line2d(cl_domain_2))
#window.plotter.get_graph('schwing').set_colors(color_min=[0.0, 0.0, 0.0, 1.0], color_max=[0.0, 0.0, 0.0, 1.0])
#window.plotter.get_graph('schwing').set_dotsize(0.004)
window.plotter.gl_plot.precision_axis = (4,4)

def update_uniform(self, value):
    param = self[0].args[0]
    cl_domain.calculate_cl_buffer(param, value)

uniforms = window.plotter.get_uniform_manager()
#uniforms.set_global('V_s', V_s, 1)
#uniforms.set_global('iterations', iterations, 10)
#uniforms.set_global('it_offset', iteration_offset, 1000)
widget = widget.Uniforms(uniforms, update_callback=update_uniform)
widget.floating_percision = 1
#window.add_widget('manipulate', widget)

window.run()





