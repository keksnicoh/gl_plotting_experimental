from numpy import log, inf, sqrt

R = 3.99999
X0 = 0.4
N = 1000000
EPS = 0.000001
N_ITER = 1
flog = lambda r, x: r*x*(1-x)


for j in range(0,5):
    result = []
    for k in range(0, N):
        r = R+k*EPS
        x0 = 0.4
        for i in range(0, N_ITER):
            x0 = flog(r, x0)
            if x0 == -inf: 
                break
        
        result.append(x0)

    intervals = []
    current_start = None
    for k in range(0, N):
        r = R+k*EPS
        x0 = 0.4
        if result[k] == -inf and current_start is None:
            current_start = r
        elif result[k] > -inf and current_start is not None:
            intervals.append((current_start, r))
            current_start = None
        
    if current_start is not None:
        intervals.append((current_start, r))

    if len(intervals):
        msg = "N_ITER={} found {} intervals. Last interval [{},{}]".format(
            N_ITER, 
            len(intervals), 
            intervals[len(intervals)-1][0],
            intervals[len(intervals)-1][1])
    else: 
        msg = "nothing at N_ITER={}".format(N_ITER)

    print(msg)
    N_ITER *= 10
