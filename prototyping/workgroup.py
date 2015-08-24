from opencl.OpenCLHandler import BaseCalculator
import numpy as np

import time

KERNEL = """__kernel void f(
            __global float* inputArray,
            __local float* localMem,
            __global float* partialSums) {

	int local_id = get_local_id(0);
	int global_id = get_global_id(0);
	int group_id = get_group_id(0);

	localMem[local_id] = inputArray[global_id];
	barrier(CLK_LOCAL_MEM_FENCE);

	if(local_id == 0) {
		float sum = localMem[0];
		for(int i=1; i < (int)get_local_size(0); i++) {
			sum += localMem[i];
		}
		partialSums[group_id] = sum;
	}

}"""




calculator = BaseCalculator(hidePlatformDetails=False, gpuOnly=True)

length = 2**14
print length
localsize = 256
inputData = np.random.rand(length,1).astype('float32')
inputBuffer = calculator.createArrayBuffer(inputData)
localMemory = calculator.createLocalMemory(localsize)

output = np.empty(length / localsize, dtype="float32")


start_time = time.time()
result = calculator.calculateSimple(KERNEL, [inputBuffer, localMemory], output, (length,), (localsize,))
print "Result: %d, Calculation time OPENCL (Simple): %f" % (np.sum(result), (time.time() - start_time))





