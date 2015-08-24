import numpy 

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