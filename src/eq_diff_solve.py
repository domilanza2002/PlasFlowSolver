#.................................................
#   EQ_DIFF_SOLVE.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This project file is needed to solve
#   the differential equation of the model.
#.................................................
def thomas(a,c,e,d): #Function to solve a tridiagonal system
    """This function solves a tridiagonal system of equations.

    Args:
        a (float array): diagonal of the matrix
        c (float array): upper diagonal of the matrix
        e (float array): lower diagonal of the matrix
        d (float array): vector of the solution
    Raises:
        Exception: wrong input size

    Returns:
        x (float array): vector of the solution
    """
    #.................................................
    #   This function is the Thomas algorithm.
    #.................................................
    #   INPUTS:
    #   a: diagonal of the matrix
    #   c: upper diagonal of the matrix
    #   e: lower diagonal of the matrix
    #   d: vector of the solution
    #   OUTPUTS:
    #   x: vector of the solution
    #.................................................
    # we define some variables:
    x = None # variable to return
    y = None # variable to store the y values
    n = None # number of points
    beta = None # variable to store the beta values, lower diagonal of L
    alpha = None # variable to store the alpha values, diagonal of U
    # we compute the number of points
    n = len(a) # number of points
    if (len(c) != n-1 or len(e) != n-1 or len(d) != n): # we check the input
        raise Exception('ERROR: wrong input size')
    # we compute the values:
    alpha = [0.0]*n # we initialize the alpha array
    beta = [0.0]*(n-1) # we initialize the beta array
    alpha[0] = a[0] # we compute the first alpha value
    for i in range(0,n-1): # we compute the alpha and beta values
        beta[i] = e[i]/alpha[i]
        alpha[i+1] = a[i+1]-beta[i]*c[i]
    y = [0.0]*n # we initialize the y array
    y[0] = d[0] # we compute the first y value
    for i in range(1,n): # we compute the y values
        y[i] = d[i]-beta[i-1]*y[i-1]
    x = [0.0]*n # we initialize the x array
    x[n-1] = y[n-1]/alpha[n-1] # we compute the last x value
    for i in range(n-2,-1,-1): # we compute the x values
        x[i] = (y[i]-c[i]*x[i+1])/alpha[i]
    return x # we return the result

def solver(a,b,d,f_init,f_final): #function to solve a tridiagonal system
    """This function solves the differential equation of the model.

    Args:
        a (float array): the a coefficients of the differential equation
        b (float array): the b coefficients of the differential equation
        d (float array): the d coefficients of the differential equation
        f_init (float): the initial condition for eta=0
        f_final (float): the final condition for eta=6
    Raises:
        Exception: wrong input size

    Returns:
        res (float array): vector of the solution
    """
    #.................................................
    #   This function solves the differential equation of the model.
    #.................................................
    #   INPUTS:
    #   a: the a coefficients of the differential equation
    #   b: the b coefficients of the differential equation
    #   d: the d coefficients of the differential equation
    #   f_init: the initial condition for eta=0
    #   f_final: the final condition for eta=6
    #   OUTPUTS:
    #   res: vector of the solution
    #.................................................
    # we define some variables:
    res = None # variable to return
    n = None # number of points
    aa = None # vector to store the matrix values
    bb = None # vector to store the matrix values
    cc = None # vector to store the matrix values
    dd = None # vector to store the matrix values
    n = len(a) # number of points
    if (len(b) != n or len(d) != n): # we check the input
        raise Exception('ERROR: wrong input size')
    # Let us remember that we have n points, but:
    #   eta=0 has res=f_init
    #   eta=6 has res=f_final
    #   so we have n-2 points to solve
    ns = n-2 # number of points to solve
    # now we compute the coefficients of the matrix
    aa = [0.0]*ns # we initialize the aa array
    bb = [0.0]*ns # we initialize the bb array
    cc = [0.0]*ns # we initialize the cc array
    dd = [0.0]*ns # we initialize the dd array
    # in reality the aa and cc vectors have ns-1 points, because they are the upper and lower diagonals of the matrix
    for i in range(1, ns+1):
        mnp1p1 = a[i+1] + 1.5*b[i+1]
        mnp10 = -2*( a[i+1] + b[i+1] )
        mnp1m1 = a[i+1] + 0.5*b[i+1]
        mnp1al = -( 6*a[i+1] + 2*b[i+1] )
        mnp1be = -( 10*a[i+1] + 2*b[i+1] )
        mnp1 = a[i] + 0.5*b[i]
        mn0 = -2*a[i]
        mnm1 = a[i]-0.5*b[i]
        mnal = b[i]
        mnbe = 2*a[i]
        mnm1p1 = a[i-1] - 0.5*b[i-1]
        mnm10 = 2*( -a[i-1] + b[i-1])
        mnm1m1 = a[i-1] - 1.5*b[i-1]
        mnm1al = 6*a[i-1] - 2*b[i-1]
        mnm1be = -10*a[i-1] + 2*b[i-1]
        #determinants to eliminate alfa and beta
        delnp1 = mnal*mnp1be - mnp1al*mnbe
        deln = mnp1al*mnm1be - mnm1al*mnp1be
        delnm1 = mnm1al*mnbe - mnal*mnm1be
        #coefficients of the system
        aa[i-1] = mnm1p1*delnp1 + mnp1*deln + mnp1p1*delnm1
        bb[i-1] = mnm10*delnp1 + mn0*deln + mnp10*delnm1
        cc[i-1] = mnm1m1*delnp1 + mnm1*deln + mnp1m1*delnm1
        dd[i-1] = d[i-1]*delnp1 + d[i]*deln + d[i+1]*delnm1
    #making it really tridiagonal
    dd[0] -= cc[0]*f_init
    dd[ns-1] -= aa[ns-1]*f_final
    #solving with thomas algorithm:
    res = [0.0]*n # we initialize the res array
    res[0] = f_init # we compute the first res value
    res[n-1] = f_final # we compute the last res value
    cc = cc[1:ns] # we remove the first element of cc
    aa = aa[0:ns-1] # we remove the last element of aa
    res[1:n-1] = thomas(bb,aa,cc,dd) # we compute the res values
    return res # we return the result
#.................................................
#   Possible improvements:
#   None
#.................................................
# EXECUTION TIME: fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................