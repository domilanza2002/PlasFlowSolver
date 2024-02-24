#.................................................
#   CONTINUITY.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file is needed to solve the continuity equation: dV/deta=-f'
#.................................................
def continuity(deta, y): #Function to solve the continuity equation
    """This function solves the continuity equation: dV/deta=-f'

    Args:
        deta (float): step for the numerical integration
        y (array): function to integrate

    Returns:
        V (float): integral of y (array)
    """
    #.................................................
    #   This function solves the continuity equation: dV/deta=-f'=y
    #   We use a Simpson numerical integration with step deta and y as function
    #.................................................
    #   INPUTS:
    #   deta: step for the numerical integration
    #   y: function to integrate
    #   OUTPUTS:
    #   V: integral of y
    #.................................................
    #we define some variables:
    V = None # variable to return
    # now we need to perform a Simpson numerical integration with step deta and aa as function
    V = [] # we initialize the v array
    V.append(0) # we append the first value of v
    V.append((17*y[0]+42*y[1]-16*y[2]+6*y[3]-y[4])*deta/48) # we append the second value of v
    for i in range(2,len(y)):
        V.append(V[i-2]+(y[i-2]+4*y[i-1]+y[i])*deta/3) # we append the other values of v  
    return V # we return the V array
#.................................................
#   Possible improvements:
#   -Implement a more efficient integration method
#.................................................
# EXECUTION TIME: Very fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................