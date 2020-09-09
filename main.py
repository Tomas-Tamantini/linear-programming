from klee_minty import *
from solver import *

A, b, c = klee_minty()


k = simplex(A, b, c)

print(k)
