#.................................................
#   CLASSES.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module contains all the classes used in the program.
#   There are currently 13 classes:
#   -CF_constants: contains the constants used to convert the read values to the SI units
#   -database_settings_class: contains the database settings read from file
#   -database_inputs_class: contains the database inputs
#   -database_class: contains the database data to be stored
#   -dataframe_class: contains all the variables read from the input files
#   -inputs_class: contains the thermodynamic inputs of the program for the current case
#   -initials_class: contains the initial conditions of the program for the current case
#   -probes_class: contains the probe settings for the current case
#   -settings_class: contains the settings of the program for the current case
#   -initial_conditions_db_class: contains the initial conditions database for the current case
#   -out_properties_class: contains the output properties of the program
#.................................................
class CF_constants:
    """This class contains the constants used to convert
    the read values to the SI units.
    """
    def __init__(self):
        self.P_CF = 1e3  # Conversion factor for pressure (kPa->Pa)
        self.Q_CF = 1e4  # Conversion factor for heat flux (W/cm^2->W/m^2)
        self.L_CF = 1e-3  # Conversion factor for length (mm->m)
#.................................................
class database_settings_class:
    """This class contains the database settings read from file.
    """
    def __init__(self):
        self.db_name = None  # Database name
        self.create_db_flag = None  # Flag to indicate if the database should be created if it does not exist
        self.lower_time_flag = None  # Flag to indicate if the database should be updated if a lower time is found
        self.generate_ic_flag = None  # Flag to indicate if the initial conditions map should be generated from the database
        self.ic_name = None  # Initial conditions map name
        self.ic_mixture_split_flag = None  # Flag to indicate if the initial conditions map should be split by mixture
#.................................................
class database_inputs_class:
    """This class contains the database inputs.
    """
    def __init__(self):
        # Input properties:
        self.P = None  # Pressure
        self.P_dyn =  None  # Dynamic pressure
        self.q_target =  None  # Target heat flux
        self.mixture_name =  None  # Mixture name
        self.T_w =  None  # Probe wall temperature
        self.R_p =  None  # Pitot external radius
        self.R_m =  None  # Heat flux probe external radius
        self.R_j =  None  # Plasma jet radius
        self.barker_type =  None  # Barker's correction type
        self.stag_type =  None  # Stagnation type
#.................................................
class database_class:
    """This class contains the database data to be stored.
    """
    def __init__(self):
        # Input properties:
        self.P = None  # Pressure
        self.P_dyn = None  # Dynamic pressure
        self.q_target = None  # Target heat flux
        self.mixture_name = None  # Mixture name
        self.T_w = None  # Probe wall temperature
        self.R_p = None  # Pitot external radius
        self.R_m = None  # Heat flux probe external radius
        self.R_j = None  # Plasma jet radius
        self.barker_type = None  # Barker's correction type
        self.stag_type = None  # Stagnation type
        # Output properties:
        self.T = None  # Temperature
        self.T_t = None  # Total temperature
        self.u = None  # Flow velocity
        self.P_t = None  # Total pressure
        self.time = None  # Runnning time
        # Convergence properties:
        self.has_converged = None  # Flag to indicate if the iteration has converged
#.................................................
class dataframe_class:
    """This class contains all the variables read from
    the input files, regardless of the type of file.
    """
    def __init__(self):  # Basic constructor
        # To be computed:
        self.n = None  # Number of cases (integer)
        # To be read from the file:
        # Inputs:
        self.comment = None  # Comment (string)
        self.P = None  # Pressure (float)
        self.P_dyn = None  # Dynamic pressure (float)
        self.P_stag = None  # Stagnation pressure (float)
        self.q_target = None  # Target heat flux (float)
        self.plasma_gas = None  # Plasma gas (string)
        # Initial conditions:
        self.ic_db_name = None  # Initial conditions database name (string)
        self.T_0 = None  # Initial static temperature (float)
        self.T_t_0 = None  # Initial total temperature (float)
        self.u_0 = None  # Initial flow velocity (float)
        self.P_t_0 = None  # Initial total pressure (float)
        # Probe settings:
        self.T_w = None  # Probe wall temperature (float)
        self.R_p = None  # Pitot external radius (float)
        self.R_m = None  # External radius of the heat flux probe (float)
        self.R_j = None  # Plasma jet radius (float)
        self.stag_type = None  # Stagnation type (string)
        self.hf_law = None  # Heat flux law (string)
        self.barker_type = None  # Barker's correction type (string)
        # Program settings:
        self.N_p = None  # Number of point for the discretization of normal coordinate of the boundary layer (integer)
        self.max_hf_iter = None  # Maximum number of iterations for the heat flux computation (integer)
        self.hf_conv = None  # Convergence criteria for the heat flux computation (float)
        self.use_prev_ite = None  # Flag to indicate if the previous iteration for the heat flux computation should be
        # used as initial guess for the new iteration (string)
        self.eta_max = None  # Upper integration boundary for the normal coordinate of the boundary layer (float)
        self.log_warning_hf = None  # Flag to indicate if a warning should be logged when the heat flux computation does not converge (string)
        self.newton_conv = None  # Convergence criteria for the Newton-Raphson method (float)
        self.max_newton_iter = None  # Maximum number of iterations for Newton-Raphson method (integer)
        self.jac_diff = None  # Finite difference epsilon for the Jacobian matrix (float)
        self.min_T_relax = None  # Minimum ammissible value for the temperature, used for relaxation (float)
        self.max_T_relax = None  # Maximum ammissible value for the temperature, used for relaxation (float)
