"""
detektiert periodenverdoppelungen via lyapunov exponent
und berechnet so die Feigenbaumkonstante

localhost:py keksnicoh$ python -m prak.feigenbaum
searching from 1.9
looking for next start_r from 2.00000000002
searching from 2.99950000003
looking for next start_r from 3.23606797751
searching from 3.44927797752
looking for next start_r from 3.49856169934
searching from 3.54400769935
looking for next start_r from 3.55464086278
searching from 3.56439786279
looking for next start_r from 3.56666737986
found values [2.0000000000249916, 3.236067977509959, 3.498561699344952, 3.554640862779951, 3.5666673798649517]
delta_0=4.70894301336
delta_1=4.68077099865
delta_2=4.66295961155

"""
from numpy import log as nlog, abs, sin, cos

def log(x): 
    if x < 0.0000000000001:
        raise RuntimeWarning()
    return nlog(x)



log_fct = lambda r, x: r*x*(1-x)
dlog_fct = lambda r, x: r-2*r*x

sin_fct = lambda r, x: r*sin(x)
dsin_fct = lambda r, x: r*cos(x)

f = sin_fct
df = dsin_fct

LOWEST = -10**10
def lyapunov(r, n=100):
    try:
        x0 = 0.4
        sum = 0.0
        sum = log(abs(df(r, x0)))
        for i in range(1, n):
            x0 = f(r, x0)
            log_arg = abs(df(r, x0))
            sum += log(log_arg)
        return sum/n
    except RuntimeWarning:
        return LOWEST

BEST = -1000
n = 500
eps = 0.0025
x = 0.0
intervals = [(0.0, 3.5, -0.3)]
infimum = 0.7
min_delta = 0.0000000001
fragmentation = 14000.0
found = []

for i in range(0,2):
    print('run', i, len(intervals))
    eps /= 10.0
    new_intervals = []
    #fragmentation /= 10.0
    for interval in intervals:
        start = None
       
        infimum = interval[2]
        x = interval[0]
        print('DELTA', float(interval[1]-x))
        eps = float(interval[1]-x)/fragmentation
        if eps < 10**-5:
            print('SKIP')
            new_intervals.append(interval)
            continue
        min = 0.0
        while x <= interval[1]:
            l = lyapunov(x)
            if l <= min:
                min = l
            if l <= infimum:
                if start is None:
                    start = x
            elif l > infimum and start is not None:
                print('OKAY', min, eps, start, x, start+(x-start)/2)
                if min < -100.0:
                    min = -100.0
                new_intervals.append((start-eps, x+eps, min))
                start = None
                min = 0.0

            x+=eps

    intervals = new_intervals

for i in intervals:
    print(lyapunov(i[0]+(i[1]-i[0])/2.0, n=5000))

#print(intervals)

#print(x, len(intervals))

#print(len(new_intervals))
#print('found values ' + str(a))
#for i in range(0,len(a)):
#    print('delta_'+str(i)+'='+str((a[i+0]-a[i+1])/(a[i+1]-a[i+2])))