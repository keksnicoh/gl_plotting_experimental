import pyopencl as cl
from pyopencl import array
import numpy
import time
from time import sleep

 
if __name__ == "__main__":
    #Max Graka
    size1 = 100000000

    #CPU
    size2 = 100000000

    def createRandomMatrix(size):
        matrix = numpy.zeros((1, size), numpy.float32)
        matrix[:] = numpy.random.rand(*matrix.shape)
        return matrix

    def calculate(size, devices):
        mat1 = createRandomMatrix(size)
        mat2 = createRandomMatrix(size)
    

        ## Step #1. Obtain an OpenCL platform.
        platform = cl.get_platforms()[0]
     
        ## It would be necessary to add some code to check the check the support for
        ## the necessary platform extensions with platform.extensions
        #print platform.get_devices()
        ## Step #2. Obtain a device id for at least one device (accelerator).
        device = []
        for device_id in devices:
            device.append(platform.get_devices()[device_id])
        ## It would be necessary to add some code to check the check the support for
        ## the necessary device extensions with device.extensions
         
        ## Step #3. Create a context for the selected device.
        context = cl.Context(device)
         
        ## Step #4. Create the accelerator program from source code.
        ## Step #5. Build the program.
        ## Step #6. Create one or more kernels from the program functions.
        program = cl.Program(context, """
            __kernel void matrix_dot_vector(__global const float *matrix,
            __global const float *vector, __global float *result)
            {
              int gid = get_global_id(0);
              result[gid] = matrix[gid] * matrix[gid] +  vector[gid] * vector[gid] < 1;
            }
            """).build()
         
        ## Step #7. Create a command queue for the target device.
        queue = cl.CommandQueue(context)
         
        ## Step #8. Allocate device memory and move input data from the host to the device memory.
        mem_flags = cl.mem_flags
        matrix_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=mat1)
        vector_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=mat2)
        matrix_dot_vector = numpy.zeros(size, numpy.float32)
        destination_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, matrix_dot_vector.nbytes)
         
        ## Step #9. Associate the arguments to the kernel with kernel object.
        ## Step #10. Deploy the kernel for device execution.
        program.matrix_dot_vector(queue, matrix_dot_vector.shape, None, matrix_buf, vector_buf, destination_buf)
         
        cl.enqueue_copy(queue, matrix_dot_vector, destination_buf)
    

        return numpy.sum(matrix_dot_vector)



    start_time = time.time()
    x = 0
    y = 5
    hits = 0
    while x < y:
        hits = calculate(size1, [0])
        x = x + 1
        sleep(0.1)
        print "Next"

    print "--- %f seconds total time ---" % (time.time() - start_time)

    print "Hits: %i" % hits
    print "Tries: %i" % (size1 * x)
    print "Pi: %f" % (4 * hits / size1)