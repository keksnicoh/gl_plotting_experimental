import numpy 

def iteration(f, l=100):
    data=numpy.zeros(l*2)
    data[0] = 0
    data[1] = f(0.5)
    for i in range(1, l):
        data[i*2] = i 
        data[i*2 +1] = f(data[i*2 -1])
    print(data)
    return data


def iteration_attractor_quadruple(f, l=100):
    """
    erstellt datensatz welcher die iterationsschritte visualisiert.
    """
    data = numpy.zeros(l*4)
    data[0] = 0.1
    data[1] = 0.0
    data[2] = data[0]
    data[3] = f(data[0])
    for i in range(1, l):
        data[i*4] = data[i*4 -1]
        data[i*4+1] = data[i*4 -1]
        data[i*4+2] = data[i*4 -1]
        data[i*4+3] = f(data[i*4 -1])

    return data



def iteration_attractor_quadruple_opt1(f, l=100):
    """
    erstellt datensatz welcher die iterationsschritte visualisiert.
    """
    data = numpy.zeros(l*4)
    data[0] = 0.1
    data[1] = 0.0
    data[2] = data[0]
    data[3] = f(data[0])
    for i in range(1, l):
        data[i*4] = data[i*4 -1]
        data[i*4+1] = data[i*4 -1]
        data[i*4+2] = data[i*4 -1]
        data[i*4+3] = (f(data[i*4 -1]) + data[i*4 -1])/2

    return data



def bifurcation(f, l=100, rn=10000, imax=1000, xs=2.5, xe=4.0):
    """
    erstellt datensatz welcher die iterationsschritte visualisiert.
    """

    #xs, xe = 2.5, 4.0

    data = numpy.zeros(rn*imax/2*3)
    k = 0
    for i in range(0, rn):
        r = xs+i*(xe-xs)/rn
        x = 0.5
        for j in range(0, imax):
            
            if j > imax/2:
                data[k*3] = r
                data[k*3 +1] = f(r, x)
                data[k*3 +2] = 2*(float(j)/imax-0.5)

                x = data[k*3 +1] 
                k+=1
            else:
                x = f(r,x)


    return data

def bifurcation_opt(f, l=100):
    """
    erstellt datensatz welcher die iterationsschritte visualisiert.
    """

    imax = 1000
    rn = 10000
    xs, xe = 2.5, 4.0

    data = numpy.zeros(rn*imax/2*3)
    k = 0
    for i in range(0, rn):
        r = xs+i*(xe-xs)/rn
        x = 0.5
        for j in range(0, imax):
            
            if j > imax/2:
                data[k*3] = r
                data[k*3 +1] = f(r, x)
                data[k*3 +2] = 2*(float(j)/imax-0.5)

                x = data[k*3 +1] 
                k+=1
            else:
                x = f(r,x)+x


    return data