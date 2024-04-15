#.................................................
#   READ_FILERUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to read the
#   database in File Run mode.
#.................................................
import classes as classes_file  # Module that contains the classes of the program
import bash_run as bash_run_file  # Module that contains the functions to detect if a bashrun must be executed

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
    # Conversion factors:
    P_CF = None  # Static pressure conversion factor (float)
    P_dyn_CF = None  # Dynamic pressure conversion factor (float)
    P_stag_CF = None  # Stagnation pressure conversion factor (float)
    q_CF = None  # Heat flux conversion factor (float)
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
    # conversion factors
    settings_file.readline()
    #Static pressure conversion factor:
    line = settings_file.readline() #I read the line
    try:
        P_CF = float(line.split("=")[1].strip()) #I save the static pressure conversion factor
        if (P_CF <= 0):
            raise ValueError("Error: the static pressure conversion factor is not positive")
            
    except:
        raise ValueError("Error: the static pressure conversion factor is not a number")
    #Dynamic pressure conversion factor:
    line = settings_file.readline() #I read the line
    try:
        PD_CF = float(line.split("=")[1].strip()) #I save the dynamic pressure conversion factor
        if (PD_CF <= 0):
            raise ValueError("Error: the dynamic pressure conversion factor is not positive")
    except:
        raise ValueError("Error: the dynamic pressure conversion factor is not a number")
    #Heat flux conversion factor:
    line = settings_file.readline() #I read the line
    try:
        Q_CF = float(line.split("=")[1].strip()) #I save the heat flux conversion factor
        if (Q_CF <= 0):
            raise ValueError("Error: the heat flux conversion factor is not positive")
    except:
        raise ValueError("Error: the heat flux conversion factor is not a number")
    #Initial conditions:
    settings_file.readline()
    #Initial static temperature:
    line = settings_file.readline() #I read the line
    try:
        T_0 = float(line.split("=")[1].strip()) #I save the initial static temperature
        if (T_0 <= 0):
            raise ValueError("Error: the initial static temperature is not positive")
    except:
        raise ValueError("Error: the initial static temperature is not a number")
    #Initial total temperature:
    line = settings_file.readline() #I read the line
    try:
        Tt_0 = float(line.split("=")[1].strip()) #I save the initial total temperature
        if (Tt_0 <= 0):
            raise ValueError("Error: the initial total temperature is not positive")
    except:
        raise ValueError("Error: the initial total temperature is not a number")
    #Initial velocity:
    line = settings_file.readline() #I read the line
    try:
        u_0 = float(line.split("=")[1].strip()) #I save the initial velocity
        if (u_0 <= 0):
            raise ValueError("Error: the initial velocity is not positive")
    except:
        raise ValueError("Error: the initial velocity is not a number")
    #Initial total pressure:
    line = settings_file.readline() #I read the line
    try:
        Pt_0 = float(line.split("=")[1].strip()) #I save the initial total pressure
        if (Pt_0 < 0):
            raise ValueError("Error: the initial total pressure is negative")
    except:
        raise ValueError("Error: the initial total pressure is not a number")
    #Probes properties:
    settings_file.readline()
    #Wall temperature:
    line = settings_file.readline() #I read the line
    try:
        Tw = float(line.split("=")[1].strip()) #I save the wall temperature
        if (Tw <= 0):
            raise ValueError("Error: the wall temperature is not positive")
    except:
        raise ValueError("Error: the wall temperature is not a number")
    #Pitot external radius:
    line = settings_file.readline() #I read the line
    try:
        Rp = float(line.split("=")[1].strip()) #I save the pitot external radius
        if (Rp <= 0):
            raise ValueError("Error: the pitot external radius is not positive")
    except:
        raise ValueError("Error: the pitot external radius is not a number")
    #Flux probe external radius:
    line = settings_file.readline() #I read the line
    try:
        Rm = float(line.split("=")[1].strip()) #I save the flux probe external radius
        if (Rm <= 0):
            raise ValueError("Error: the flux probe external radius is not positive")
    except:
        raise ValueError("Error: the flux probe external radius is not a number")
    #Plasma jet radius:
    line = settings_file.readline() #I read the line
    try:
        Rj = float(line.split("=")[1].strip()) #I save the plasma jet radius
        if (Rj <= 0):
            raise ValueError("Error: the plasma jet radius is not positive")
    except:
        raise ValueError("Error: the plasma jet radius is not a number")
    #Stagnation type:
    line = settings_file.readline() #I read the line
    stagtype = line.split("=")[1].strip() #I save the stagnation type
    match stagtype:
        case "flat":
            stagtype = 0
        case _:
            raise ValueError("Error: the stagnation type is not valid")
    #Heat flux law:
    line = settings_file.readline() #I read the line
    hflaw = line.split("=")[1].strip() #I save the heat flux law
    match hflaw:
        case "exact":
            hflaw = 0
        case _:
            raise ValueError("Error: the heat flux law is not valid")
    #Barker correction:
    line = settings_file.readline() #I read the line
    barker = line.split("=")[1].strip() #I save the barker correction
    match barker:
        case "none":
            barker = 0
        case "homann":
            barker = 1
        case "carleton":
            barker = 2
        case _:
            raise ValueError("Error: the barker correction is not valid")
    #Settings:
    settings_file.readline()
    #Plasma gas:
    line = settings_file.readline() #I read the line
    plasma_gas = line.split("=")[1].strip().lower() #I save the plasma gas
    match plasma_gas:
        case "air":
            plasma_gas = "air_13"
        case "n2":
            plasma_gas = "nitrogen2"
        case "air_13":
            plasma_gas = "air_13"
        case "nitrogen2":
            plasma_gas = "nitrogen2"
        case "air_11":
            plasma_gas = "air_11"
        case _:
            raise ValueError("Error: the plasma gas is not valid")
    #Number of point for the boundary layer eta discretization:
    line = settings_file.readline() #I read the line
    try:
        p = int(line.split("=")[1].strip()) #I save the number of point for the boundary layer eta discretization
        if (p <= 0):
            raise ValueError("Error: the number of point for the boundary layer eta discretization is not positive")
    except:
        raise ValueError("Error: the number of point for the boundary layer eta discretization is not an integer")
    #Maximum number of iterations for the heat flux:
    line = settings_file.readline() #I read the line
    try:
        max_hf_iter = int(line.split("=")[1].strip()) #I save the maximum number of iterations for the heat flux
        if (max_hf_iter <= 0):
            raise ValueError("Error: the maximum number of iterations for the heat flux is not positive")
    except:
        raise ValueError("Error: the maximum number of iterations for the heat flux is not an integer")
    #Convergence criteria for the heat flux:
    line = settings_file.readline() #I read the line
    try:
        hf_conv = float(line.split("=")[1].strip()) #I save the convergence criteria for the heat flux
        if (hf_conv <= 0):
            raise ValueError("Error: the convergence criteria for the heat flux is not positive")
    except:
        raise ValueError("Error: the convergence criteria for the heat flux is not a number")
    #Use previous iteration for the heat transfer:
    line = settings_file.readline() #I read the line
    use_prev_ite = line.split("=")[1].strip() #I save the use previous iteration for the heat transfer
    match use_prev_ite:
        case "yes":
            use_prev_ite = 1
        case "no":
            use_prev_ite = 0
        case 1:
            use_prev_ite = 1
        case 0:
            use_prev_ite = 0
        case _:
            raise ValueError("Error: the use previous iteration for the heat transfer is not valid")
    #Convergence criteria for the newton solver:
    line = settings_file.readline() #I read the line
    try:
        newton_conv = float(line.split("=")[1].strip()) #I save the convergence criteria for the newton solver
        if (newton_conv <= 0):
            raise ValueError("Error: the convergence criteria for the newton solver is not positive")
    except:
        raise ValueError("Error: the convergence criteria for the newton solver is not a number")
    #Maximum number of iterations for the newton solver:
    line = settings_file.readline() #I read the line
    try:
        max_newton_iter = int(line.split("=")[1].strip()) #I save the maximum number of iterations for the newton solver
        if (max_newton_iter <= 0):
            raise ValueError("Error: the maximum number of iterations for the newton solver is not positive")
    except:
        raise ValueError("Error: the maximum number of iterations for the newton solver is not an integer")
    #Main newton jacobian finite difference epsilon:
    line = settings_file.readline() #I read the line
    try:
        jac_diff = float(line.split("=")[1].strip()) #I save the main newton jacobian finite difference epsilon
        if (jac_diff <= 0):
            raise ValueError("Error: the main newton jacobian finite difference epsilon is not positive")
    except:
        raise ValueError("Error: the main newton jacobian finite difference epsilon is not a number")
    #Maximum value for the temperature used for relaxation:
    line = settings_file.readline() #I read the line
    try:
        max_T_relax = float(line.split("=")[1].strip()) #I save the maximum value for the temperature used for relaxation
        if (max_T_relax <= 0):
            raise ValueError("Error: the maximum value for the temperature used for relaxation is not positive")
    except:
        raise ValueError("Error: the maximum value for the temperature used for relaxation is not a number")
    #Minimum value for the temperature used for relaxation:
    line = settings_file.readline() #I read the line
    try:
        min_T_relax = float(line.split("=")[1].strip()) #I save the minimum value for the temperature used for relaxation
        if (min_T_relax <= 0):
            raise ValueError("Error: the minimum value for the temperature used for relaxation is not positive")
    except:
        raise ValueError("Error: the minimum value for the temperature used for relaxation is not a number")
    #Log warning for when the heat flux does not converge:
    line = settings_file.readline() #I read the line
    match line:
        case "yes":
            log_warning_hf = True
        case "no":
            log_warning_hf = False
        case _:
            raise ValueError("Error: the log warning for when the heat flux does not converge is not valid")
    #eta_max:
    line = settings_file.readline() #I read the line
    try:
        eta_max = float(line.split("=")[1].strip()) #I save the maximum value for the boundary layer eta
        if (eta_max <= 0):
            raise ValueError("Error: the maximum value for the boundary layer eta is not positive")
    except:
        raise ValueError("Error: the maximum value for the boundary layer eta is not a number")
    #I close the settings file
    settings_file.close()
    #Now I read the input file
    input_file = open(input_filename, "r") #I open the file
    line = input_file.readline() #I read the line
    comment = []
    P = []
    Pdyn = []
    q = []
    while (line != "" and line!="\n"): #I read the file until the end
        # the first 20 characters of the line are the comment, then 20 for the pressure, 20 for the dynamic pressure, 20 for the heat flux
        comment.append(line[:20].strip()) #I save the comment
        P.append(line[20:40].strip().replace("d","e")) #I save the pressure
        Pdyn.append(line[40:60].strip().replace("d","e")) #I save the dynamic pressure
        q.append(line[60:80].strip().replace("d","e")) #I save the heat flux
        line = input_file.readline() #I read the line
    input_file.close() #I close the file
    n = len(comment) #I save the number of cases
    #I now save the variables in the dataframe object
    df_object.n = n #Number of cases, integer
    df_object.comment = comment #Comment, string
    df_object.P = P #Pressure, float
    df_object.Pdyn = Pdyn #Dynamic pressure, float
    df_object.Pstag = None
    df_object.q = q #Heat flux, float
    df_object.plasma_gas = plasma_gas #Plasma gas, string
    df_object.P_CF = P_CF #Static pressure conversion factor, float
    df_object.PD_CF = PD_CF #Dynamic pressure conversion factor, float
    df_object.PS_CF = None
    df_object.Q_CF = Q_CF #Heat flux conversion factor, float
    df_object.T_0 = T_0 #Initial static temperature, float
    df_object.Tt_0 = Tt_0 #Initial total temperature, float
    df_object.u_0 = u_0 #Initial velocity, float
    df_object.Pt_0 = Pt_0 #Initial total pressure, float
    df_object.Tw = Tw #Wall temperature, float
    df_object.Rp = Rp #Pitot external radius, float
    df_object.Rm = Rm #Flux probe external radius, float
    df_object.Rj = Rj #Plasma jet radius, float
    df_object.stagtype = stagtype #Stagnation type, string->integer
    df_object.hflaw = hflaw #Heat flux law, string->integer
    df_object.barker = barker #Barker correct, string->integer
    df_object.p = p #Number of point for the boundary layer eta discretization, integer
    df_object.max_hf_iter = max_hf_iter #Maximum number of iterations for the heat flux, integer
    df_object.hf_conv = hf_conv #Convergence criteria for the heat flux, float
    df_object.use_prev_ite = use_prev_ite #Use previous iteration for the heat transfer, string
    df_object.newton_conv = newton_conv #Convergence criteria for the newton solver, float
    df_object.max_newton_iter = max_newton_iter #Maximum number of iterations for the newton solver, integer
    df_object.jac_diff = jac_diff #Main newton jacobian finite difference epsilon, float
    df_object.max_T_relax = max_T_relax #Maximum value for the temperature used for relaxation, float
    df_object.min_T_relax = min_T_relax #Minimum value for the temperature used for relaxation, float
    df_object.log_warning_hf = log_warning_hf #Log warning for when the heat flux does not converge, string
    df_object.eta_max = eta_max #Maximum value for the boundary layer eta, float
    return df_object,output_filename #return the dataframe class object and the output filename
#.................................................
#   Possible improvements:
#   -Add getter and setter for the dataframe object
#   -Throw specific exceptions for each read error
#.................................................
# EXECUTION TIME: Not relevant
#.................................................
#   Known problems:
#   - None
#.................................................