#.................................................
#   HEAT_FLUX_HF_LAW0.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the 
#   heat flux for the exact heat flux law, hf_law=0
#.................................................
import math  # Library for mathematical operations
import numpy as np  # Library for numerical operations
import heat_flux_hf_law0_edge as heat_flux_hf_law0_edge_file  # Module to compute the edge properties of the flow for hflaw=0
import heat_flux_hf_law0_wall as heat_flux_hf_law0_wall_file  # Module to compute the wall properties of the flow for hflaw=0
import heat_flux_hf_law0_flow as heat_flux_hf_law0_flow_file  # Module to compute the flow properties of the flow for hflaw=0
import continuity as continuity_file  # Module with the function to solve the continuity equation
import first_deriv as first_deriv_file  # Module with the function to compute the first derivative of functions
import eq_diff_solve as eq_diff_solve_file  # Module with the function to solve differential equations

def reset_vars(deta, T_e, T_w, N_p, eta_max):
    """Function to reset the x,y,z arrays
    for the heat flux computation.

    Args:
        deta (float): the step of eta
        T_e (float): the edge temperature
        T_w (float): the wall temperature
        N_p (integer): the number of points for the boundary layer eta discretization

    Returns:
        x (list, float): the eta array
        y (list, float): the F array
        z (list, float): the g array
    """
    # Variables:
    x = None  # Array with the eta discretization
    y = None  # Array with the F values
    z = None  # Array with the g values
    eta = None  # The eta_i-th value
    f_i = None  # The F_i-th value
    g_i = None  # The g_i-th value
    # Initialization:
    x=[]
    y=[] 
    z=[] 
    # Computing the arrays:
    for i in range(N_p):
        eta = i * deta 
        x.append(eta)
        f_i = 0.007005*pow(eta,3) - 0.114439*pow(eta,2) + 0.598555*eta  # Initial solution
        y.append(f_i)
        g_i = min(1, f_i+T_w/T_e*(eta_max-eta)/eta_max)  # Initial solution
        z.append(g_i)
    return x, y, z

def properties_across_BL(T_e, P_e, mu_e, rho_e, C_p_e, z, N_p, mixture_object, max_T_relax):
    # Variables:
    Khi = None  # Vector to store the Khi values, Khi = rho*mu/(rho_e*mu_e)
    rr = None  # Vector to store the rr values, rr = rho_e/rho
    kpr = None  # Vector to store the kpr values, kpr=lambda_eq/(mu_e*C_p*rr)
    C = None  # Vector to store the C values, C=C_p/C_p_e
    T = None  # Variable to store the current temperature
    rho = None  # Density on the current point
    C_p = None  # Specific heat on the current point
    mu = None  # Viscosity on the current point
    lambda_eq = None  # Equilibrium thermal conductivity on the current point
    kpr_i = None  # The kpr_i-th value
    c_i = None  # The c_i-th value
    redo = None # Variable to understand if we need to redo the computation
    
    # Initialization:
    Khi = []  # Reset the Khi array
    rr = []  # Reset the rr array
    kpr = []  # Reset the kpr array
    C = []  # Reset the C array
    redo = False  
    for i in range(0, N_p):
        T = T_e*z[i]  # Current temperature
        if (T<=4 or np.isnan(T) or T>max_T_relax):  #This should never happen
            redo = True
            return Khi, rr, kpr, C, redo
        rho, C_p, mu, lambda_eq = heat_flux_hf_law0_flow_file.heat_flux_hf_law0_flow(P_e, T, mixture_object)
        khi_i = rho*mu/(rho_e*mu_e)
        Khi.append(khi_i)
        rr_i = rho_e/rho 
        rr.append(rr_i)
        kpr_i = lambda_eq/(mu_e*C_p*rr_i) 
        kpr.append(kpr_i) 
        c_i = C_p/C_p_e 
        C.append(c_i) 
    return Khi, rr, kpr, C, redo

