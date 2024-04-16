#.................................................
#   READ_XLSX.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to read the
#   dataframe from a xlsx file.
#.................................................
import pandas as pd  # Library to read the xlsx file
import classes as classes_file  # Module that contains the classes used in the program
import bash_run as bash_run_file  # Module for the bash run

def prompt_input_file():
    """This function prompts the user and 
    returns the input filename.

    Returns:
        input_filename (string): the name of the input file
    """
    #Variables:
    input_file_name = None  # Input filename to return
    print("Please input the name of the xlsx file with the data.")
    input_file_name = input("Filename: ") 
    # I check if the extension is .xlsx, otherwise I add it
    if (input_file_name.endswith(".xlsx") == False): 
        input_file_name = input_file_name + ".xlsx"
    return input_file_name

def read_xlsx(bash_run):
    """This function reads the dataframe from the xlsx file.
    
    Args:
        bash_run (boolean): True if the bash.pfs file is present, False otherwise    

    Returns:
        df_object (dataframe_class): the dataframe from the xlsx file
        output_filename (string): the name of the output file
    """
    #Variables:
    input_filename = None  # Input filename
    df = None  # The dataframe object from Pandas
    df_dropped = None  # The dataframe from which we extract the data
    file_found = None  # Variable to check if the file is found (boolean)
    #Variables to be read:
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
    #Variables to return
    df_object = classes_file.dataframe_class()  # The dataframe object to be returned
    output_filename = None  # The output filename
    # Start:
    file_found = False
    if (bash_run == True):  # If we are in bash mode
        input_filename = bash_run_file.retrieve_filename()  # I retrieve the filename from the bash.pfs file
        try:  # If we can read the file:
            df = pd.read_excel(input_filename, engine="openpyxl", header=[0,1])
            file_found = True 
        except:  # If we cannot read the file:
            print("Error: the file in bash.pfs does not exist or is not an xlsx file.")
            print("The program will continue in manual mode.")
    # If we are not in bash mode or the file is not found:
    while (file_found == False):
        input_filename = prompt_input_file()
        try:  # If we can read the file:
            df = pd.read_excel(input_filename, engine="openpyxl", header=[0,1])
            file_found = True
        except:
            print("Error: the file does not exist or is not an xlsx file.")
    output_filename = input_filename[:-5]+"_out.xlsx"  # I set the output filename
    # DATA EXTRACTION:
    # If the excel is multiindex on the rows, I drop the first row level
    try: 
        df_dropped = df.droplevel(level=0, axis=1)  # I drop the first row level
    except:
        df_dropped = df
    n = df_dropped.shape[0]  # Number of the test
    # INPUTS:
    # comment:
    comment = df_dropped['comment']
    # Pressure:
    P = df_dropped['P']
    # Dynamic pressure:
    P_dyn = df_dropped['P_dyn']
    # Stagnation pressure:
    P_stag = df_dropped['P_stag']
    # Heat flux:
    q_target = df_dropped['q_target']
    # Plasma gas:
    plasma_gas = df_dropped['plasma_gas']
    # INPUT CONVERSION FACTOR
    #Static pressure conversion factor:
    P_CF = df_dropped['P_CF']
    # Dynamic pressure conversion factor:
    P_dyn_CF = df_dropped['P_dyn_CF']
    # Stagnation pressure conversion factor:
    P_stag_CF = df_dropped['P_stag_CF']
    # Heat flux conversion factor:
    q_CF = df_dropped['q_CF']
    # INITIAL CONDITIONS
    # Initial conditions database name:
    ic_db_name = df_dropped['ic_db_name']
    # Initial static temperature:
    T_0 = df_dropped['T_0']
    # Initial total temperature:
    T_t_0 = df_dropped['T_t_0']
    # Initial velocity:
    u_0 = df_dropped['u_0']
    # Initial total pressure:
    P_t_0 = df_dropped['P_t_0']
    # PROBE SETTINGS
    #Wall temperature:
    T_w = df_dropped['T_w']
    # Pitot external radius:
    R_p = df_dropped['R_p'] 
    # Heat flux probe external radius:
    R_m = df_dropped['R_m'] 
    # Plasma jet radius:
    R_j = df_dropped['R_j'] 
    # Stagnation type:
    stag_type = df_dropped['stag_type'] 
    # Heat flux law:
    hf_law = df_dropped['hf_law'] 
    # Barker's correction type:
    barker_type = df_dropped['barker_type'] 
    # PROGRAM SETTINGS
    # Number of point for the boundary layer eta discretization:
    N_p = df_dropped['N_p']
    # Maximum number of iterations for the heat flux:
    max_hf_iter = df_dropped['max_hf_iter']
    # Convergence criteria for the heat flux:
    hf_conv = df_dropped['hf_conv']
    # Use previous iteration for the heat transfer:
    use_prev_ite = df_dropped['use_prev_ite'] 
    # Upper integration boundary for the normal coordinate of the boundary layer:
    eta_max = df_dropped['eta_max']
    # Log warning heat flux:
    log_warning_hf = df_dropped['log_warning_hf']
    # Convergence criteria for the Newton solver:
    newton_conv = df_dropped['newton_conv'] 
    # Maximum number of iterations for the Newton solver:
    max_newton_iter = df_dropped['max_newton_iter']
    # Jacobian finite difference epsilon:
    jac_diff = df_dropped['jac_diff']
    # Minimum value for the temperature used for relaxation:
    min_T_relax = df_dropped['min_T_relax'] 
    # Maximum value for the temperature used for relaxation:
    max_T_relax = df_dropped['max_T_relax']
    # I store the values in the dataframe object
    df_object.n = n
    df_object.comment = comment
    df_object.P = P
    df_object.P_dyn = P_dyn
    df_object.P_stag = P_stag
    df_object.q_target = q_target
    df_object.plasma_gas = plasma_gas
    df_object.P_CF = P_CF
    df_object.P_dyn_CF = P_dyn_CF
    df_object.P_stag_CF = P_stag_CF
    df_object.q_CF = q_CF
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