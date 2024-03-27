#.................................................
#   READ_SRUN.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This project file is needed to read the
#   SRUN(Single Run) file and to create the the
#   dataframe object.
#.................................................
import classes as classes_file #Module that contains the classes of the program
import bash_run as bash_run_file #Module that contains the bash run functions

def prompt_input_file(): #function to prompt the input file
    """This function prompts the input file and returns the input filename

    Returns:
        string: input_filename, the name of the input file
    """
    #.................................................
    #   This function prompts the input file and returns the input filename
    #.................................................
    #   INPUTS:
    #   None
    #.................................................
    #   OUTPUTS:
    #   input_filename: the name of the input file
    #.................................................
    #Variables:
    input_file_name = None #name of the input file
    print("Please input the name of the .srun file with the data:") #we ask the user to choose an input file
    input_file_name = input("Filename: ") 
    # we check if the extension is .xlsx, otherwise we throw an error
    if (input_file_name[-5:] != ".srun"): #if the extension is not .xlsx
        #We add the extension to the file name
        input_file_name = input_file_name+".srun"
    return input_file_name #we return the input filename

def read_srun(bash_run):
    """This function reads the dataframe from the srun file

    Inputs:
        bash_run: bool, True if the program is in bash mode, False otherwise
    
    Returns:
        string: df_object, the dataframe from the xlsx file
        string: output_filename, the name of the output file
    """
    #.................................................
    #   This function reads the dataframe from the xlsx file
    #.................................................
    #   INPUTS:
    #   bash_run: bool, True if the program is in bash mode, False otherwise
    #.................................................
    #   OUTPUTS:
    #   df:the dataframe from the xlsx file
    #   output_filename: the name of the output file
    #.................................................
    #Variables:
    P_TOL = 1e-3 #Tolerance for the pressure
    input_filename = None #name of the input file
    file = None #file object
    file_found = None #variable to check if the file is found, boolean
    line = None #line of the file
    p_dyn_used = None #Pdyn used, boolean
    p_stag_used = None #Pstag used, boolean
    #Variables to be read from the file
    #   -Inputs
    comment = None #Comment, string
    P = None #Pressure, float
    Pdyn = None #Dynamic pressure, float
    Pstag = None #Stagnation pressure, float
    q = None #Heat flux, float
    plasma_gas = None #Plasma gas, string
    #   -Conversion factors
    P_CF = None #Static pressure conversion factor, float
    PD_CF = None #Dynamic pressure conversion factor, float
    PS_CF = None #Stagnation pressure conversion factor, float  
    Q_CF = None #Heat flux conversion factor, float
    #   -Initial conditions
    T_0 = None #Initial static temperature, float
    Tt_0=None #Initial total temperature, float
    u_0 = None #Initial velocity, float
    Pt_0 = None #Initial total pressure, float
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
    #Variables to return
    df_object = classes_file.dataframe_xlsx_class() #I create the dataframe object to be returned
    output_filename = None #Name of the output file
    #I set the file_found variable to False
    file_found = False
    # we check if the program is in bash mode
    if (bash_run == True):
        input_filename = bash_run_file.retrieve_filename() #I retrieve the filename from the bash.pfs file
        try: #I try to read the file
            file = open(input_filename, "r") #I try to open the file
            file_found = True #If the file is found, we set the variable to True
            file.close() #I close the file
        except:
            print("Error: the file in bash.pfs does not exist or is not an .srun file")
            print("The program will continue in manual mode")
    #I ask for the input file
    while (file_found == False):
        input_filename = prompt_input_file() #I prompt the input file
        try: #I try to read the file
            file = open(input_filename, "r") #I try to open the file
            file_found = True #If the file is found, we set the variable to True
            file.close() #I close the file
            continue
        except:
            print("Error: the file does not exist or is not an .srun file")
            continue
    #I set the output filename
    output_filename = input_filename[:-5]+"_out.srun" #we set the output filename
    #Now I read the file
    file = open(input_filename, "r") #I open the file
    #INPUTS:
    file.readline() #I skip the first line
    #Comment:
    line = file.readline() #I read the line
    comment = line.split("=")[1].strip() #I save the comment
    #Pressure:
    line = file.readline() #I read the line
    P = float(line.split("=")[1].strip()) #I save the pressure
    #Dynamic pressure:
    p_dyn_used = False #I set the dynamic pressure used to False
    line = file.readline() #I read the line
    try:
        Pdyn = float(line.split("=")[1].strip()) #I save the dynamic pressure
        p_dyn_used = True #I set the dynamic pressure used to True
    except:
        pass
    #Stagnation pressure:
    p_stag_used = False #I set the stagnation pressure used to False
    line = file.readline() #I read the line
    try:
        Pstag = float(line.split("=")[1].strip()) #I save the stagnation pressure
        p_stag_used = True #I set the stagnation pressure used to True
    except:
        pass
    #Heat flux:
    line = file.readline() #I read the line
    q = float(line.split("=")[1].strip()) #I save the heat flux
    #Plasma gas:
    line = file.readline() #I read the line
    plasma_gas = line.split("=")[1].strip().lower() #I save the plasma gas
    match plasma_gas:
        case "air":
            plasma_gas = "air_13"
        case "n2":
            plasma_gas = "nitrogen2"
        case "nitrogen2":
            pass
        case "air_13":
            pass
        case "air_11":
            pass
        case _:
            raise Exception("ERROR: plasma gas not recognized")
    #Conversion factors:
    line = file.readline() #I skip the line
    #Static pressure conversion factor:
    line = file.readline() #I read the line
    P_CF = float(line.split("=")[1].strip()) #I save the static pressure conversion factor
    #Dynamic pressure conversion factor:
    line = file.readline() #I read the line
    if (p_dyn_used):    
        PD_CF = float(line.split("=")[1].strip()) #I save the dynamic pressure conversion factor
    #Stagnation pressure conversion factor:
    line = file.readline() #I read the line
    if (p_stag_used):
        PS_CF = float(line.split("=")[1].strip()) #I save the stagnation pressure conversion factor
    #Heat flux conversion factor:
    line = file.readline() #I read the line
    Q_CF = float(line.split("=")[1].strip()) #I save the heat flux conversion factor
    # P, Pdyn and Pstag:
    P *= P_CF
    if (p_dyn_used == True and p_stag_used == False):
        Pdyn = Pdyn*PD_CF
        Pstag = P+Pdyn
    elif (p_dyn_used == False and p_stag_used == True):
        Pstag = Pstag*PS_CF
        Pdyn = Pstag-P
    elif (p_dyn_used == True and p_stag_used == True):
        Pdyn = Pdyn*PD_CF
        Pstag = Pstag*PS_CF
        if (abs(Pstag-P-Pdyn)>P_TOL):
            raise Exception("ERROR: The pressure are inconsistent")
    else: 
        raise Exception("ERROR: The dynamic and stagnation pressure are not missing")
    if (P<=0 or Pdyn<=0 or Pstag<=0 or q<=0):
        raise Exception("ERROR: The inputs are invalid")
    #Initial conditions:
    line = file.readline() #I skip the line
    #Initial static temperature:
    line = file.readline() #I read the line
    T_0 = float(line.split("=")[1].strip()) #I save the initial static temperature
    #Initial total temperature:
    line = file.readline() #I read the line
    Tt_0 = float(line.split("=")[1].strip()) #I save the initial total temperature
    #Initial velocity:
    line = file.readline() #I read the line
    u_0 = float(line.split("=")[1].strip()) #I save the initial velocity
    #Initial total pressure:
    line = file.readline() #I read the line
    Pt_0 = float(line.split("=")[1].strip()) #I save the initial total pressure
    if (Pt_0 == 0):
        Pt_0 = Pstag
    if (T_0<=0 or Tt_0<=0 or u_0<=0 or Pt_0<=0):
        raise Exception("ERROR: The initial conditions are invalid")
    #Probes properties:
    line = file.readline() #I skip the line
    #Wall temperature:
    line = file.readline() #I read the line
    Tw = float(line.split("=")[1].strip()) #I save the wall temperature
    #Pitot external radius:
    line = file.readline() #I read the line
    Rp = float(line.split("=")[1].strip()) #I save the pitot external radius
    #Flux probe external radius:
    line = file.readline() #I read the line
    Rm = float(line.split("=")[1].strip()) #I save the flux probe external radius
    #Plasma jet radius:
    line = file.readline() #I read the line
    Rj = float(line.split("=")[1].strip()) #I save the plasma jet radius
    if (Tw<=0 or Rp<=0 or Rm<=0 or Rj<=0):
        raise Exception("ERROR: The probes properties are invalid")
    #Stagnation type:
    line = file.readline() #I read the line
    stagtype = line.split("=")[1].strip() #I save the stagnation type
    match stagtype:
        case "flat":
            stagtype = 0
        case _:
            raise Exception("ERROR: Stagnation type not recognized")
    #Heat flux law:
    line = file.readline() #I read the line
    hflaw = line.split("=")[1].strip() #I save the heat flux law
    match hflaw:
        case "exact":
            hflaw = 0
        case _:
            raise Exception("ERROR: Heat flux law not recognized")
    #Barker correction:
    line = file.readline() #I read the line
    barker = line.split("=")[1].strip() #I save the barker correction
    match barker:
        case "none":
            barker = 0
        case "homann":
            barker = 1
        case "carleton":
            barker = 2
        case _:
            raise Exception("ERROR: Barker correction not recognized")
    #Settings:
    line = file.readline() #I skip the line
    #Number of point for the boundary layer eta discretization:
    line = file.readline() #I read the line
    p = int(line.split("=")[1].strip()) #I save the number of point for the boundary layer eta discretization
    #Maximum number of iterations for the heat flux:
    line = file.readline() #I read the line
    max_hf_iter = int(line.split("=")[1].strip()) #I save the maximum number of iterations for the heat flux
    #Convergence criteria for the heat flux:
    line = file.readline() #I read the line
    hf_conv = float(line.split("=")[1].strip()) #I save the convergence criteria for the heat flux
    #Use previous iteration for the heat transfer:
    line = file.readline() #I read the line
    use_prev_ite = line.split("=")[1].strip() #I save the use previous iteration for the heat transfer
    match use_prev_ite:
        case "yes":
            use_prev_ite = 1
        case "no":
            use_prev_ite = 0
        case _:
            raise Exception("ERROR: Use previous iteration for the heat transfer not recognized")
    #Convergence criteria for the newton solver:
    line = file.readline() #I read the line
    newton_conv = float(line.split("=")[1].strip()) #I save the convergence criteria for the newton solver
    #Maximum number of iterations for the newton solver:
    line = file.readline() #I read the line
    max_newton_iter = int(line.split("=")[1].strip()) #I save the maximum number of iterations for the newton solver
    #Main newton jacobian finite difference epsilon:
    line = file.readline() #I read the line
    jac_diff = float(line.split("=")[1].strip()) #I save the main newton jacobian finite difference epsilon
    #Maximum value for the temperature used for relaxation:
    line = file.readline() #I read the line
    max_T_relax = float(line.split("=")[1].strip()) #I save the maximum value for the temperature used for relaxation
    #Minimum value for the temperature used for relaxation:
    line = file.readline() #I read the line
    min_T_relax = float(line.split("=")[1].strip()) #I save the minimum value for the temperature used for relaxation
    #log warning for when the heat flux does not converge:
    line = file.readline() #I read the line
    log_warning_hf = line.split("=")[1].strip()
    match log_warning_hf:
        case "yes":
            log_warning_hf = 1
        case "no":
            log_warning_hf = 0
        case _:
            raise Exception("ERROR: Log warning for when the heat flux does not converge not recognized")
    #Maximum value for the boundary layer eta:
    line = file.readline() #I read the line
    eta_max = float(line.split("=")[1].strip()) #I save the maximum value for the boundary layer eta
    #I close the file
    file.close()    
    #I now save the variables in the dataframe object
    df_object.n = 1 #Number of cases, integer
    df_object.comment = comment #Comment, string
    df_object.P = P #Pressure, float
    df_object.Pdyn = Pdyn #Dynamic pressure, float
    df_object.Pstag = Pstag #Stagnation pressure, float
    df_object.q = q #Heat flux, float
    df_object.plasma_gas = plasma_gas #Plasma gas, string
    df_object.P_CF = P_CF #Static pressure conversion factor, float
    df_object.PD_CF = PD_CF #Dynamic pressure conversion factor, float
    df_object.PS_CF = PS_CF #Stagnation pressure conversion factor, float
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