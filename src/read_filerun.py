#.................................................
#   READ_FILERUN.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This project file is needed to read the
#   FILERUN(File Run) file and to create the the
#   dataframe object.
#.................................................
import classes as classes_file #Module that contains the classes of the program

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
    print("Please input the name of the .in file with the data:") #we ask the user to choose an input file
    input_file_name = input("Filename: ") 
    # we check if the extension is .xlsx, otherwise we throw an error
    if (input_file_name[-3:] != ".in"): #if the extension is not .xlsx
        #We add the extension to the file name
        input_file_name = input_file_name+".in"
    return input_file_name #we return the input filename

def prompt_settings_file(): #function to prompt the input file
    """This function prompts the settings file and returns the settings filename

    Returns:
        string: settings_filename, the name of the input file
    """
    #.................................................
    #   This function prompts the settings file and returns the settings filename
    #.................................................
    #   INPUTS:
    #   None
    #.................................................
    #   OUTPUTS:
    #   settings_filename: the name of the settings file
    #.................................................
    #Variables:
    settings_file_name = None #name of the input file
    print("Please input the name of the .pfs file with the settings:") #we ask the user to choose a settings file
    settings_file_name = input("Filename: ") 
    # we check if the extension is .pfs, otherwise we add it
    if (settings_file_name[-4:] != ".pfs"): #if the extension is not .xlsx
        #We add the extension to the file name
        settings_file_name = settings_file_name+".pfs"
    return settings_file_name #we return the input filename

def read_filerun():
    """This function reads the dataframe from the .in file

    Returns:
        string: df_object, the dataframe from the xlsx file
        string: output_filename, the name of the output file
    """
    #.................................................
    #   This function reads the dataframe from the xlsx file
    #.................................................
    #   INPUTS:
    #   None.
    #.................................................
    #   OUTPUTS:
    #   df:the dataframe from the xlsx file
    #   output_filename: the name of the output file
    #.................................................
    #Variables:
    input_filename = None #name of the input file
    settings_filename = None #name of the settings file
    input_file = None #file object
    settings_file = None #file object
    file_found = None #variable to check if the file is found, boolean
    line = None #line of the file
    #Variables to be read from the file
    #   -Inputs
    comment = None #Comment, string
    P = None #Pressure, float
    Pdyn = None #Dynamic pressure, float
    q = None #Heat flux, float
    #   -Conversion factors
    P_CF = None #Static pressure conversion factor, float
    PD_CF = None #Dynamic pressure conversion factor, float  
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
    plasma_gas = None #Plasma gas, string
    p = None #Number of point for the boundary layer eta discretization, integer
    max_hf_iter = None #Maximum number of iterations for the heat flux, integer
    hf_conv = None #Convergence criteria for the heat flux, float
    use_prev_ite = None #Use previous iteration for the heat transfer, string
    newton_conv = None #Convergence criteria for the newton solver, float
    max_newton_iter = None #Maximum number of iterations for the newton solver, integer
    jac_diff = None #Main newton jacobian finite difference epsilon, float
    max_T_relax = None #Maximum value for the temperature used for relaxation, float
    min_T_relax = None #Minimum value for the temperature used for relaxation, float
    #Variables to return
    df_object = classes_file.dataframe_xlsx_class() #I create the dataframe object to be returned
    output_filename = None #Name of the output file
    #I set the file_found variable to False
    file_found = False
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
    output_filename = input_filename[:-3]+".out" #we set the output filename
    #I read the settings filename
    file_found = False #I set the file_found variable to False
    while (file_found == False):
        settings_filename = prompt_settings_file()
        try:
            file = open(settings_filename, "r") #I try to open the file
            file_found = True #If the file is found, we set the variable to True
            file.close() #I close the file
            continue
        except:
            print("Error: the file does not exist or is not an .pfs file")
            continue
    #Now I read the settings file
    settings_file = open(settings_filename, "r") #I open the file
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
        P.append(float(line[20:40].strip().replace("d","e"))) #I save the pressure
        Pdyn.append(float(line[40:60].strip().replace("d","e"))) #I save the dynamic pressure
        q.append(float(line[60:80].strip().replace("d","e"))) #I save the heat flux
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