from opencl.OpenCLHandler import BaseCalculator
import numpy as np

import time

SIMPLE = """__kernel void f(
            __global float* inputArray,
            __global float* partialSums) {

	int local_id = get_local_id(0);
	int global_id = get_global_id(0);
	int group_id = get_group_id(0);

	if(local_id == 0) {
		float sum = inputArray[global_id];
		for(int i=1; i < (int)get_local_size(0); i++) {
			sum += inputArray[global_id + i];
			//printf(" %d ", inputArray[global_id + i]);
		}
		//printf(" %d ", sum);
		partialSums[group_id] = sum;
	}


}"""

BETTER = """__kernel void f(
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

EVEN_BETTER = """__kernel void f(
            __global float* inputArray,
            __local float* localMem,
            __global float* partialSums) {

	uint local_id = get_local_id(0);
	uint global_id = get_global_id(0);
	uint group_id = get_group_id(0);
	uint localsize = get_group_size(0);

	localMem[local_id] = inputArray[global_id];
	barrier(CLK_LOCAL_MEM_FENCE);
	for(uint s=localsize/2; s > 0; s /= 2) {
		

		if(local_id < s) {
			localMem[local_id] += localMem[local_id + s];
			barrier(CLK_LOCAL_MEM_FENCE);
		}
	}
	

	if(local_id == 0) {
		partialSums[group_id] = localMem[0];
	}

}"""





calculator = BaseCalculator(hidePlatformDetails=False, gpuOnly=True)

length = 2**8
print length
localsize = 8
inputData = np.random.rand(length,1).astype('float32')
inputBuffer = calculator.createArrayBuffer(inputData)
localMemory = calculator.createLocalMemory(localsize)

output = np.empty(length / localsize, dtype="float32")


start_time = time.time()
result = calculator.calculateSimple(SIMPLE, [inputBuffer], output, (length, ), (localsize, ))
print "Result: %d, Calculation time OPENCL (Simple): %f" % (np.sum(result), (time.time() - start_time))

start_time = time.time()
result = calculator.calculateSimple(BETTER, [inputBuffer, localMemory], output, (length, ), (localsize, ))
print "Result: %d, Calculation time OPENCL (Better): %f" % (np.sum(result), (time.time() - start_time))#

#start_time = time.time()
#result = calculator.calculateSimple(EVEN_BETTER, [inputBuffer, localMemory], output, (length, ), (localsize, ))
#print "Result: %d, Calculation time OPENCL (Better): %f" % (np.sum(result), (time.time() - start_time))

start_time = time.time()
result = np.sum(inputData)
print "Result: %d, Calculation time Numpy: %f" % (result, (time.time() - start_time))




