#.................................................
#   HEAT_FLUX_HFLAW0.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This project file is needed to compute the 
#   heat flux for the exact heat flux law, hflaw=0
#.................................................
import math #Library for mathematical operations
import numpy as np #Library for numerical operations
import mutationpp as mpp #Library to compute the mixture properties
import heat_flux_hflaw0_edge as heat_flux_hflaw0_edge_file #Module with the function to compute the edge properties of the flow for hflaw=0
import heat_flux_hflaw0_wall as heat_flux_hflaw0_wall_file #Module with the function to compute the wall properties of the flow for hflaw=0
import heat_flux_hflaw0_flow as heat_flux_hflaw0_flow_file #Module with the function to compute the flow properties of the flow for hflaw=0
import continuity as continuity_file #Module with the function to solve the continuity equation to compute the heat flux
import first_deriv as first_deriv_file #Module with the function to compute the first derivative of a function
import eq_diff_solve as eq_diff_solve_file #Module with the function to solve the differential equation

def reset_vars(deta, Te, Tw, p): #function to reset the x,y,z arrays
    """Function to reset the x,y,z arrays

    Args:
        deta (_type_): _description_
        Te (_type_): _description_
        Tw (_type_): _description_
        p (_type_): _description_

    Returns:
        _type_: _description_
    """
    y=[] # we reset the y array
    z=[] # we reset the z array
    for i in range(p):
        eta = i*deta # we compute the eta value
        f_i = 0.007005*pow(eta,3)-0.114439*pow(eta,2)+0.598555*eta # we compute the f' starting value/guess(formula from previous code)
        y.append(f_i) # we append the f' value to the array
        g_i = min(1,f_i+Tw/Te*(6-eta)/6) # we compute the g starting value/guess(formula from previous code)
        #g_i=f_i+Tw/Te*(6-eta)/6 # we compute the g starting value/guess(formula from previous code)
        z.append(g_i) # we append the g value to the array
    return y,z

