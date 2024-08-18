#.................................................
#   READ_FILERUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to read the
#   database in File Run mode.
#.................................................
import classes as classes_file  # Module that contains the classes of the program
import bash_run as bash_run_file  # Module that contains the functions to detect if a bashrun must be executed
from initial_conditions_map import verify_db  # Function to verify if the database exists
from retrieve_helper import retrieve_mixture_name  # Function to retrieve the mixture name
from retrieve_helper import retrieve_stag_type  # Function to retrieve the stagtype
from retrieve_helper import retrieve_hf_law  # Function to retrieve the hf_law
from retrieve_helper import retrieve_barker_type  # Function to retrieve the barker type
from retrieve_helper import retrieve_use_prev_ite  # Function to retrieve the use_prev_iter
from retrieve_helper import retrieve_log_warning_hf  # Function to retrieve the log_warning_hf

def prompt_input_file():
    """This function prompts the user for the input file 
    and returns the input filename.

    Returns:
        input_filename (string): the input filename
    """
    #Variables:
    input_file_name = None
    print("Please input the name of the .in file with the data.")
    input_file_name = input("Filename: ") 
    # I check if the extension is .in, otherwise I add it
    if (input_file_name.endswith(".in") == False):
        input_file_name = input_file_name + ".in"
    return input_file_name

def prompt_settings_file():
    """This function prompts the user for the settings file 
    and returns the settings filename.

    Returns:
        settings_filename (string): the settings filename
    """
    #Variables:
    settings_file_name = None
    print("Please input the name of the .pfs file with the settings.")
    settings_file_name = input("Filename: ") 
    # I check if the extension is .pfs, otherwise I add it
    if (settings_file_name.endswith(".pfs") == False):
        settings_file_name = settings_file_name + ".pfs"
    return settings_file_name 

