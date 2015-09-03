import pyopencl as cl
import numpy as np

platforms = cl.get_platforms()
platform = platforms[0]

cpu = platform.get_devices()[0]
graka = platform.get_devices()[1]

iterations = 500000

DOUBLE_KERNEL = """
#pragma OPENCL EXTENSION cl_khr_fp64 : enable
    __kernel void f(__global double *result)
    {
    	double x = 0.2;
    	double r = 3.0;
        for(int i=0; i < %d; i += 1) {
            x = x*r*(1.0-x);
            result[i] = x;
        }
    }
""" % iterations

FLOAT_KERNEL = """
    __kernel void f(__global float *result)
    {
    	float x = 0.2f;
    	float r = 3.0f;
        for(int i=0; i < %d; i += 1) {
            x = x*r*(1.0f-x);
            result[i] = x;
        }
    }
""" % iterations

INT_KERNEL = """
    __kernel void f(__global float *result)
    {
    	float x = 20.0f; // float x = 0.2f; 
    	float r = 300.0f; //float r = 3.0f;
        for(int i=0; i < %d; i += 1) {
            x = x*r*(100.0f-x)/10000.0f;
            result[i] = x;
        }
    }
""" % iterations

zero32 = np.zeros(iterations, dtype=np.float32);
zero64 = np.zeros(iterations, dtype=np.float64);


def _buildKernel(context, kernel):
	program = cl.Program(context, kernel).build()
	queue = cl.CommandQueue(context)
	return (program, queue)

def _print_result(result):
	print "0: %0.20f" % result[0]
	count = 0;
	last = 0;
	double = True
	for pp in result:
		if last == pp and double:
			print count, "%0.20f" % pp
			double = False
		elif pp == 0:
			print count, "%0.20f" % pp
			break
		count += 1
		last = pp
	print count-1, "%0.20f" % result[count-1]


def test_graka():
	print("Device name:", graka.name)
	print("Device type:", cl.device_type.to_string(graka.type))
	print "DOUBLE: ", graka.get_info(cl.device_info.DOUBLE_FP_CONFIG)
	#print "EXTENSIONS: ", graka.get_info(cl.device_info.EXTENSIONS)
	context = cl.Context(devices=[graka])
	result_buffer = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=zero32)

	(program, queue) = _buildKernel(context, INT_KERNEL)

	program.f(queue, (1,), None, result_buffer)

	cl.enqueue_copy(queue, zero32, result_buffer)

	_print_result(zero32)

def test_cpu():
	print("Device name:", cpu.name)
	print("Device type:", cl.device_type.to_string(cpu.type))
	print "DOUBLE: ", cpu.get_info(cl.device_info.DOUBLE_FP_CONFIG)
	#print "EXTENSIONS: ", cpu.get_info(cl.device_info.EXTENSIONS)
	context = cl.Context(devices=[cpu])
	result_buffer = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=zero64)

	(program, queue) = _buildKernel(context, DOUBLE_KERNEL)

	program.f(queue, (1,), None, result_buffer)

	cl.enqueue_copy(queue, zero64, result_buffer)

	_print_result(zero64)



test_graka()
test_cpu()





