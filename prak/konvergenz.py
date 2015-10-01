import numpy 

N_POINTS = 10000
N_ITER   = 15
X0       = 0.8
A        = 0.5
f        = lambda r, x: r*x*(1-x)
EPS      = 0.00000001
DEPTH    = 8
R_MIN    = 0.0
R_MAX    = 4.0

data_f     = numpy.zeros(N_POINTS)
data_df    = numpy.zeros(N_POINTS)
tmp_data   = numpy.zeros(N_ITER) 
tmp_bifurk = numpy.zeros(DEPTH)

r_min = R_MIN
r_max = R_MAX
r_len = r_max-r_min
eps   = EPS

for j in range(0, DEPTH):
    r  = r_min
    eps *= -1
    dr = r_len/N_POINTS
    for k in range(0, N_POINTS):
        tmp_data[0] = X0
        for i in range(1, N_ITER):
            tmp_data[i] = A*(f(r, tmp_data[i-1])+tmp_data[i-1])
        data_f[k] = tmp_data[N_ITER-1]
        data_df[k] = numpy.abs((f(r,data_f[k])-f(r,data_f[k]+eps))/eps)
        if k > 0 and (data_df[k] > 1 and data_df[k-1] < 1 or data_df[k-1] > 1 and data_df[k] < 1):
            tmp_bifurk[j] = r+eps/2
            r_len /= 10
            r_min = max(r_min, tmp_bifurk[j]-r_len/2)
            r_max = min(r_max, tmp_bifurk[j]+r_len/2)
            break
        r += dr

bifurk = (tmp_bifurk[DEPTH-1]+tmp_bifurk[DEPTH-2])/2
print(bifurk)