def heat_flux(probes, settings, P_e, T_e, u, mixture_object):
    """Function to compute the stagnation heat flux for 
    the hflaw=0 case.

    Args:
        probes (probes_class) : the probes object containing the probe properties
        settings (settings_class) : the settings object containing the program settings
        P_e (float) : the edge pressure, which is the total pressure in this case
        T_e (float) : the total temperature, which is the total temperature in this case
        u (float) : the freestream velocity
        mixture_object (mpp.Mixture) : the mixture object
    
    Raises:
        ValueError: if the temperature is negative, nan or greater than the max temperature

    Returns:
        q (float): the stagnation heat flux
    """
    # Varibles:
    ORDER = 4  # Order of the central finite difference
    max_iter = settings.max_hf_iter  # Maximum number of iterations for the heat flux
    hf_conv = settings.hf_conv  # Convergence criteria for the heat flux
    log_warning_hf = settings.log_warning_hf  # Log warning for when the heat flux does not converge
    N_p = settings.N_p  # Number of points for the boundary layer eta discretization
    eta_max = settings.eta_max  # Maximum value for the boundary layer eta
    T_w = probes.T_w  # Probe wall temperature
    max_T_relax = settings.max_T_relax  # Maximum value for the temperature used for relaxation
    R_m = probes.R_m  # Heat flux probe external radius
    stag_var = probes.stag_var  # Stagnation variable, beta*u/R_m
    beta = stag_var * u/R_m  # Velocity gradient
    q = None  # Variable to store the heat flux
    deta = None  # Variable to store the step of eta
    x = []  # Array to store the eta values
    y = []  # Array to store the F values of the boundary layer
    z = []  # Array to store the g values of the boundary layer
    iter = None  # Variable to store the iteration number
    redo = None  # Variable to understand if we need to reset the boundary layer variables
    # Edge properties:
    rho_e = None  # Density on the edge
    C_p_e = None  # Specific heat on the edge
    mu_e = None  # Viscosity on the edge
    # Wall properties:
    rho_w = None  # Density on the wall
    lambda_eq_wall = None  # Equilibrium thermal conductivity on the wall
    # Loop variables:
    Khi = None  # Vector to store the Khi values, Khi = rho*mu/(rho_e*mu_e)
    rr = None  # Vector to store the rr values, rr = rho_e/rho
    kpr = None  # Vector to store the kpr values, kpr=lambda_eq/(mu_e*C_p*rr)
    C = None  # Vector to store the C values, C=C_p/C_p_e
    aa = None  # Vector to store the aa values: coefficients for the continuity equation, and the differential equations
    bb = None  # Vector to store the bb values: coefficients for the differential equations
    dd = None  # Vector to store the dd values: coefficients for the differential equations
    dkhi = None  # Vector to store the dkhi values: derivative of Khi with respect to eta
    V = None  # Vector to store the V values: solution of the continuity equation
    new_f = None  # The new values of F
    new_g = None  # The new values of g
    hf_first_comp = None  # Variable to understand if the heat flux has been computed previously
    stop = None  # Variable to understand if we need to stop the loop
    dg_v = None  # Vector to store the derivative of g with respect to eta
    dg = None  # The derivative of g with respect to eta
    redo = None  # Variable to understand if we need to reset the boundary layer variables
    already_reset = None  # Variable to understand if we already reset the boundary layer variables
    #.................................................
    #START OF THE CODE:
    deta = eta_max/(N_p-1)  # Step of eta. We use N_p-1 because we need N_p points, not N_p+1 (we start from 0 and we end at eta_max)
    # Now I check if the x, y, z exist, so if the heat flux has been computed previously
    if (settings.use_prev_ite == True):  # If we want to use the previous iteration for the heat flux
        hf_first_comp = np.loadtxt('hf_first_comp.var', dtype=int)  # This file exist for sure, it has been created in the main code
    else:
        hf_first_comp = 0
    if (hf_first_comp == 0):  # I need to compute a starting solution
        x, y, z = reset_vars(deta, T_e, T_w, N_p, eta_max)
    else:  # I need to read the x, y, z arrays from the x.var, y.var and z.var files using numpy
        x = np.loadtxt('x.var')
        y = np.loadtxt('y.var')
        z = np.loadtxt('z.var')
        x = x.tolist() 
        y = y.tolist() 
        z = z.tolist()
    # I need to compute the edge properties:
    rho_e, C_p_e, mu_e = heat_flux_hf_law0_edge_file.heat_flux_hf_law0_edge(P_e, T_e, mixture_object)
    # I need to compute the wall properties:
    rho_w, lambda_eq_wall=heat_flux_hf_law0_wall_file.heat_flux_hf_law0_wall(P_e, T_w, mixture_object)  # Remember, dP/dy = 0
    # I start the convergence loop
    iter = 0
    already_reset = False
    while (iter<max_iter):
        # For safety reason, the loop has a maximum number of iterations, but inside the loop there is also
        # a convergence criteria based on the succesive iteration method
        iter += 1
        # I reset some vectors:
        Khi, rr, kpr, C, redo = properties_across_BL(T_e, P_e, mu_e, rho_e, C_p_e, z, N_p, mixture_object, max_T_relax)
        if (redo == True):
            if (already_reset == True):
                raise ValueError("ERROR: T<=0, nan or T>T_max, resetting BL vars...FAILED")
            print("ERROR: T<=0, nan or T>T_max, resetting BL vars...")
            x, y, z = reset_vars(deta, T_e, T_w, N_p, eta_max)
            Khi, rr, kpr, C, redo = properties_across_BL(T_e, P_e, mu_e, rho_e, C_p_e, z, N_p, mixture_object, max_T_relax)
            already_reset = True
        # Continuity equation:
        aa = []
        for i in range(0, N_p):
            aa.append(-y[i])  # Coefficients for the continuity equation
        V = continuity_file.continuity(deta, aa)  # I solve the continuity equation
        # MOMENTUM EQUATION:
        dkhi = first_deriv_file.first_deriv_array(Khi, deta, ORDER)  # I compute kdhi/deta
        # Reset the aa, bb and dd vectors
        aa = [] 
        bb = [] 
        dd = [] 
        # Coefficients for the linear equation to solve:
        for i in range(0, N_p):
            aa.append( Khi[i]/pow(deta,2) )
            bb.append( (dkhi[i]-V[i])/deta ) 
            dd.append( 0.5*(pow(y[i],2)-rr[i]) )
        f_init = 0  # Initial condition for eta=0
        f_final = 1  # Final condition for eta=eta_max
        new_f = eq_diff_solve_file.solver(aa, bb, dd, f_init, f_final)  # I solve it with the solver module
        # ENERGY EQUATION:
        dkpr = first_deriv_file.first_deriv_array(kpr, deta, ORDER)  # I compute dkpr/deta
        dc = first_deriv_file.first_deriv_array(C, deta, ORDER)  # I compute dc/deta
        # Reset the aa, bb and dd vectors
        aa = [] 
        bb = [] 
        dd = [] 
        # Coefficients for the linear equation to solve:
        for i in range(0, N_p):
            aa.append( kpr[i]/pow(deta,2) )
            bb.append( (dkpr[i]+kpr[i]/C[i]*dc[i]-V[i])/deta )
            dd.append(0)
        g_init = T_w/T_e  # Initial condition for eta=0
        g_final = 1  # Final condition for eta=eta_max
        new_g = eq_diff_solve_file.solver(aa,bb,dd, g_init, g_final)  # I solve it with the solver module
        stop = True 
        # CONVERGENCE CHECK:
        # I check the convergence for each point of the grid, using the succesive iteration convergence criteria
        # If for every point of the grid, the following iteration criteria is reached, we stop the loop
        for i in range(0, N_p):
            if( abs(new_f[i]-y[i]) > hf_conv or abs(new_g[i]-z[i]) > hf_conv ):  # If the convergence is not reached
                stop = False  # We do not stop the loop
                break
        if(stop or iter >= max_iter):  # If we converged or we reached the maximum number of iterations
            if(stop == False and log_warning_hf==True):  # If we did not converge and we want to log the warning
                print("Warning: an heat flux computation did not converge for the current iteration.")
            break  # We stop the loop
        # If we did not converge, we need to update the x,y,z arrays
        for i in range(0, N_p):
            y[i] = new_f[i]
            z[i] = new_g[i]
    # HEAT FLUX COMPUTATION:
    dg_v = first_deriv_file.first_deriv_array(z, deta, ORDER)  # I compute dg/deta
    # I take the value of dg on the wall, eta=0
    dg = dg_v[0] 
    # I compute the heat flux
    q = math.sqrt(2/(rho_e*mu_e))*dg*T_e*rho_w*lambda_eq_wall 
    q = q*math.sqrt(beta)  #beta=stagvar*u/Rm, velocity gradient
    if (settings.use_prev_ite==True and stop==True):  # If we converged and we want to use this solution as starting solution
        # for the next heat flux computation in this case, we save the new x,y,z arrays to the x.var,y.var and z.var files using numpy
        np.savetxt('x.var', x) 
        np.savetxt('y.var', y) 
        np.savetxt('z.var', z)
        if (hf_first_comp==0):  # We need to update the hf_first_comp variable
            hf_first_comp=np.array([1])
            np.savetxt("hf_first_comp.var", hf_first_comp, fmt="%1.1u")
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