"""
Strategy to calculate Feigenbaumkonstante based on Lyapunovexponent
1. Periodenverdopplung occurs when Lyapunovexponent equal 0
2. 
"""

from opencl.OpenCLHandler import BaseCalculator
import numpy as np

import time

KERNEL_SIN = """
__kernel void f(__global float* r, float x_0, int n, int start_sum, __global float *result){
	int global_id = get_global_id(0);

    float summe = x_0;
    for (int i = 1; i < n - 1; i+=1) {
        x_0 = r[global_id]*sin(x_0);

        if (i > start_sum) {
            summe += log(fabs(r[global_id]*cos(x_0)));
        }

    }
    float eps = 0.01f;
    float res = summe/n;
    if(fabs(res) < eps) {
        result[global_id] = r[global_id];
    //printf(" %f ", res);
    
    }
    else {
        result[global_id] = 10.0f;
    }
}
"""

KERNEL_LOG = """
static float g(float l, float x){
        return l * x * (1-x);
    }

__kernel void f(__global float* r, float x_0, int n, int start_sum, float epss, __global float *result){
    int global_id = get_global_id(0);

    float summe = x_0;
    float eps = 0.000001f;
    for (int i = 1; i < n - 1; i+=1) {
        x_0 = g(r[global_id], x_0);

        if (i > start_sum) {
            summe += log(fabs(g(r[global_id], x_0+eps)-g(r[global_id], x_0))/eps);
        }

    }
    float res = summe/n;
    if(fabs(res) < epss) {
        result[global_id] = r[global_id];
    }
    else {
        result[global_id] = 0.0f;
    }
}
"""

#print len(output.shape), len(output)

calculator = BaseCalculator(hidePlatformDetails=True, gpuOnly=True)

size = 30000.0
start = 3.4
end = 3.5
steps = (end-start) / size

output = np.zeros(size, dtype=np.float32)
data = np.arange(start, end, steps,dtype=np.float32)
if len(data) != len(output):
    raise RuntimeError("Invalid data sizes")


inputData = calculator.createArrayBuffer(data)


result = calculator.calculateSimple(KERNEL_LOG, [inputData, np.float32(0.1), np.int32(1500), np.int32(800), np.float32(0.00005)], output, globalsize=(int(size),))


sections = []

section_start = 0.0
section_end = 0.0
for i in range(0, len(result)):
    r = result[i]
    if r != 0.0:
        if section_start == 0.0:
            section_start = r

    elif section_start != 0.0:
        sections.append((section_start, result[i-1]))
        section_start = 0.0

print "Got %d sections" % len(sections)
periods = 2
for section in sections:
    print "Periode: %d at %.15f" % (periods, section[0] + (section[1] - section[0]) / 2.0)
    periods *= 2

#for section in sections:
#    if section[0] != section[1]:
#        steps = (section[1]-section[0]) / size
#        data = np.arange(section[0], section[1], steps,dtype=np.float32)
#        inputData = calculator.createArrayBuffer(data)
#        result = calculator.calculateSimple(KERNEL_LOG, [inputData, np.float32(0.1), np.int32(500), np.int32(200), np.float32(0.002)], output, globalsize=(int(size),))
#
#        print result
#        break

#newData = []
#for i in range(0, int(size)):
#    if result[i] != 10.0:





