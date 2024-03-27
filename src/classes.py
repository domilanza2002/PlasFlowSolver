#.................................................
#   CLASSES.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file contains the classes of the program.
#   There are currently 5 classes:
#   -inputs_class: class to store all the inputs of the program for the current iteration
#   -settings_class: class to store all the settings of the program
#   -probes_class: class to store all the probes properties
#   -initials_class: class to store all the initial conditions
#   -dataframe_xlsx_class: class to store the dataframe variables from the xlsx file
#.................................................
class inputs_class: #class to store all the inputs of the program for the current iteration
    """This class contains the inputs of the program for the current iteration
    """
    #.................................................
    #   This class contains the inputs of the program for the current iteration
    #.................................................
    def __init__(self): #basic constructor
        comment = None #Comment, string
        P = None #Pressure, float
        Pdyn = None #Dynamic pressure, float
        Pstag = None #Stagnation pressure, float
        q = None #Heat flux, float
        plasma_gas = None #Plasma gas, string
        P_CF = None #Static pressure conversion factor, float
        PD_CF = None #Dynamic pressure conversion factor, float
        PS_CF = None #Stagnation pressure conversion factor, float
        Q_CF = None #Heat flux conversion factor, float
    
class settings_class: #class to store all the settings of the program
    """This class contains the settings of the program
    """
    #.................................................
    #   This class contains the settings of the program
    #.................................................
    def __init__(self): #basic constructor
        p = None #Number of point for the boundary layer eta discretization, integer
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
class probes_class: #class to store all the probes properties
    """This class contains the properties of the probe
    """
    #.................................................
    #   This class contains the properties of the probe
    #.................................................
    def __init__(self): #basic constructor
        Tw = None #Wall temperature, float
        Rp = None #Pitot external radius, float
        Rm = None #Flux probe external radius, float
        Rj = None #Plasma jet radius, float
        stagtype = None #Stagnation type, string->integer
        hflaw = None #Heat flux law, string->integer
        barker = None #Barker correct, string->integer
        stagvar = None #Stagnation variable, float
#.................................................
class initials_class: #class to store all the initial conditions
    """This class contains the initial conditions of the program
    """
    #.................................................
    #   This class contains the initial conditions of the program
    #.................................................
    def __init__(self): #basic constructor
        T_0=None #Initial static temperature, float
        Tt_0=None #Initial total temperature, float
        u_0=None #Initial velocity, float
        Pt_0=None #Initial total pressure, float
#.................................................
class dataframe_xlsx_class: #class to store the dataframe variables from the xlsx file
    #   This class contains the dataframe variables from the xlsx file, read using pandas library.
    """This class contains the dataframe variables from the xlsx file, read using pandas library.
    """
    def __init__(self): #basic constructor
        #To be calculated
        n = None #Number of the test, integer
        #To be read from the xlsx file
        #   -Inputs
        comment = None #Comment, string
        P = None #Pressure, float
        Pdyn = None #Dynamic pressure, float
        Pstag = None #Stagnation pressure, float
        q = None #Heat flux, float
        plasma_gas = None #Plasma gas, string
        #   -Conversion factors
        P_CF=None #Static pressure conversion factor, float
        PD_CF=None #Dynamic pressure conversion factor, float
        Q_CF=None #Heat flux conversion factor, float
        #   -Initial conditions
        T_0=None #Initial static temperature, float
        Tt_0=None #Initial total temperature, float
        u_0=None #Initial velocity, float
        Pt_0=None #Initial total pressure, float
        #   -Probes settings
        Tw = None #Wall temperature, float
        Rp = None #Pitot external radius, float
        Rm = None #Flux probe external radius, float
        Rj = None #Plasma jet radius, float
        stagtype = None #Stagnation type, string->integer
        hflaw = None #Heat flux law, string->integer
        barker = None #Barker correct, string->integer
        #   -Settings
        p = None #Number of point for the boundary layer eta discretization, integer
        max_hf_iter = None #Maximum number of iterations for the heat flux, integer
        hf_conv = None #Convergence criteria for the heat flux, float
        use_prev_ite = None #Use previous iteration for the heat transfer, string
        newton_conv = None #Convergence criteria for the newton solver, float
        max_newton_iter = None #Maximum number of iterations for the newton solver, integer
        jac_diff = None #Main newton jacobian finite difference epsilon, float
        max_T_relax = None #Maximum value for the temperature used for relaxation, float
        min_T_relax = None #Minimum value for the temperature used for relaxation, float
        log_warning_hf = None #Log warning for when the heat flux does not converge, string
        eta_max = None #Maximum value for the boundary layer eta, float
#.................................................
#   Possible improvements:
#   -Add getters and setters and make all the variable private
#   -Add more constructors
#   -Write better docstrings
#.................................................
# EXECUTION TIME: Not applicable.
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................