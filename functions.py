__author__ = 'oleh'

from random import randint

# Generate n dots. Each one has X, Y, Z position in 3D
def generate_array(n):
    l = []
    tmp = []
    for i in range(0, n):
        tmp.append(randint(0, 1000))    # X - pos
        tmp.append(randint(0, 1000))    # Y - pos
        tmp.append(randint(0, 1000))    # Z - pos
        l.append(tmp)
        tmp = []
    return l
