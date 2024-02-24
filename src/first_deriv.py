#.................................................
#   FIRST_DERIV, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file is needed to compute the first derivative of a function,
#   using the finite difference method.
#   At the moment, only the 2nd and 4th order finite difference method are implemented.
#.................................................
def first_deriv_array(f, dx, order): #function to compute the first derivative of a function
    """This function computes the first derivative of a function using the finite difference method.

    Args:
        f (array): function to derive
        dx (float): step for the finite difference method
        order (int): order of the finite difference method
    Returns:
        df (array): first derivative of f
    """
    #.................................................
    #   This function computes the first derivative of a function using the finite difference method.
    #   At the moment, only the 2nd and 4th order finite difference method are implemented.
    #.................................................
    #   INPUTS:
    #   f: function to derive
    #   dx: step for the finite difference method
    #   order: order of the finite difference method
    #   OUTPUTS:
    #   df: first derivative of f
    #.................................................
    # we declare some variables:
    df = None #variable to store the first derivative
    ord = None #actual order used
    n = None #number of points
    # we now check the order:
    if (len(f) <= 2): #if the array is too short, we throw an error
        raise Exception("Error: the array is too short to compute the central finite derivative")
    elif (len(f) == 3 or len(f) == 4):
        ord=2 #maxiumum order usable
    else:
        ord = 4 #maxiumum order usable
    # note: we could add more cases in the future
    if (order<ord): #the order given by the user is lower than the maximum order usable
        ord = order #we use the order given by the user
    # we now compute the first derivative
    n = len(f) #number of points
    # we do a match statement for the order
    df = [0.0]*n #we initialize the df array
    match (ord): #we do a match statement for the order of the finite difference method to use
        case 2: #we use the 2nd order finite difference method(Central and sided on the extrema)
            df[0] = (-3*f[0]+4*f[1]-f[2])/(2*dx) #we compute the first derivative at the first point
            df[n-1] = (3*f[n-1]-4*f[n-2]+f[n-3])/(2*dx) #we compute the first derivative at the last point
            for i in range(1, n-1):
                df[i] = (f[i+1]-f[i-1])/(2*dx)
        case 4: #we use the 4th order finite difference method(Central and sided on the extrema)
            df[0] = (-25*f[0]+48*f[1]-36*f[2]+16*f[3]-3*f[4])/(12*dx) #we compute the first derivative at the first point
            df[1] = (-3*f[0]-10*f[1]+18*f[2]-6*f[3]+f[4])/(12*dx) #we compute the first derivative at the second point
            df[n-1] = (25*f[n-1]-48*f[n-2]+36*f[n-3]-16*f[n-4]+3*f[n-5])/(12*dx) #we compute the first derivative at the last point
            df[n-2] = (3*f[n-1]+10*f[n-2]-18*f[n-3]+6*f[n-4]-f[n-5])/(12*dx) #we compute the first derivative at the second last point
            for i in range(2, n-2):
                df[i] = (f[i-2]-8*f[i-1]+8*f[i+1]-f[i+2])/(12*dx)
        case _: #order not yet implemented, we throw an error
            raise Exception("Error: order not yet implemented")
    return df #we return the first derivative
#.................................................
#   Possible improvements:
#   - Add more finite difference methods, to improve the precision.
#   - We could check the validity of the implementation of the finite difference method.
#.................................................
# EXECUTION TIME: It depends on the order of the finite difference method used, but very fast.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................