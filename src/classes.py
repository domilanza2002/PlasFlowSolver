#.................................................
#   CLASSES.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module contains all the classes used in the program.
#   There are currently 5 classes:
#   -dataframe_class: class to store all the input variables
#   -inputs_class: class to store all the inputs of the program for the current iteration
#   -initial_conditions_db_class: class to store all the initial conditions database
#   -initials_class: class to store all the initial conditions
#   -probes_class: class to store all the probes properties
#   -settings_class: class to store all the settings of the program
#.................................................
#.................................................
class dataframe_class:
    """This class contains all the variables read from
    the input files, regardless of the type of file.
    """
    def __init__(self):  # Basic constructor
        # To be computed:
        n = None  # Number of cases (integer)
        # To be read from the file:
        # Inputs:
        comment = None  # Comment (string)
        P = None  # Pressure (float)
        P_dyn = None  # Dynamic pressure (float)
        P_stag = None  # Stagnation pressure (float)
        q_target = None  # Target heat flux (float)
        plasma_gas = None  # Plasma gas (string)
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

#..................................................
class inputs_class: 
    """This class contains the thermodynamic inputs of 
    the program for the current case.
    """
    def __init__(self):  # Basic constructor
        comment = None  # Comment (string)
        P = None  # Static pressure (float)
        P_dyn = None  # Dynamic pressure (float)
        P_stag = None  # Stagnation pressure (float)
        q_target = None  # Target heat flux (float)
        mixture_name = None  # Mixture name (string)
        
#.................................................
class initial_conditions_db_class:
    """This class contains the initial conditions 
    database for the current case.
    """
    def __init__(self):  # Basic constructor
        self.db_inputs = None
        self.db_outputs = None
#.................................................

class initials_class:
    """This class contains the initial conditions 
    of the program for the current case.
    """
    def __init__(self):  # Basic constructor
        ic_db_name = None  # Initial conditions database name (string)
        T_0 = None  # Initial static temperature (float)
        T_t_0 = None  # Initial total temperature (float)
        u_0 = None  # Initial flow velocity (float)
        P_t_0 = None  # Initial total pressure (float)

#.................................................
class probes_class:
    """This class contains the probe settings
    for the current case.
    """
    def __init__(self):  # Basic constructor
        T_w = None  # Probe wall temperature (float)
        R_p = None  # Pitot external radius (float)
        R_m = None  # Heat flux probe external radius (float)
        R_j = None  # Plasma jet radius (float)
        hf_law = None  # Heat flux law (integer)
        barker_type = None  # Barker's correction type (integer)
        stag_var = None  # Stagnation variable, beta*u/R_m (float)

#..................................................
class settings_class:
    """This class contains the settings of the program
    for the current case.
    """
    def __init__(self): #basic constructor
        N_p = None #Number of point for the boundary layer eta discretization, integer
        max_hf_iter = None #Maximum number of iterations for the heat flux, integer
        hf_conv = None #Convergence criteria for the heat flux, float
        use_prev_ite = None #Use previous iteration for the heat transfer, string
        log_warning_hf = None #Log warning for when the heat flux does not converge, string
        eta_max = None #Maximum value for the boundary layer eta, float
        newton_conv = None #Convergence criteria for the newton solver, float
        max_newton_iter = None #Maximum number of iterations for the newton solver, integer
        jac_diff = None #Main newton jacobian finite difference epsilon, float
        min_T_relax = None #Minimum value for the temperature used for relaxation, float
        max_T_relax = None #Maximum value for the temperature used for relaxation, float

#.................................................
#   Possible improvements:
#   -Add getters and setters and make all the variable private
#   -Add more constructors
#.................................................
# EXECUTION TIME: Not applicable.
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................