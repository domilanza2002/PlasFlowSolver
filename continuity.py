#.................................................
#   CONTINUITY.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to solve the continuity equation: dV/deta=-F
#.................................................
def continuity(deta, y): 
    """This function solves the continuity equation: dV/deta=-F
    by using a Simpson numerical integration.

    Args:
        deta (float): step for the numerical integration
        y (array): function to integrate

    Returns:
        V (float): integral of y (array)
    """
    # Variable to return
    V = None
    V = []  # I initialize the V array
    V.append(0)  # The first value of V is 0, since that the integral is from 0 to eta_max
    V.append( (17*y[0]+42*y[1]-16*y[2]+6*y[3]-y[4])*deta/48 )  # The second value of V
    # is obtained by using a modified Simpson rule for better accuracy
    for i in range(2,len(y)):  # Standard Simpson rule
        V.append(V[i-2]+(y[i-2]+4*y[i-1]+y[i])*deta/3) 
    return V
#.................................................
#   Possible improvements:
#   -Implement a more efficient integration method
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................