from klee_minty import *
from solver import *

A, b, c = klee_minty(dimensions=3, val_b=12)

sol_simplex = simplex(A, b, c)
sol_ip = interior_point(A, b, c, alpha0=0.99, tolerance=1e-6)
sol_hybrid = hybrid(A, b, c, alpha0=0.99, tolerance=1e-6)

print(solution_to_str(sol_simplex))
print(solution_to_str(sol_ip))
print(solution_to_str(sol_hybrid))


