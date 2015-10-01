import numpy 

N_POINTS = 15
N_ITER   = 10
X0       = 0.8
A        = 0.5
f        = lambda r, x: r*x*(1-x)
EPS      = 0.00000001
DEPTH    = 8
R_MIN    = 0.5
R_MAX    = 4.0

data_f     = []
data_df    = numpy.zeros(N_POINTS)
tmp_data   = numpy.zeros(N_ITER) 
tmp_bifurk = numpy.zeros(DEPTH)

r_min = R_MIN
r_max = R_MAX
r_len = r_max-r_min
eps   = EPS

r  = r_min
eps *= -1
dr = r_len/N_POINTS
for k in range(0, N_POINTS):
    tmp_data[0] = X0
    for i in range(1, N_ITER):
        tmp_data[i] = A*(f(r, tmp_data[i-1])+tmp_data[i-1])
    print('    ${:.2f}$ & ${:.2f}$ & ${:.2f}$ & ${:.2e}$ \\\\ \hline'.format(r, 1-1.0/r, tmp_data[N_ITER-1], abs(1-1.0/r-tmp_data[N_ITER-1])))
    r += dr

