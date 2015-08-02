from opencl.OpenCLHandler import BaseCalculator
import numpy as np

import time

# 10^7 gpuOnly=True => 0.521s
# 10^8 gpuOnly=True => failed: mem object allocation failure <-- GPU Cache gets to small
# 10^8 gpuOnly=False => failed: 4.82s <-- CPU Cache is big enough
KERNEL_SIMPLE = """__kernel void f(
            __global float2* buffer,
            __global int* result) {
  int id = get_global_id(0);

  if(buffer[id].x * buffer[id].x + buffer[id].y * buffer[id].y < 1.0f) {
    result[id] = 1;
  }else {
    result[id] = 0;
  }
}
"""


KERNEL_GROUPS = """__kernel void f(
            __global float2* buffer,
            __local int* scratch,
            __global int* result) {
  int global_id = get_global_id(0);
  int local_id = get_local_id(0);
  int local_size = get_local_size(0);


  printf(" global: %d, local: %d, size: %d", global_id, local_id, local_size);
  if(buffer[global_id].x * buffer[global_id].x + buffer[global_id].y * buffer[global_id].y < 1.0f) {
    scratch[local_id] = 1;
  }else {
    scratch[local_id] = 0;
  }

  //if(local_id == 3) {
  //  for(int i=0; i<3; i++) {
  //    result[groupid] += partial[i];
  //  }
  //  printf(" %d ", result[groupid]);
  //}

}
"""

start_time = time.time()
calculator = BaseCalculator(hidePlatformDetails=False, gpuOnly=True)
length = 8;
inputData = np.random.rand(length,2).astype('float32')
output = np.empty(length/4, dtype="int32")

#print inputData

inputBuffer = calculator.createArrayBuffer(inputData)

localMemory = calculator.createLocalMemory(4)

result = calculator.calculateSimple(KERNEL_GROUPS, [inputBuffer, localMemory], output, (8, ), (4, ))
print result
hits = np.sum(result)
print "Pi: %f " % (4*hits/float(length))
print "Calculation time: %f" % (time.time() - start_time)
