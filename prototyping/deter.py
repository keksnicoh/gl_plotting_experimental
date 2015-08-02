from opencl.OpenCLHandler import BaseCalculator
import numpy as np

import time

SIMPLE = """__kernel void f(
            __global float3* inputArray,
            __global float* partialSums) {

	int local_id = get_local_id(0);
	int global_id = get_global_id(0);
	int group_id = get_group_id(0);


}"""




calculator = BaseCalculator(hidePlatformDetails=False, gpuOnly=True)

length = 9
print length
localsize = 3
inputData = np.array([[0,3,1], [1,2,1], [2,1,0]], dtype='float32')
inputBuffer = calculator.createArrayBuffer(inputData)
localMemory = calculator.createLocalMemory(localsize)

output = np.empty(1, dtype="float32")


start_time = time.time()
result = calculator.calculateSimple(SIMPLE, [inputBuffer], output, (length, ), (localsize, ))
print "Result: %d, Calculation time OPENCL (Simple): %f" % (np.sum(result), (time.time() - start_time))




