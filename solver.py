from time import time
from functools import wraps

from scipy.optimize import linprog


# See documentation for the SciPy functions at:
# https://docs.scipy.org/doc/scipy/reference/optimize.linprog-interior-point.html
# https://docs.scipy.org/doc/scipy/reference/optimize.linprog-revised_simplex.html

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
def _generic_solver(method, A, b, c, x0=None, options=None):
    """
    Solve LP program of the form:
    maximize c*x with: A*x <= b
    :param method: revised simplex OR interior-point
    :return: Dictionary with solution info
    """
    header = f'SIMPLEX - Dim: {len(c)}' if method == 'revised simplex' else \
        f'INTERIOR POINT - Dim: {len(c)} / Alpha0: {options["alpha0"]} / Tolerance: {options["tol"]}'
    try:
        scipy_solution = linprog(c=-c, A_ub=A, b_ub=b, method=method, x0=x0,
                                 options=options)
    except Exception as error:
        return {'header': header, 'error': error}
    solution = {'header': header, 'message': scipy_solution.message, 'status': scipy_solution.status,
                'max_value': -scipy_solution.fun, 'solution': scipy_solution.x, 'num_iterations': scipy_solution.nit, }
    return solution


def simplex(A, b, c, x0=None, max_iterations=100000000):
    """
    Uses revised SIMPLEX algorithm to solves LP problem of the form:
    maximize c*x with: A*x <= b
    :param x0: Initial vertex (Default is origin)
    :param max_iterations: Maximum number of iterations to be run
    :return: Dictionary with solution info
    """
    return _generic_solver('revised simplex', A, b, c, x0, {'maxiter': max_iterations})


def interior_point(A, b, c, alpha0=0.99995, tolerance=1e-8, max_iterations=100000000):
    """
    Uses Mosek interior point algorithm to solves LP problem of the form:
    maximize c*x with: A*x <= b
    :param alpha0: Size of step
    :param tolerance: Termination tolerance
    :param max_iterations: Maximum number of iterations to be run
    :return: Dictionary with solution info
    """
    return _generic_solver('interior-point', A, b, c,
                           options={'maxiter': max_iterations, 'alpha0': alpha0, 'tol': tolerance})