#..................................................
class inputs_class: 
    """This class contains the thermodynamic inputs of 
    the program for the current case.
    """
    def __init__(self):  # Basic constructor
        self.comment = None  # Comment (string)
        self.P = None  # Static pressure (float)
        self.P_dyn = None  # Dynamic pressure (float)
        self.P_stag = None  # Stagnation pressure (float)
        self.q_target = None  # Target heat flux (float)
        self.mixture_name = None  # Mixture name (string)
#.................................................
class initials_class:
    """This class contains the initial conditions 
    of the program for the current case.
    """
    def __init__(self):  # Basic constructor
        self.ic_db_name = None  # Initial conditions database name (string)
        self.T_0 = None  # Initial static temperature (float)
        self.T_t_0 = None  # Initial total temperature (float)
        self.u_0 = None  # Initial flow velocity (float)
        self.P_t_0 = None  # Initial total pressure (float)
#.................................................
class probes_class:
    """This class contains the probe settings
    for the current case.
    """
    def __init__(self):  # Basic constructor
        self.T_w = None  # Probe wall temperature (float)
        self.R_p = None  # Pitot external radius (float)
        self.R_m = None  # Heat flux probe external radius (float)
        self.R_j = None  # Plasma jet radius (float)
        self.hf_law = None  # Heat flux law (integer)
        self.barker_type = None  # Barker's correction type (integer)
        self.stag_type = None  # Stagnation type (integer)
        self.stag_var = None  # Stagnation variable, beta*u/R_m (float)
#..................................................
class settings_class:
    """This class contains the settings of the program
    for the current case.
    """
    def __init__(self): #basic constructor
        self.N_p = None #Number of point for the boundary layer eta discretization, integer
        self.max_hf_iter = None #Maximum number of iterations for the heat flux, integer
        self.hf_conv = None #Convergence criteria for the heat flux, float
        self.use_prev_ite = None #Use previous iteration for the heat transfer, string
        self.log_warning_hf = None #Log warning for when the heat flux does not converge, string
        self.eta_max = None #Maximum value for the boundary layer eta, float
        self.newton_conv = None #Convergence criteria for the newton solver, float
        self.max_newton_iter = None #Maximum number of iterations for the newton solver, integer
        self.jac_diff = None #Main newton jacobian finite difference epsilon, float
        self.min_T_relax = None #Minimum value for the temperature used for relaxation, float
        self.max_T_relax = None #Maximum value for the temperature used for relaxation, float
#.................................................
class initial_conditions_db_class:
    """This class contains the initial conditions 
    database for the current case.
    """
    def __init__(self):
        self.db_inputs = None
        self.db_outputs = None
#.................................................
class out_properties_class:
    """This class contains the output properties of the program.
    """
    def __init__(self):
        self.has_converged_out = None  # Variable to store if the iteration has converged
        self.rho_out = None  # Edge density to be written on the output file
        self.T_out = None  # Edge temperature to be written on the output file
        self.h_out = None  # Edge enthalpy to be written on the output file
        self.u_out = None  # Edge velocity to be written on the output file
        self.a_out = None  # Edge sound speed to be written on the output file
        self.M_out = None  # Edge Mach number to be written on the output file
        self.T_t_out = None  # Total temperature to be written on the output file
        self.h_t_out = None  # Total enthalpy to be written on the output file
        self.P_t_out = None  # Total pressure to be written on the output file
        self.Re_out = None  # Pitot Reynolds number to be written on the output file
        self.Kn_out = None  # Knudsen number to be written on the output file
        self.warnings_out=None  # Warnings to be written on the output file
        self.res_out = None  # Final convergence criteria to be written on the output file
        self.species_names_out = None  # Names of the species
        self.species_Y_out = None  # Mass fractions of the species
#.................................................
#   Possible improvements:
#   - Add getters and setters and make all the variable private
#   - Improve organization
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................