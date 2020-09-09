from klee_minty import *
from solver import *

A, b, c = klee_minty()


k = simplex(A, b, c)
l = interior_point(A, b, c)
h = hybrid(A,b ,c)
print(k)
print(l)
print(h)
