#.................................................
#   RETRIEVE_DATA_FILERUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to retrieve the needed
#   data from the dataframe object for the current loop
#   iteration using the filerun mode.
#.................................................
import classes as classes_file  # Module with the classes

def retrieve_data(df, n_case):
    """This function retrieves the needed data 
    from the dataframe object from the current loop iteration
    for the filerun mode.

    Args:
        df (dataframe_class): the dataframe object
        n_case (int): the number of the current case

    Returns:
        inputs_class (inputs_class): the inputs object containing the inputs
        initials_class (initials_class): the initials object containing the initials
        probes_class (probes_class): the probes object containing the probes
        settings_class (settings_class): the settings object containing the settings
    """
    
    # Variables:
    ratio_L = None # Ratio between the flux probe external radius and the plasma jet radius (float)
    den_sv = None  # Denominator for the stagnation variable (float)
    mixture_name = None  # Mixture name (string)
    warnings = None  # Warnings for the reading process (string)
    # Inputs:
    comment = None  # Comment (string)
    P = None  # Pressure (float)
    P_dyn = None  # Dynamic pressure (float)
    P_stag = None  # Stagnation pressure (float)
    q_target = None  # Target heat flux (float)
    plasma_gas = None  # Plasma gas (string)
    # Initial conditions:
    T_0 = None  # Initial static temperature (float)
    T_t_0 = None  # Initial total temperature (float)
    u_0 = None  # Initial flow velocity (float)
    P_t_0 = None  # Initial total pressure (float)
    # Probe settings:
    T_w = None  # Probe wall temperature (float)
    R_p = None  # Pitot external radius (float)
    R_m = None  # External radius of the heat flux probe (float)
    R_j = None  # Plasma jet radius (float)
    stag_type = None  # Stagnation type (string)
    hf_law = None  # Heat flux law (string)
    barker_type = None  # Barker's correction type (string)
    # Program settings:
    N_p = None  # Number of point for the discretization of normal coordinate of the boundary layer (integer)
    max_hf_iter = None  # Maximum number of iterations for the heat flux computation (integer)
    hf_conv = None  # Convergence criteria for the heat flux computation (float)
    use_prev_ite = None  # Flag to indicate if the previous iteration for the heat flux computation should be
    # used as initial guess for the new iteration (string)
    eta_max = None  # Upper integration boundary for the normal coordinate of the boundary layer (float)
    log_warning_hf = None  # Flag to indicate if a warning should be logged when the heat flux computation does not converge (string)
    newton_conv = None  # Convergence criteria for the Newton-Raphson method (float)
    max_newton_iter = None  # Maximum number of iterations for Newton-Raphson method (integer)
    jac_diff = None  # Finite difference epsilon for the Jacobian matrix (float)
    min_T_relax = None  # Minimum ammissible value for the temperature, used for relaxation (float)
    max_T_relax = None  # Maximum ammissible value for the temperature, used for relaxation (float)

    # Variables to return:
    inputs_object = classes_file.inputs_class()  
    initials_object = classes_file.initials_class() 
    probes_object = classes_file.probes_class() 
    settings_object = classes_file.settings_class()
    warnings = [] 
    # Inputs:
    warnings = "None|"
    # Comment: no checks needed
    comment = df.comment[n_case] #Comment, string
    inputs_object.comment = comment #Comment, string
    # Pressure:
    try:
        P = float(df.P[n_case]) #Pressure, float
    except:
        raise ValueError("Error: The pressure value is not valid")
    if (P<=0):
        raise ValueError("Error: The pressure value is not valid")
    else:
        inputs_object.P = P #Pressure, float
    # Dynamic pressure:
    try:
        Pdyn = float(df.Pdyn[n_case]) #Dynamic pressure, float
    except:
        raise ValueError("Error: The dynamic pressure value is not valid")
    if (Pdyn<=0):
        raise ValueError("Error: The dynamic pressure value is not valid")
    else:
        inputs_object.Pdyn = Pdyn
    # Heat flux:
    try:
        q = float(df.q[n_case]) #Heat flux, float
    except: 
        raise ValueError("Error: The heat flux value is not valid")
    if(q<=0):
        raise ValueError("Error: The heat flux value is not valid")
    else:
        inputs_object.q = q #Heat flux, float
    # Plasma gas:
    plasma_gas = df.plasma_gas #Plasma gas, string
    inputs_object.plasma_gas = plasma_gas #Plasma gas, string
    # Conversion factors:
    P_CF = df.P_CF #Static pressure conversion factor, float
    inputs_object.P_CF = P_CF #Static pressure conversion factor, float
    inputs_object.P *= inputs_object.P_CF #We convert the pressure to the right unit
    PD_CF = df.PD_CF #Dynamic pressure conversion factor, float
    inputs_object.PD_CF = PD_CF #Dynamic pressure conversion factor, float
    inputs_object.Pdyn *= inputs_object.PD_CF #We convert the dynamic pressure to the right unit
    inputs_object.Pstag = inputs_object.P + inputs_object.Pdyn #Stagnation pressure, float
    Q_CF = df.Q_CF #Heat flux conversion factor, float
    inputs_object.Q_CF = Q_CF #Heat flux conversion factor, float
    inputs_object.q *= inputs_object.Q_CF #We convert the heat flux to the right unit
    # Initials:
    T_0 = df.T_0 #Initial temperature, float
    initials_object.T_0=T_0 #Initial temperature, float
    Tt_0 = df.Tt_0 #Initial total temperature, float
    initials_object.Tt_0=Tt_0 #Initial total temperature, float
    u_0 = df.u_0 #Initial velocity, float
    initials_object.u_0=u_0 #Initial velocity, float
    Pt_0 = df.Pt_0 #Initial total pressure, float
    if (Pt_0 == 0):
        Pt_0 = inputs_object.Pstag
    initials_object.Pt_0=Pt_0 #Initial total pressure, float
    # Probes:
    # Wall temperature
    Tw = df.Tw #Wall temperature, float
    probes_object.Tw = Tw #Wall temperature, float
    # Pitot probe
    Rp = df.Rp #Pitot external radius, float
    probes_object.Rp = Rp #Pitot external radius, float
    # Flux probe
    Rm = df.Rm #Flux probe external radius, float
    probes_object.Rm = Rm #Flux probe external radius, float
    # Plasma jet
    Rj = df.Rj #Plasma jet radius, float
    probes_object.Rj = Rj #Plasma jet radius, float
    # Stagnation type
    stagtype = df.stagtype #Stagnation type, string->integer
    probes_object.stagtype = stagtype #Stagnation type, string->integer
    # Heat flux law
    hflaw = df.hflaw #Heat flux law, string->integer
    probes_object.hflaw = hflaw #Heat flux law, string->integer
    # Barker correct
    barker = df.barker #Barker correct, string->integer
    probes_object.barker = barker #Barker correct, string->integer
    # Stagnation variable
    match stagtype:
        case 0:
            ratio_L=Rm/Rj
            if(ratio_L<=1):
                den_sv=2-ratio_L-1.68*pow((ratio_L-1),2)-1.28*pow((ratio_L-1),3)
                stagvar=1/den_sv
            else:
                stagvar=ratio_L
        case _:
            raise ValueError("Error: Check the code, you should not be here")
    probes_object.stagvar = stagvar
    # Settings:
    p = df.p #Number of point for the boundary layer eta discretization, integer
    settings_object.p = p #Number of point for the boundary layer eta discretization, integer
    # Maximum number of iterations for the heat flux
    max_hf_iter = df.max_hf_iter #Maximum number of iterations for the heat flux, integer
    settings_object.max_hf_iter = max_hf_iter #Maximum number of iterations for the heat flux, integer
    # Convergence criteria for the heat flux
    hf_conv = df.hf_conv #Convergence criteria for the heat flux, float
    settings_object.hf_conv = hf_conv #Convergence criteria for the heat flux, float
    # Use previous iteration for the heat transfer
    use_prev_ite = df.use_prev_ite #Use previous iteration for the heat transfer, string
    settings_object.use_prev_ite = use_prev_ite #Use previous iteration for the heat transfer, string
    # Convergence criteria for the newton solver
    newton_conv = df.newton_conv #Convergence criteria for the newton solver, float
    settings_object.newton_conv = newton_conv #Convergence criteria for the newton solver, float
    # Maximum number of iterations for the newton solver
    max_newton_iter = df.max_newton_iter #Maximum number of iterations for the newton solver, integer
    settings_object.max_newton_iter = max_newton_iter #Maximum number of iterations for the newton solver, integer
    # Main newton jacobian finite difference epsilon
    jac_diff = df.jac_diff #Main newton jacobian finite difference epsilon, float
    settings_object.jac_diff = jac_diff #Main newton jacobian finite difference epsilon, float
    # Maximum value for the temperature used for relaxation
    max_T_relax = df.max_T_relax #Maximum value for the temperature used for relaxation, float
    settings_object.max_T_relax = max_T_relax #Maximum value for the temperature used for relaxation, float
    # Minimum value for the temperature used for relaxation
    min_T_relax = df.min_T_relax #Minimum value for the temperature used for relaxation, float
    settings_object.min_T_relax = min_T_relax #Minimum value for the temperature used for relaxation, float   
    # Log warning for when the heat flux does not converge
    log_warning_hf = df.log_warning_hf #Log warning for when the heat flux does not converge, string
    settings_object.log_warning_hf = log_warning_hf #Log warning for when the heat flux does not converge, string
    # Maximum value for the boundary layer eta
    eta_max = df.eta_max #Maximum value for the boundary layer eta, float
    settings_object.eta_max = eta_max #Maximum value for the boundary layer eta, float   
    # Return the objects
    return inputs_object, initials_object, probes_object, settings_object, warnings
#.................................................
#   Possible improvements:
#   -Use getter and setter for the inputs, initials, probes and settings objects
#.................................................
# Execution time: Not relevant.
#.................................................
#   Known problems:
#   None.
#.................................................
