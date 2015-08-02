from calc import Calculator
import numpy as np

KERNEL = """#pragma OPENCL EXTENSION cl_khr_fp64 : enable
			__kernel void f(__global const double *r, double x, int iterations, int periods, double eps, __global double *result)
			{
				
				int gid = get_global_id(0);
				for (int i=0; i < iterations; i++) {
					x = r[gid] * x - r[gid] * x * x;
				}
				// Calculate periods more
				double x_p = x;
				for (int a=0; a < periods; a++) {
					x_p = r[gid] * x_p - r[gid] * x_p * x_p;
					printf("%d: %f %f , ", a, x_p, x);
				}
				

				//double diff = x_p - x;
				if (x_p == x) {
					result[gid] = r[gid];
				}
				else {
					result[gid] = 0;
				}
			}
			"""


app = Calculator(True)

r_values = np.arange(3.4, 3.5, 0.1, dtype="float64")



result = app.calculate(KERNEL, [app.createArrayBuffer(r_values), np.float64(0.6), np.int64(1000), np.int64(2), np.float64(2.0)], np.empty_like(r_values))

print result
print "%.155f" % np.amax(result)