def read_filerun(bash_run):
    """ This function reads the dataframe from the .in input
    file and from the .pfs settings file.
    
    Args:
        bash_run (bool): boolean to check if the program is in bash run mode.
    
    Returns:
        df_object (dataframe_class): dataframe object containing the input data.
        output_filename (string): name of the output file.
    """
    #Variables:
    input_filename = None  # Input filename
    settings_filename = None  # Settings filename
    input_file = None  # Input file object
    settings_file = None  # Settings file object
    file_found = None  # Boolean to check if the file is found
    line = None  # Line read from the file
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
    #Variables to return:
    df_object = classes_file.dataframe_class()  # Object with all the variables
    output_filename = None  # Name of the output file
    file_found = False
    #I check if the program is in bash run mode
    if (bash_run == True):
        input_filename = bash_run_file.retrieve_filename()  #I retrieve the filename from the bash.pfs file
        try:  #I try to read the file
            file = open(input_filename, "r")
            file_found = True
            file.close()
        except:  #If the file is not found, we continue in manual mode
            print("Error: the input file specified in bash.pfs does not exist or it is not an .in file.")
            print("The program will continue in manual mode.")
            bash_run = False
    # If the program is not in bash more or the file is not found, we prompt the user for the input file
    while (file_found == False):
        input_filename = prompt_input_file()
        try:  #I try to read the file
            file = open(input_filename, "r")
            file_found = True
            file.close()
        except:
            print("Error: the file does not exist or it is not an .in file.")
    # I set the output filename
    output_filename = input_filename[:-3] + ".out"
    # I read the settings filename
    file_found = False
    # I check if the program is still in bash run mode
    if (bash_run == True):
        settings_filename = bash_run_file.retrieve_settings()  # I retrieve the filename from the bash.pfs file
        try:  # I try to read the file
            file = open(settings_filename, "r") 
            file_found = True
            file.close() 
        except:
            print("Error: the settings file in bash.pfs does not exist or is not an .pfs file.")
            print("The program will continue in manual mode.")
            bash_run = False 
    # If the program is not in bash mode or the file is not found, we prompt the user for the settings file
    while (file_found == False):
        settings_filename = prompt_settings_file()
        try:  # I try to read the file
            file = open(settings_filename, "r") 
            file_found = True 
            file.close() 
        except:
            print("Error: the file does not exist or it is not an .pfs file.")
    # Now I read the settings file
    settings_file = open(settings_filename, "r")
    # Initial conditions:
    settings_file.readline()  # I skip the line, which is the title
    # Initial conditions database name:
    line = settings_file.readline()
    ic_db_name = line.split("=")[1].strip()  # Initial conditions database name (string)
    if (verify_db(ic_db_name) == True):
        print("Initial database " + ic_db_name + " verified.")
    else:
        if (ic_db_name != ""):
            print("Initial database " + ic_db_name + " invalid. Initial conditions will be read from the file.")
        ic_db_name = ""
    # Initial static temperature:
    line = settings_file.readline() 
    try:
        T_0 = float(line.split("=")[1].strip())  # Initial static temperature (float)
        if (T_0 <= 0 and ic_db_name == ""):
            raise ValueError("Error: the initial static temperature is not positive.")
    except:
        raise ValueError("Error: the initial static temperature is not a number.")
    # Initial total temperature:
    line = settings_file.readline() 
    try:
        T_t_0 = float(line.split("=")[1].strip()) 
        if (T_t_0 <= 0 and ic_db_name == ""):
            raise ValueError("Error: the initial total temperature is not positive.")
    except:
        raise ValueError("Error: the initial total temperature is not a number.")
    # Initial velocity:
    line = settings_file.readline() 
    try:
        u_0 = float(line.split("=")[1].strip())  # Initial velocity (float)
        if (u_0 <= 0 and ic_db_name == ""):
            raise ValueError("Error: the initial velocity is not positive.")
    except:
        raise ValueError("Error: the initial velocity is not a number.")
    # Initial total pressure:
    line = settings_file.readline() 
    try:
        P_t_0 = float(line.split("=")[1].strip())  # Initial total pressure (float)
        if (P_t_0 < 0 and ic_db_name == ""):
            raise ValueError("Error: the initial total pressure is negative.")
    except:
        raise ValueError("Error: the initial total pressure is not a number.")
    # Probes properties:
    settings_file.readline()  # I skip the line, which is the title
    # Wall temperature:
    line = settings_file.readline() 
    try:
        T_w = float(line.split("=")[1].strip())  # Wall temperature (float)
        if (T_w <= 0):
            raise ValueError("Error: the wall temperature is not positive.")
    except:
        raise ValueError("Error: the wall temperature is not a number.")
    # Pitot external radius:
    line = settings_file.readline() 
    try:
        R_p = float(line.split("=")[1].strip())  # Pitot external radius (float)
        if (R_p <= 0):
            raise ValueError("Error: the Pitot external radius is not positive.")
    except:
        raise ValueError("Error: the Pitot external radius is not a number.")
    # Flux probe external radius:
    line = settings_file.readline()  # I read the line
    try:
        R_m = float(line.split("=")[1].strip())  # Flux probe external radius (float)
        if (R_m <= 0):
            raise ValueError("Error: the flux probe external radius is not positive.")
    except:
        raise ValueError("Error: the flux probe external radius is not a number.")
    # Plasma jet radius:
    line = settings_file.readline() 
    try:
        R_j = float(line.split("=")[1].strip())  # Plasma jet radius (float)
        if (R_j <= 0):
            raise ValueError("Error: the plasma jet radius is not positive")
    except:
        raise ValueError("Error: the plasma jet radius is not a number")
    # Stagnation type:
    line = settings_file.readline() 
    stag_type = line.split("=")[1].strip().lower()  # Stagnation type (string)
    stag_type = retrieve_stag_type(stag_type)  # Stagnation type (integer)
    # Note: since that the properties are the same for all the cases,
    # I retrieve them here and not in the retrieve_data_filerun.py module
    # Heat flux law:
    line = settings_file.readline() 
    hf_law = line.split("=")[1].strip().lower()  # Heat flux law (string)
    hf_law = retrieve_hf_law(hf_law)  # Heat flux law (integer)
    # Barker's correction type:
    line = settings_file.readline() 
    barker_type = line.split("=")[1].strip().lower()  # Barker's correction type (string)
    barker_type = retrieve_barker_type(barker_type)  # Barker's correction type (integer)
    # Program settings:
    settings_file.readline()  # I skip the line, which is the title
    # Plasma gas:
    line = settings_file.readline() 
    plasma_gas = line.split("=")[1].strip()  # Plasma gas (string)
    plasma_gas = retrieve_mixture_name(plasma_gas)  # Plasma gas (string)
    # Number of point for the boundary layer eta discretization:
    line = settings_file.readline()
    try:
        N_p = float(line.split("=")[1].strip())  # Number of point for the boundary layer eta discretization (integer)
        if (N_p <= 0):
            raise ValueError("Error: the number of point for the boundary layer eta discretization is not positive")
        if (int(N_p) != N_p):
            raise ValueError("Error: the number of point for the boundary layer eta discretization is not an integer.")
    except:
        raise ValueError("Error: the number of point for the boundary layer eta discretization is not an integer")
    N_p = int(N_p)
    # Maximum number of iterations for the heat flux:
    line = settings_file.readline() 
    try:
        max_hf_iter = float(line.split("=")[1].strip())  # Maximum number of iterations for the heat flux (integer)
        if (max_hf_iter <= 0):
            raise ValueError("Error: the maximum number of iterations for the heat flux is not positive.")
        if(int(max_hf_iter) != max_hf_iter):
            raise ValueError("Error: the maximum number of iterations for the heat flux is not an integer.")
    except:
        raise ValueError("Error: the maximum number of iterations for the heat flux is not an integer.")
    max_hf_iter = int(max_hf_iter)
    # Convergence criteria for the heat flux:
    line = settings_file.readline() 
    try:
        hf_conv = float(line.split("=")[1].strip())  # Convergence criteria for the heat flux (float)
        if (hf_conv <= 0):
            raise ValueError("Error: the convergence criteria for the heat flux is not positive.")
    except:
        raise ValueError("Error: the convergence criteria for the heat flux is not a number.")
    # Use previous iteration for the heat transfer:
    line = settings_file.readline() 
    use_prev_ite = line.split("=")[1].strip().lower()  # Use previous iteration for the heat transfer (string)
    use_prev_ite = retrieve_use_prev_ite(use_prev_ite)  # Use previous iteration for the heat transfer (integer)
    # Upper integration boundary for the normal coordinate of the boundary layer:
    line = settings_file.readline() 
    try:
        eta_max = float(line.split("=")[1].strip())  # Upper integration boundary for the normal coordinate of the boundary layer (float)
        if (eta_max <= 0):
            raise ValueError("Error: the maximum value for the boundary layer eta is not positive.")
    except:
        raise ValueError("Error: the maximum value for the boundary layer eta is not a number.")
    # Log warning for when the heat flux does not converge:
    line = settings_file.readline() 
    log_warning_hf = line.split("=")[1].strip().lower()  # Log warning for when the heat flux does not converge (string)
    log_warning_hf = retrieve_log_warning_hf(log_warning_hf)  # Log warning for when the heat flux does not converge (integer)
    # Convergence criteria for the Newton solver:
    line = settings_file.readline() 
    try:
        newton_conv = float(line.split("=")[1].strip())  # Convergence criteria for the newton solver (float)
        if (newton_conv <= 0):
            raise ValueError("Error: the convergence criteria for the newton solver is not positive.")
    except:
        raise ValueError("Error: the convergence criteria for the newton solver is not a number.")
    # Maximum number of iterations for the Newton solver:
    line = settings_file.readline()
    try:
        max_newton_iter = float(line.split("=")[1].strip())  # Maximum number of iterations for the newton solver (integer)
        if (max_newton_iter <= 0):
            raise ValueError("Error: the maximum number of iterations for the newton solver is not positive.")
        if (int(max_newton_iter) != max_newton_iter):
            raise ValueError("Error: the maximum number of iterations for the newton solver is not an integer.")
    except:
        raise ValueError("Error: the maximum number of iterations for the newton solver is not an integer.")
    max_newton_iter = int(max_newton_iter)
    # Jacobian finite difference epsilon:
    line = settings_file.readline() 
    try:
        jac_diff = float(line.split("=")[1].strip()) 
        if (jac_diff <= 0):
            raise ValueError("Error: the Jacobian finite difference epsilon is not positive.")
    except:
        raise ValueError("Error: the Jacobian finite difference epsilon is not a number.")
    # Minimum value for the temperature used for relaxation:
    line = settings_file.readline() 
    try:
        min_T_relax = float(line.split("=")[1].strip())  # Minimum value for the temperature used for relaxation (float)
        if (min_T_relax <= 0):
            raise ValueError("Error: the minimum value for the temperature used for relaxation is not positive.")
    except:
        raise ValueError("Error: the minimum value for the temperature used for relaxation is not a number.")
    # Maximum value for the temperature used for relaxation:
    line = settings_file.readline() 
    try:
        max_T_relax = float(line.split("=")[1].strip())  # Maximum value for the temperature used for relaxation (float)
        if (max_T_relax <= 0):
            raise ValueError("Error: the maximum value for the temperature used for relaxation is not positive.")
    except:
        raise ValueError("Error: the maximum value for the temperature used for relaxation is not a number.")
    # I close the settings file
    settings_file.close()
    # Now I read the input file
    input_file = open(input_filename, "r")
    line = input_file.readline() 
    comment = []
    P = []
    P_dyn = []
    q_target = []
    while (line != "" and line != "\n"):  # I read the file until the end
        # the first 20 characters of the line are the comment, then 20 for the pressure, 20 for the dynamic pressure, 20 for the heat flux
        comment.append(line[:20].strip()) 
        P.append(line[20:40].strip().replace("d","e")) 
        P_dyn.append(line[40:60].strip().replace("d","e")) 
        q_target.append(line[60:80].strip().replace("d","e")) 
        line = input_file.readline() 
        # The "replace" is order to accept format in the Fortran style
    # I close the input file
    input_file.close() 
    n = len(comment)  # Number of cases
    # I now save the variables in the dataframe object
    df_object.n = n
    df_object.comment = comment
    df_object.P = P
    df_object.P_dyn = P_dyn
    df_object.q_target = q_target
    df_object.plasma_gas = plasma_gas   
    df_object.ic_db_name = ic_db_name
    df_object.T_0 = T_0
    df_object.T_t_0 = T_t_0
    df_object.u_0 = u_0
    df_object.P_t_0 = P_t_0
    df_object.T_w = T_w
    df_object.R_p = R_p
    df_object.R_m = R_m
    df_object.R_j = R_j
    df_object.stag_type = stag_type
    df_object.hf_law = hf_law
    df_object.barker_type = barker_type
    df_object.N_p = N_p
    df_object.max_hf_iter = max_hf_iter
    df_object.hf_conv = hf_conv
    df_object.use_prev_ite = use_prev_ite
    df_object.eta_max = eta_max
    df_object.log_warning_hf = log_warning_hf
    df_object.newton_conv = newton_conv
    df_object.max_newton_iter = max_newton_iter
    df_object.jac_diff = jac_diff
    df_object.min_T_relax = min_T_relax
    df_object.max_T_relax = max_T_relax
    # I return the dataframe object and the output filename
    return df_object, output_filename
#.................................................
#   Possible improvements:
#   -Add getter and setter for the dataframe object
#.................................................
#   EXECUTION TIME: Not relevant
#.................................................
#   Known problems:
#   - None
#.................................................