from opencl.OpenCLHandler import BaseCalculator
import numpy as np

import time

# Idea: The whole Matrix is in 1 array: For example 3x3 Matrix = 9 components array
# 3x3: 
MAT_3_X_3 = """__kernel void f(
            __global float* inputArray,
            __local float* cache,
            __global float* result) {

	int size = 3;
	int global_id = get_global_id(0); 
	//int local_id = get_local_id(0));
	int index = 0;
	int row = 2;
	int col = 1;
	for(int i=size; i < size*size; i++) {
		if (col != global_id + 1) {
			cache[index] = inputArray[i];
			//printf("Value: %f ", cache[index]);
			index++;
		}

		col++;
		if (col > size){
			col = 1;
			row++;
		}
	}
	
	float partDet = inputArray[global_id]*(cache[0]*cache[3]-cache[1]*cache[2]);
	//printf("Value: %f ", partDet);

	result[global_id] = partDet;
	barrier(CLK_GLOBAL_MEM_FENCE);
	
	result[0] = result[0] - result[1] + result[2];

}"""




calculator = BaseCalculator(hidePlatformDetails=False, gpuOnly=True)

inputData = np.array([[5.0,2.0,3.0],[4.0,5.3,6.0],[10.0,8.0,9.0]], dtype="float32")
inputBuffer = calculator.createArrayBuffer(inputData)
cache = calculator.createLocalMemory(4)

output = np.empty(1, dtype="float32")


start_time = time.time()
result = calculator.calculateSimple(MAT_3_X_3, [inputBuffer, cache], output, (3, ), (1, ))
print "Result: %d, Calculation time OPENCL (Simple): %f" % (result, (time.time() - start_time))

start_time = time.time()
result = np.linalg.det(inputData);
print "Result: %d, Calculation time Numpy: %f" % (result, (time.time() - start_time))





