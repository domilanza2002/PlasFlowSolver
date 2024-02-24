#.................................................
#   SYSTEM_SOLVE.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file is needed to solve the linear system
#   in order to use the Newton-Raphson method
#.................................................
import numpy as np #library to solve linear systems
def system_solve(n,A,b): #we define the function system_solve
    """Solves the linear system Ax=b using the linalg.solve function from the scipy library

    Args:
        n (int): number of equations
        A (list): matrix A
        b (list): vector b
    Raises:
        Exception: Error detected in system_solve.py, the linear system cannot be solved.

    Returns:
        x (float list): solution
    """
    #.................................................
    #   This function solves the linear system Ax=b
    #   using the linalg.solve function from the scipy library
    #.................................................
    #   INPUTS:
    #   n: number of equations
    #   A: matrix A
    #   b: vector b
    #   OUTPUTS:
    #   x: solution
    #.................................................
    # we declare some variables:
    x = None #variable to store the solution
    AA = None #variable to store the reducted A matrix
    bb = None #variable to store the reducted b vector
    # AA must be A[1:n,1:n]
    # bb must be b[1:n]
    # we extract AA and bb from A and b
    AA = [[0.0 for i in range(n)] for j in range(n)]
    bb = [0.0]*n
    for i in range(n):
        for j in range(n):
            AA[i][j] = A[i][j]
        bb[i] = b[i]
    # we solve the system using the linalg.solve function
    try: #we use a try-except block to handle exceptions
        x = np.linalg.solve(AA,bb) #we solve the system
    except Exception as e: #if an exception is thrown
        #we inform the user and exit
        raise Exception("Error detected in system_solve.py, the linear system cannot be solved: "+str(e))
    return x #we return the solution
#.................................................
#   Possible improvements:
#   - Improve the efficiency of the code
#.................................................
# EXECUTION TIME: fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................