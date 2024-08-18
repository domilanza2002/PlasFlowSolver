#.................................................
#   RETRIEVE_DATA_FILERUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to retrieve the needed
#   data from the dataframe object for the current loop
#   iteration using the filerun mode.
#.................................................
import classes as classes_file  # Module with the classes
from retrieve_helper import retrieve_stag_var  # Function to retrieve the stagnation variable
from retrieve_helper import retrieve_ic  # Function to retrieve the initial conditions database
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
    warnings = None  # Warnings for the reading process (string)
    inputs_object = None  # Inputs object
    initials_object = None  # Initials object
    probes_object = None  # Probes object
    settings_object = None  # Settings object
    # Inputs:
    comment = None  # Comment (string)
    P = None  # Pressure (float)
    P_dyn = None  # Dynamic pressure (float)
    q_target = None  # Target heat flux (float)
    # Initial conditions:
    ic_db_name = None  # Initial conditions database name (string)
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
    stag_var = None  # Stagnation variable (float)
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
    warnings = "None|"
    # INPUTS:
    # Comment:
    comment = df.comment[n_case]  # comment (string)
    inputs_object.comment = comment
    # Pressure:
    try:
        P = float(df.P[n_case])  # Pressure (float)
    except:
        raise ValueError("Error: The static pressure value is not valid.")
    if (P<=0):
        raise ValueError("Error: The pressure value is negative or zero.")
    else:
        inputs_object.P = P 
    # Dynamic pressure:
    try:
        P_dyn = float(df.P_dyn[n_case])  # Dynamic pressure (float)
    except:
        raise ValueError("Error: The dynamic pressure value is not valid.")
    if (P_dyn<=0):
        raise ValueError("Error: The dynamic pressure value is negative or zero.")
    else:
        inputs_object.P_dyn = P_dyn
    # Heat flux:
    try:
        q_target = float(df.q_target[n_case])  # Heat flux (float)
    except: 
        raise ValueError("Error: The heat flux value is not valid.")
    if(q_target<=0):
        raise ValueError("Error: The heat flux value is negative or zero.")
    else:
        inputs_object.q_target = q_target
    # Plasma gas:
    plasma_gas = df.plasma_gas  # Plasma gas (string)
    inputs_object.mixture_name = plasma_gas  # Already managed in read_filerun.py
    # Stagnation pressure:
    inputs_object.P_stag = inputs_object.P + inputs_object.P_dyn  # Stagnation pressure (float)
    # Database name:
    ic_db_name = df.ic_db_name  # Initial conditions database name (string)
    # Initials:
    if (ic_db_name != ""):
        initials_object, warnings_int = retrieve_ic(ic_db_name, inputs_object.P, inputs_object.P_dyn, inputs_object.q_target)
        if (warnings_int is not None):
            warnings += warnings_int
    else:
        T_0 = df.T_0  # Initial temperature (float)
        initials_object.T_0 = T_0 
        T_t_0 = df.T_t_0  # Initial total temperature (float)
        initials_object.T_t_0=T_t_0 
        u_0 = df.u_0  # Initial velocity (float)
        initials_object.u_0 = u_0  # Initial velocity (float)
        P_t_0 = df.P_t_0  # Initial total pressure (float)
        if (P_t_0 == 0):  # If the initial total pressure is zero we set it as the stagnation pressure
            P_t_0 = inputs_object.P_stag
        initials_object.P_t_0=P_t_0 
    # Probe properties:
    # Wall temperature:
    T_w = df.T_w  # Wall temperature, float
    probes_object.T_w = T_w
    # Pitot probe external radius:
    R_p = df.R_p  #Pitot probe external radius (float)
    probes_object.R_p = R_p 
    # Flux probe external radius:
    R_m = df.R_m  #Flux probe external radius (float)
    probes_object.R_m = R_m  #Flux probe external radius (float)
    # Plasma jet radius:
    R_j = df.R_j  #Plasma jet radius (float)
    probes_object.R_j = R_j  
    # Stagnation type:
    stag_type = df.stag_type  #Stagnation type (integer)
    # Not saved in any object
    # Heat flux law:
    hf_law = df.hf_law  #Heat flux law (integer)
    probes_object.hf_law = hf_law  # Already managed in read_filerun.py
    # Barker's correction type:
    barker_type = df.barker_type  #Barker's correction type (integer)
    probes_object.barker_type = barker_type  # Already managed in read_filerun.py
    # Stagnation variable:
    stag_var = retrieve_stag_var(stag_type, R_m, R_j)  #Stagnation variable (float)
    probes_object.stag_var = stag_var
    # Settings:
    N_p = df.N_p  # Number of point for the boundary layer eta discretization (integer)
    settings_object.N_p = N_p 
    # Maximum number of iterations for the heat flux:
    max_hf_iter = df.max_hf_iter  #Maximum number of iterations for the heat flux (integer)
    settings_object.max_hf_iter = max_hf_iter 
    # Convergence criteria for the heat flux:
    hf_conv = df.hf_conv  #Convergence criteria for the heat flux (float)
    settings_object.hf_conv = hf_conv 
    # Use previous iteration for the heat transfer:
    use_prev_ite = df.use_prev_ite  #Use previous iteration for the heat transfer (integer)
    settings_object.use_prev_ite = use_prev_ite  # Already managed in read_filerun.py
    # Maximum value for the boundary layer eta:
    eta_max = df.eta_max  # Maximum value for the boundary layer eta (float)
    settings_object.eta_max = eta_max 
    # Log warning for when the heat flux does not converge:
    log_warning_hf = df.log_warning_hf  # Log warning for when the heat flux does not converge (integer)
    settings_object.log_warning_hf = log_warning_hf  # Already managed in read_filerun.py
    # Convergence criteria for the Newton solver:
    newton_conv = df.newton_conv  #Convergence criteria for the newton solver (float)
    settings_object.newton_conv = newton_conv 
    # Maximum number of iterations for the Newton solver:
    max_newton_iter = df.max_newton_iter  #Maximum number of iterations for the newton solver (integer)
    settings_object.max_newton_iter = max_newton_iter 
    # Jacobian finite difference epsilon
    jac_diff = df.jac_diff  # Jacobian finite difference epsilon (float)
    settings_object.jac_diff = jac_diff 
    # Minimum value for the temperature used for relaxation
    min_T_relax = df.min_T_relax  # Minimum value for the temperature used for relaxation (float)
    settings_object.min_T_relax = min_T_relax 
    # Maximum value for the temperature used for relaxation
    max_T_relax = df.max_T_relax  # Maximum value for the temperature used for relaxation (float)
    settings_object.max_T_relax = max_T_relax 
    # Check Barker's effect and initial total pressure consistency:
    if (probes_object.barker_type == 0 and initials_object.P_t_0 != inputs_object.P_stag):
        initials_object.P_t_0 = inputs_object.P_stag
        warnings += "P_t_0 not consistent with the Barker's correction, set to P_stag|"
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
