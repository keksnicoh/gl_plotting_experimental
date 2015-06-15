#-*- coding: utf-8 -*-
"""
some matrix functions
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""

import numpy

def translation_matrix(x=0.0, y=0.0, z=0.0):
    return numpy.array([
        1,0,0,0,
        0,1,0,0,
        0,0,1,0,
        x,y,z,1,
    ], dtype=numpy.float32)

def translation_matrix2d(x=0.0, y=0.0):
    return numpy.array([
        1,0,0,
        0,1,0,
        x,y,1,
    ], dtype=numpy.float32)

