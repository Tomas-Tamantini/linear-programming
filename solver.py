from time import time
from functools import wraps

from scipy.optimize import linprog


def timer(func):
    """Decorator that times each solution"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        solution = func(*args, **kwargs)
        end = time()
        solution['elapsed_time'] = end - start
        return solution

    return wrapper


@timer
def simplex(A, b, c, x0=None, max_iterations=100000000):
    """
    Uses revised SIMPLEX algorith to solves LP problem of the form:
    maximize c*x with: A*x <= b
    :param x0:
    :return: Dictionary with solution info
    """
    header = f'SIMPLEX - Dim: {len(c)}'
    try:
        scipy_solution = linprog(c=-c, A_ub=A, b_ub=b, method='revised simplex', x0=x0,
                                 options={'maxiter': max_iterations})
    except Exception as error:
        return {'header': header, 'error': error}

    solution = {'header': header, 'message': scipy_solution.message, 'status': scipy_solution.status,
                'max_value': -scipy_solution.fun, 'solution': scipy_solution.x, 'num_iterations': scipy_solution.nit, }
    return solution