def heat_flux_hflaw0(probes, settings, Pt, Tt, ue, mixture_object): #function to compute the heat flux for the hflaw=0 case
    """Function to compute the heat flux for the hflaw=0 case

    Args:
        probes (probes_class) : the probes object containing the probes
        settings (settings_class) : the settings object containing the settings
        Pt (float) : the total pressure
        Tt (float) : the total temperature
        ue (float) : the edge velocity
        mixture_object (mpp.Mixture) : the mixture of the case
    
    Raises:
        Exception: if the temperature is negative, nan or greater than the max temperature

    Returns:
        q (float): the heat flux
    """
    #.................................................
    #   This function computes the heat flux for the hflaw=0 case
    #.................................................
    #   INPUTS:
    #   probes: the probes object containing the probes
    #   settings: the settings object containing the settings
    #   Pt: the total pressure
    #   Tt: the total temperature
    #   ue: the edge velocity
    #   mixture_object: the mixture of the case
    #.................................................
    #   OUTPUTS:
    #   q: the heat flux
    #.................................................
    # we now define some new variables:
    ORDER = 4 #order for the central,backward and forward finite difference method for the derivatives.
    max_iter = settings.max_hf_iter #maximum number of iterations for the heat flux computations
    hf_conv = settings.hf_conv #convergence criteria for the heat flux computation
    log_warning_hf = settings.log_warning_hf #log warning for when the heat flux does not converge
    eta_max = settings.eta_max #maximum value for the boundary layer eta
    Pe = Pt # To compute the heat flux at the stagnation point, we use the total pressure(measured OUTSIDE the boundary layer)
    Te = Tt # To compute the heat flux at the stagnation point, we use the total temperature(measured OUTSIDE the boundary layer)
    ue = ue # To compute the heat flux at the stagnation point, we use the edge velocity(measured OUTSIDE the boundary layer)
    Tw = probes.Tw # To compute the heat flux at the stagnation point, we use the wall temperature(constant)
    p = settings.p # Number of points for the boundary layer eta discretization
    q = None #variable to store the heat flux
    eta = None #variable to store the eta_i-th value
    f_i = None #variable to store the f'_i-th value
    g_i = None #variable to store the g_i-th value
    deta = None #variable to store the step of eta
    x = [] #array to store the eta values=eta of the boundary layer(normal)
    y = [] #array to store the f' values of the boundary layer
    z = [] #array to store the g values of the boundary layer
    T = None #variable to store the current loop temperature
    iter = None #variable to store the number of iterations
    redo = None #variable to understand if we need to reset the boundary layer variables
    # edge properties:
    rhoe = None #density on the edge
    cpe = None #specific heat on the edge
    mue = None #viscosity on the edge
    # wall properties:
    rhow = None #density on the wall
    kwt = None #thermal conductivity on the wall
    # flow properties:
    rho = None #density on the current point
    cp = None #specific heat on the current point
    mu = None #viscosity on the current point
    k = None #thermal conductivity on the current point
    # loop variables:
    khi = None #vector to store the khi values. khi=rho*mu/(rhoe*mue)
    rr = None #vector to store the rr values. rr=rhoe/rho
    kpr = None #vector to store the kpr values. kpr=k/(mue*cp*rr)
    c = None #vector to store the c values. c=cp/cpe
    e = None #vector to store the e values. e=ue^2/(cpe*Te)
    aa = None #vector to store the aa values: coefficients for the continuity equation
    bb = None #vector to store the bb values: coefficients for the quadratic equation
    dd = None #vector to store the dd values: coefficients for the quadratic equation
    dkhi = None #vector to store the dkhi values: derivative of khi with respect to eta
    V = None #vector to store the V values: solution of the continuity equation
    newf = None #variable to solve the tridiag system, new f
    q_first = None #variable to understand if the heat flux has been computed previously
    #START OF THE CODE:
    # Now we define the eta array used to distretize eta:
    # we go from eta=0 to eta=6(we should go to infinity, but we stop at 6. It is a good approximation)
    deta = eta_max/(p-1) #step of eta. We use p-1 because we need p points, not p+1(we start from 0 and we end at 6)
    # now we check if the x,y,z exist, so if the heat flux has been computed previously
    # we need to read the q_first variable from the q_first.var file using numpy
    q_first=np.loadtxt('q_first.var',dtype=int) # we read the q_first variable from the file
    if(q_first == 0 or settings.use_prev_ite == False): #we have never computed the heat flux and we want to use this feature
        # we now create the x array, which starts from 0, steps of deta, of p points and we initialize f' and g arrays.
        # The x array contains the eta values
        for i in range(p):
            eta = i*deta # we compute the eta value
            x.append(eta) # we append the eta value to the array
            f_i = 0.007005*pow(eta,3)-0.114439*pow(eta,2)+0.598555*eta # we compute the f' starting value/guess(formula from previous code)
            y.append(f_i) # we append the f' value to the array
            g_i = min(1,f_i+Tw/Te*(6-eta)/6) # we compute the g starting value/guess(formula from previous code)
            z.append(g_i) # we append the g value to the array
    else: # we have already computed the heat flux and we use the feature
        # we need to read the x,y,z arrays from the x.var,y.var and z.var files using numpy
        x = np.loadtxt('x.var')
        y = np.loadtxt('y.var')
        z = np.loadtxt('z.var')
        x = x.tolist() # we convert the array to a list
        y = y.tolist() # we convert the array to a list
        z = z.tolist() # we convert the array to a list
    # now we need to compute the flow properties at the edge
    rhoe, cpe,mue=heat_flux_hflaw0_edge_file.heat_flux_hflaw0_edge(Pe,Te,mixture_object)
    # now we need to compute the flow properties at wall:
    rhow, kwt=heat_flux_hflaw0_wall_file.heat_flux_hflaw0_wall(Pe,Tw,mixture_object)
    # now we can start the convergence loop to find the solution
    iter = 0 # we initialize the iteration counter
    while (iter<max_iter): # we start the convergence loop
        #For safety reason, the loop has a maximum number of iterations, but inside the loop there is also
        #a convergence criteria
        iter += 1 # we increase the iteration counter
        # we start by getting the properties across the BL grid
        # we reset some vectors:
        khi = [] # we reset the khi array
        rr = [] # we reset the rr array
        kpr = [] # we reset the kpr array
        c = [] # we reset the c array
        e = [] # we reset the e array
        redo = False
        for i in range(0, p):
            T = Te*z[i] # we compute the temperature. This is because g=z=T/Te
            if(T<=4 or np.isnan(T) or T>settings.max_T_relax): #This should never happen
                print("ERROR: T<=0, nan or T>T_max, resetting BL vars...") # it does not make sense to have a negative temperature
                if(p<1000):
                    p=2*p
                else:
                    raise Exception("ERROR: T<=0, nan or T>T_max, resetting BL vars...") # we raise an exception
                y, z = reset_vars(deta, Te, Tw, p)
                redo = True
                break
            rho, cp, mu, k=heat_flux_hflaw0_flow_file.heat_flux_hflaw0_flow(Pe, T, mixture_object)
            khi_i = rho*mu/(rhoe*mue) # we compute the khi value
            khi.append(khi_i) # we append the khi value to the array
            rr_i = rhoe/rho # we compute the rr value
            rr.append(rr_i) # we append the rr value to the array
            kpr_i = k/(mue*cp*rr_i) # we compute the kpr value
            kpr.append(kpr_i) # we append the kpr value to the array
            c_i = cp/cpe # we compute the c value
            c.append(c_i)  # we append the c value to the array
            e_i = pow(ue,2)/(cpe*Te) # we compute the e value
            e.append(e_i) # we append the e value to the array
        if (redo == True):
            khi = [] # we reset the khi array
            rr = [] # we reset the rr array
            kpr = [] # we reset the kpr array
            c = []    # we reset the c array
            e = []    # we reset the e array
            for i in range(0,p):
                T = Te*z[i] # we compute the temperature. This is because g=z=T/Te
                # now we retrive the flow properties:
                rho, cp, mu, k = heat_flux_hflaw0_flow_file.heat_flux_hflaw0_flow(Pe, T, mixture_object)
                khi_i = rho*mu/(rhoe*mue) # we compute the khi value
                khi.append(khi_i)   # we append the khi value to the array
                rr_i = rhoe/rho   # we compute the rr value
                rr.append(rr_i)  # we append the rr value to the array
                kpr_i = k/(mue*cp*rr_i) # we compute the kpr value
                kpr.append(kpr_i)   # we append the kpr value to the array
                c_i = cp/cpe # we compute the c value
                c.append(c_i)  # we append the c value to the array
                e_i = pow(ue,2)/(cpe*Te) # we compute the e value
                e.append(e_i) # we append the e value to the array
            redo=False
        # now we need to solve the continuity equation to find V
        # we compute the aa vector. This is because dV/deta=-f'=y
        aa = [] # we initialize the aa array
        for i in range(0, p):
            aa.append(-y[i]) # we append the value to the array
        V = continuity_file.continuity(deta, aa) # we solve the continuity equation
        # now we need to solve the momentum equation for y=f'
        #firstly, we need to compute the dkhi vector, that is the derivative of khi with respect to eta
        dkhi = first_deriv_file.first_deriv_array(khi, deta, ORDER) # we compute the dkhi vector
        # we reset the aa,bb,cc and dd vectors
        aa = [] # we initialize the aa array
        bb = [] # we initialize the bb array
        dd = [] # we initialize the dd array
        # we set the coefficients of the linear equation to solve
        for i in range(0, p):
            aa.append(khi[i]/pow(deta,2))
            bb.append((dkhi[i]-V[i])/deta) 
            dd.append(0.5*(pow(y[i],2)-rr[i]))
        f_init = 0 # we set the initial condition for eta=0
        f_final = 1 # we set the final condition for eta=6
        newf = eq_diff_solve_file.solver(aa, bb, dd, f_init, f_final) # we solve it with the solver module
        # now we need to solve the energy equation for z=g
        # we computed the needed derivatives
        dkpr = first_deriv_file.first_deriv_array(kpr, deta, ORDER)
        dc = first_deriv_file.first_deriv_array(c, deta, ORDER)
        dy = first_deriv_file.first_deriv_array(y, deta, ORDER)
        # we reset the aa,bb,cc and dd vectors
        aa = [] # we initialize the aa array
        bb = [] # we initialize the bb array
        dd = [] # we initialize the dd array
        # we set the coefficients of the linear equation to solve
        for i in range(0, p):
            aa.append(kpr[i]/pow(deta,2))
            bb.append((dkpr[i]+kpr[i]/c[i]*dc[i]-V[i])/deta)
            dd.append(e[i]/c[i]*(0.5*rr[i]*y[i]-khi[i]*pow(dy[i],2)))
        g_init = Tw/Te # we set the initial condition for eta=0
        g_final = 1 # we set the final condition for eta=6
        newg = eq_diff_solve_file.solver(aa,bb,dd, g_init, g_final) # we solve it with the solver module
        # now we need to check the convergence to exit the loop
        stop = True # we initialize the stop variable to True
        # we check the convergence for each point of the grid, using the succesive iteration convergence criteria
        # If for each point of the grid, the following iteration criteria is reached, we stop the loop
        for i in range(0, p):
            if(abs(newf[i]-y[i])>hf_conv or abs(newg[i]-z[i])>hf_conv): # if the convergence is not reached
                stop = False # we set the stop variable to False, we do not stop
        # we also stop the loop if the max number of iterations is reached
        if(stop or iter>=max_iter): # if the convergence is reached or the max number of iterations is reached
            if(stop == False and log_warning_hf==True): # if we didn't converge but we reached the max number of iterations and we want to log the warning
                print("Warning: an heat flux computation did not converge for the current iteration") # we print the warning
            break # we exit the loop
        # If we do not stop, now we need to update the f and g arrays
        for i in range(0, p):
            y[i] = newf[i]
            z[i] = newg[i]
    # now we need to compute the heat flux
    #we find the derivative of g=z with respect to eta
    dg_v = first_deriv_file.first_deriv_array(z, deta, ORDER) # we compute the derivative of g with respect to eta
    #we take the value on the wall,eta=0
    dg = dg_v[0] #we take the value on the wall,eta=0
    q = math.sqrt(2/(rhoe*mue))*dg*Te*rhow*kwt # we compute the heat flux
    # we multiply by the stagnation variable
    q = q*math.sqrt(probes.stagvar*ue/probes.Rm) #we multiply by the stagnation variable
    if (settings.use_prev_ite==True and stop==True): # if we want to use the previous iteration and the convergence is reached
        # we save the new x,y,z arrays to the x.var,y.var and z.var files using numpy
        np.savetxt('x.var',x) # we save the x array to the file
        np.savetxt('y.var',y) # we save the y array to the file
        np.savetxt('z.var',z) # we save the z array to the file
        if (q_first==0):
            q_first=np.array([1]) #we update q_first to 1
            np.savetxt("q_first.var",q_first, fmt="%1.1u") # we save the q_first variable to the file
    return q
#.................................................
#   Possible improvements:
#   -Make the central finite derivative order variable
#   -Improve the diff eq algorithm
#   -Understand if we need to keep the x,y,z arrays to the files
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................