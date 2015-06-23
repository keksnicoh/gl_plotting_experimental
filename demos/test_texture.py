from mygl.app import BasicGl
from mygl.util import *
import numpy
def next_p2 (num):
    """ If num isn't a power of 2, will return the next higher power of two """
    rval = 1
    while rval<num:
        rval <<= 1
    return rval

if __name__ == '__main__':
    test = numpy.array([1.45,4], dtype=numpy.float32)
    print(ArrayDatatype.arrayByteCount(test))
    app = BasicGl()
    tex = Texture2D(2048, 2048)
