#.................................................
#   TRIDIAG_INV.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This project file is needed to solve
#   a tridiagonal system of equations.
#   The module is composed by two functions:
#   thomas() and tridiag_inv().
#   The first one is the Thomas algorithm, called by the second one.
#   The second one is the function that solves the tridiagonal system.
#.................................................
def thomas(ngm1,a,b,c,d): #function to solve a tridiagonal system
    #.................................................
    #   This function is the Thomas algorithm.
    #   It is called by the tridiag_inv() function.
    #.................................................
    #   INPUTS:
    #   ngm1: number of points minus 1
    #   a: vector of the a coefficients
    #   b: vector of the b coefficients
    #   c: vector of the c coefficients
    #   d: vector of the d coefficients
    #   OUTPUTS:
    #   res: vector of the solution
    #.................................................
    # we define some variables:
    res=None # variable to return
    b[0]=1/b[0]
    a[0]=d[0]*b[0]
    for i in range(1,ngm1):
        c[i-1]=c[i-1]*b[i-1]
        b[i]=b[i]-a[i]*c[i-1]
        b[i]=1/b[i]
        a[i]=(d[i]-a[i]*a[i-1])*b[i]
    res=[0.0]*ngm1 # we initialize the res array
    res[ngm1-1]=a[ngm1-1]
    # we solve for res
    for i in range(1,ngm1):
        k=ngm1-1-i
        res[k]=a[k]-c[k]*res[k+1]
    return res # we return the result

def tridiag_inv(wrhs,f1,g1,h1,a,b,c,d): #function to solve a tridiagonal system
    #.................................................
    #   This function solves a tridiagonal system of equations.
    #   It uses the Thomas algorithm.
    #.................................................
    #   INPUTS:
    #   wrhs: ???????
    #   f1: ??????
    #   g1: ???????
    #   h1: ???????
    #   a: vector of the a coefficients
    #   b: vector of the b coefficients
    #   c: vector of the c coefficients
    #   d: vector of the d coefficients
    #   OUTPUTS:
    #   res: vector of the solution
    #.................................................
    # we define some variables:
    res=None # variable to return
    ng=len(a) # number of points
    aa=None # vector to store the aa values
    bb=None # vector to store the bb values
    cc=None # vector to store the cc values
    dd=None # vector to store the dd values
    ngm1=ng-1 # number of points minus 1
    # now we compute the coefficients of th ematrix(for 2<=n<=n-1=ngm1), but python starts from 0, so we need to add 1 to the index
    aa=[0.0]*ng # we initialize the aa array
    bb=[0.0]*ng # we initialize the bb array
    cc=[0.0]*ng # we initialize the cc array
    dd=[0.0]*ng # we initialize the dd array
    for n in range(1,ngm1):
        mnp1p1=a[n+1]+1.5*b[n+1]+c[n+1]
        mnp10=-(2*a[n+1]+2*b[n+1])
        mnp1m1=a[n+1]+0.5*b[n+1]
        mnp1al=-(6*a[n+1]+2*b[n+1])
        mnp1be=-(10*a[n+1]+2*b[n+1])
        mnp1=a[n]+0.5*b[n]
        mn0=-2*a[n]+c[n]
        mnm1=a[n]-0.5*b[n]
        mnal=b[n]
        mnbe=2*a[n]
        mnm1p1=a[n-1]-0.5*b[n-1]
        mnm10=2*(-a[n-1]+b[n-1])
        mnm1m1=a[n-1]-1.5*b[n-1]+c[n-1]
        mnm1al=6*a[n-1]-2*b[n-1]
        mnm1be=-10*a[n-1]+2*b[n-1]
        #determinants to eliminate alfa and beta
        delnp1=mnal*mnp1be-mnp1al*mnbe
        deln=mnp1al*mnm1be-mnm1al*mnp1be
        delnm1=mnm1al*mnbe-mnal*mnm1be
        #coefficients of the system
        aa[n]=mnm1p1*delnp1+mnp1*deln+mnp1p1*delnm1
        bb[n]=mnm10*delnp1+mn0*deln+mnp10*delnm1
        cc[n]=mnm1m1*delnp1+mnm1*deln+mnp1m1*delnm1
        dd[n]=d[n-1]*delnp1+d[n]*deln+d[n+1]*delnm1
    #coefficients at the wall
    mrp1=-0.5*f1
    mr0=2*f1
    mrm1=-1.5*f1+g1
    mral=-2*f1
    mrbe=2*f1
    m1p1=a[0]-0.5*b[0]
    m10=-2*a[0]+2*b[0]
    m1m1=a[0]-1.5*b[0]+c[0]
    m1al=6*a[0]-2*b[0] 
    m1be=-10*a[0]+2*b[0]
    m2p1=a[1]+0.5*b[1]
    m20=-2*a[1]+c[1]
    m2m1=a[1]-0.5*b[1]
    m2al=b[1]
    m2be=2*a[1]
    #determinants to eliminate alfa and beta
    delnp1=m1al*m2be-m2al*m1be
    deln=m2al*mrbe-mral*m2be
    delnm1=mral*m1be-m1al*mrbe
    #coefficients of the matrix at the wall
    r3=mrp1*delnp1+m1p1*deln+m2p1*delnm1
    r2=mr0*delnp1+m10*deln+m20*delnm1
    r1=mrm1*delnp1+m1m1*deln+m2m1*delnm1
    r=h1*delnp1+d[0]*deln+d[1]*delnm1
    #making it really tridiagonal
    dd[ngm1-1]=dd[ngm1-1]-aa[ngm1-1]*wrhs
    bb[0]=r1*aa[1]-r3*cc[1]
    aa[0]=r2*aa[1]-r3*bb[1]
    dd[0]=r*aa[1]-r3*dd[1]
    cc[0]=0
    aa[ngm1-1]=0
    #solving with thomas algorithm:
    res=thomas(ngm1,cc,bb,aa,dd)
    return res # we return the result
#.................................................
#   Possible improvements:
#   - Understand better what the function does and how to improve it
#.................................................
# EXECUTION TIME: fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................