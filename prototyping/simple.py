import math


C_r = 82*10**-12 #F
L = 2367*10**-6 # H

w = 1.0 / math.sqrt(L*C_r)
print w

L=372*10**-6
C_r = 2.5*10**-8

w = 1.0 / math.sqrt(L*C_r)
print w

w = 800000
C_r = 82*10**-12 #F

L=1/(C_r*w**2)

L=372*10**-6
C_r=1/(L*w**2)

print C_r