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

from numpy import log, abs, sin, cos

n = 2000
eps_initial = 0.0005
depth = 0
max_depth = 8
eps = eps_initial
a = []
start_r = -0.1

log_fct = lambda r, x: r*x*(1-x)
dlog_fct = lambda r, x: r-2*r*x

sin_fct = lambda r, x: r*sin(x)
dsin_fct = lambda r, x: r*cos(x)

f = sin_fct
df = dsin_fct

def lyapunov(r):
    x0 = 0.4
    sum = 0.0
    sum = log(abs(df(r, x0)))
    for i in range(1, n):
        x0 = f(r, x0)
        log_arg = abs(df(r, x0))
        sum += log(log_arg)
    return sum/n

while len(a) < 5:
    # find values
    eps = eps_initial
    right = False
    print('searching from ' + str(start_r))
    while depth < max_depth:
        next_r = start_r + eps
        l1 = lyapunov(start_r)
        l2 = lyapunov(next_r)
        if l2 - l1 <= 0.0:
            start_r = next_r
            right = True
        elif l2 - l1 > 0.0:
            found_r = (start_r + next_r)/2
            start_r = start_r - 2*eps
            if right:
                eps = eps / 10
                depth += 1
                right = False
    a.append(found_r)

    # look for next starting point
    eps = eps_initial
    start_r = found_r
    print('looking for next start_r from ' + str(start_r))
    depth = 0
    while depth < max_depth:
        l1 = lyapunov(start_r)
        l2 = lyapunov(start_r+eps)
        l3 = lyapunov(start_r+eps+eps)

        if not l1 < l2 < l3:
            eps = eps/10.0
            depth+=1
            found_r = start_r + 2*eps
        else:
            start_r += 2.0*eps

    start_r = found_r
    depth = 0
    
print('found values ' + str(a))
for i in range(0,3):
    print('delta_'+str(i)+'='+str((a[i+0]-a[i+1])/(a[i+1]-a[i+2])))