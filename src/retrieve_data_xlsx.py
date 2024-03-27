#.................................................
#   RETRIEVE_DATA_XLSX.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This project file is needed to retrieve the needed
#   data from the dataframe object from the current loop
#   iteration
#.................................................
import numpy as np #Library for numerical operations
import classes as classes_file #Module with classes
import mutationpp as mpp #Library for the thermodynamic properties
import pandas as pd #Library for the dataframe
def generate_std_file(FILENAME):
    """This function generate the standard values file if it does not exist 
    or is invalid.
    """
    #.................................................
    #   This function generate the standard values file if it does not exist
    #   or is invalid.
    #.................................................
    #   INPUTS:
    #   FILENAME: the filename for the standard values
    #.................................................
    #   OUTPUTS:
    #   None
    #.................................................
    file = open(FILENAME, "w") #Open the file
    file.write("plasma_gas = air13\n") #Plasma gas, string
    file.write("P_CF = 1e0\n") #Static pressure conversion factor, float
    file.write("PD_CF = 1e0\n") #Dynamic pressure conversion factor, float
    file.write("PS_CF = 1e0\n") #Stagnation pressure conversion factor, float
    file.write("Q_CF = 1e3\n") #Heat flux conversion factor, float
    file.write("T_0 = 1000\n") #Initial temperature, float
    file.write("Tt_0 = 2000\n") #Initial total temperature, float
    file.write("u_0 = 300\n") #Initial velocity, float
    file.write("Pt_0 = 0\n") #Initial total pressure, float
    file.write("Tw = 400\n") #Wall temperature, float
    file.write("Rp = 4e-3\n") #Pitot external radius, float
    file.write("Rm = 10.1e-3\n") #Flux probe external radius, float
    file.write("Rj = 50e-3\n") #Plasma jet radius, float
    file.write("stagtype = 0\n") #Stagnation type, string->integer
    file.write("hflaw = 0\n") #Heat flux law, string->integer
    file.write("barker = 0\n") #Barker correct, string->integer
    file.write("p = 251\n") #Number of point for the boundary layer eta discretization, integer
    file.write("max_hf_iter = 100\n") #Maximum number of iterations for the heat transfer, integer
    file.write("hf_conv = 1e-4\n") #Convergence criteria for the heat transfer, float
    file.write("use_prev_ite = 1\n") #Use previous iteration for the heat transfer, string
    file.write("newton_conv = 1e-8\n") #Convergence criteria for the newton solver, float
    file.write("max_newton_iter = 30\n") #Maximum number of iterations for the newton solver, integer
    file.write("jac_diff = 1e-2\n") #Main newton jacobian finite difference epsilon, float
    file.write("max_T_relax = 18000\n") #Maximum value for the temperature used for relaxation, float
    file.write("min_T_relax = 200\n") #Minimum value for the temperature used for relaxation, float
    file.write("log_warning_hf = 1\n") #Log warning for the heat flux, string
    file.write("eta_max = 6\n") #Maximum value for the boundary layer eta, float
    file.close() #Close the file
    return None
def read_file(FILENAME):
    """This function reads the standard values file and returns the dataframe object
    Args:
        FILENAME (str): the filename for the standard values

    Returns:
        df (dataframe_xlsx_class): the dataframe object
    """
    #.................................................
    #   This function reads the standard values file and returns the dataframe object
    #.................................................
    #   INPUTS:
    #   FILENAME: the filename for the standard values
    #.................................................
    #   OUTPUTS:
    #   df: the dataframe object
    #.................................................
    df = classes_file.dataframe_xlsx_class() #create the dataframe object
    file = open(FILENAME, "r") #Open the file
    line = file.readline() #Read the line
    df.plasma_gas = line.split(" = ")[1].strip() #Plasma gas, string
    line = file.readline() #Read the line
    df.P_CF = float(line.split(" = ")[1].strip()) #Static pressure conversion factor, float
    line = file.readline() #Read the line
    df.PD_CF = float(line.split(" = ")[1].strip()) #Dynamic pressure conversion factor, float
    line = file.readline() #Read the line
    df.PS_CF = float(line.split(" = ")[1].strip()) #Stagnation pressure conversion factor, float
    line = file.readline() #Read the line
    df.Q_CF = float(line.split(" = ")[1].strip()) #Heat flux conversion factor, float
    line = file.readline() #Read the line
    df.T_0 = float(line.split(" = ")[1].strip()) #Initial temperature, float
    line = file.readline() #Read the line
    df.Tt_0 = float(line.split(" = ")[1].strip()) #Initial total temperature, float
    line = file.readline() #Read the line
    df.u_0 = float(line.split(" = ")[1].strip()) #Initial velocity, float
    line = file.readline() #Read the line
    df.Pt_0 = float(line.split(" = ")[1].strip()) #Initial total pressure, float
    line = file.readline() #Read the line
    df.Tw = float(line.split(" = ")[1].strip()) #Wall temperature, float
    line = file.readline() #Read the line
    df.Rp = float(line.split(" = ")[1].strip()) #Pitot external radius, float
    line = file.readline() #Read the line
    df.Rm = float(line.split(" = ")[1].strip()) #Flux probe external radius, float
    line = file.readline() #Read the line
    df.Rj = float(line.split(" = ")[1].strip()) #Plasma jet radius, float
    line = file.readline() #Read the line
    df.stagtype = int(line.split(" = ")[1].strip()) #Stagnation type, string->integer
    line = file.readline() #Read the line
    df.hflaw = int(line.split(" = ")[1].strip()) #Heat flux law, string->integer
    line = file.readline() #Read the line
    df.barker = int(line.split(" = ")[1].strip()) #Barker correct, string->integer
    line = file.readline() #Read the line
    df.p = int(line.split(" = ")[1].strip()) #Number of point for the boundary layer eta discretization, integer
    line = file.readline() #Read the line
    df.max_hf_iter = int(line.split(" = ")[1].strip()) #Maximum number of iterations for the heat transfer, integer
    line = file.readline() #Read the line
    df.hf_conv = float(line.split(" = ")[1].strip()) #Convergence criteria for the heat transfer, float
    line = file.readline() #Read the line
    df.use_prev_ite = int(line.split(" = ")[1].strip()) #Use previous iteration for the heat transfer, string
    line = file.readline() #Read the line
    df.newton_conv = float(line.split(" = ")[1].strip()) #Convergence criteria for the newton solver, float
    line = file.readline() #Read the line
    df.max_newton_iter = int(line.split(" = ")[1].strip()) #Maximum number of iterations for the newton solver, integer
    line = file.readline() #Read the line
    df.jac_diff = float(line.split(" = ")[1].strip()) #Main newton jacobian finite difference epsilon, float
    line = file.readline() #Read the line
    df.max_T_relax = float(line.split(" = ")[1].strip()) #Maximum value for the temperature used for relaxation, float
    line = file.readline() #Read the line
    df.min_T_relax = float(line.split(" = ")[1].strip()) #Minimum value for the temperature used for relaxation, float
    line = file.readline() #Read the line
    df.log_warning_hf = int(line.split(" = ")[1].strip()) #Log warning for the heat flux, string
    line = file.readline() #Read the line
    df.eta_max = float(line.split(" = ")[1].strip()) #Maximum value for the boundary layer eta, float
    file.close() #Close the file
    return df
def read_std_values():
    """This function reads the standard values file and returns the dataframe object

    Returns:
        df (dataframe_xlsx_class): the dataframe object
    """
    #.................................................
    #   This function reads the standard values file and returns the dataframe object
    #.................................................
    #   INPUTS:
    #   None
    #.................................................
    #   OUTPUTS:
    #   df: the dataframe object
    #.................................................
    # Variables:
    FILENAME = "std_values.pfs" #Filename for the standard values
    file = None
    df = classes_file.dataframe_xlsx_class() #create the dataframe object
    #We check if the file exists
    try:
        file = open(FILENAME, "r") #Open the file
        file.close() #Close the file
    except:
        generate_std_file(FILENAME) 
    #We try read the file
    try:
        df = read_file(FILENAME)
    except: #If the file is not valid, we generate a new one
        generate_std_file(FILENAME)
        df = read_file(FILENAME)
    return df
    
    
def is_valid_data(x):
    """Let us understand if the data is valid

    Args:
        x (float): the data to check

    Returns:
        bool: true if the data is valid, false otherwise
    """
    if (pd.isna(x) or ( (isinstance(x, np.int64) == False) and (isinstance(x, np.float64) == False) ) or x <= 0):
        return False
    else:
        return True

def retrieve_data(df,ncase):
    """This function retrieves the needed data from the dataframe object from the current loop iteration

    Args:
        df (dataframe_xlsx_class): the dataframe object
        ncase (int): the number of the case

    Returns:
        inputs_class: the inputs object containing the inputs
        initials_class: the initials object containing the initials
        probes_class: the probes object containing the probes
        settings_class: the settings object containing the settings
    """
    #.................................................
    #   This function retrieves the needed data from the dataframe object from the current loop iteration
    #   We retrieve the "ncase"-th line from the dataframe and we return the needed data
    #.................................................
    #   INPUTS:
    #   df: the dataframe object
    #   ncase: the number of the case
    #.................................................
    #   OUTPUTS:
    #   -inputs_object: the inputs object containing the inputs
    #   -initials_object: the initials object containing the initials
    #   -probes_object: the probes object containing the probes
    #   -settings_object: the settings object containing the settings
    #.................................................
    # Variables:
    std_values = classes_file.dataframe_xlsx_class() #create the dataframe object
    MM_TO_M = 1e-3 #Conversion factor from mm to m, float
    P_eps = 1e-3 #Pressure epsilon, float
    l = None #Ratio between the flux probe external radius and the plasma jet radius, float
    den = None #Denominator for the stagnation variable, float
    #   -Inputs
    comment = None #Comment, string
    P = None #Pressure, float
    Pdyn = None #Dynamic pressure, float
    Pstag = None #Stagnation pressure, float
    P_used = None #Pressure used, string
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
    stagvar = None #Stagnation variable, float
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
    log_warning_hf = None #Log warning for the heat flux, string
    eta_max = None #Maximum value for the boundary layer eta, float
    # Variables to return
    inputs_object = classes_file.inputs_class() #create the inputs object
    initials_object = classes_file.initials_class() #create the initials object
    probes_object = classes_file.probes_class() #create the probes object
    settings_object = classes_file.settings_class() #create the settings object
    warnings = []
    # Inputs:
    warnings = "None|"
    # We read the std values:
    std_values = read_std_values()
    # Comment
    comment = df.comment[ncase] #Comment, string
    if (pd.isna(comment) or comment==None or comment==""):
        inputs_object.comment = "Case "+str(ncase) #We add the case number to the comment
    else:
        inputs_object.comment = comment
    # Pressure:
    P = df.P[ncase] #Pressure, float
    if (is_valid_data(P) == False):
        raise ValueError("Error: The pressure value is not valid")
    else:
        inputs_object.P = df.P[ncase] #Pressure, float
    # Dynamic pressure:
    Pdyn = df.Pdyn[ncase] #Dynamic pressure, float
    # Stagnation pressure:
    Pstag = df.Pstag[ncase] #Stagnation pressure, float
    if (is_valid_data(Pstag) == False):
        if (is_valid_data(Pdyn) == False):
            raise ValueError("Error: The stagnation pressure or dynamic value is not valid")
        else:
            P_used = "Pdyn"
    elif (is_valid_data(Pdyn) == False):
        P_used = "Pstag"
    else:
        P_used = "Both"
    # Heat flux:
    q = df.q[ncase] #Heat flux, float
    if(is_valid_data(q) == False):
        raise ValueError("Error: The heat flux value is not valid")
    else:
        inputs_object.q = df.q[ncase] #Heat flux, float
    # Plasma gas:
    plasma_gas = df.plasma_gas[ncase] #Plasma gas, string
    plasma_gas = plasma_gas.lower() #We convert the string to lower case
    if (pd.isna(plasma_gas) or plasma_gas==None or plasma_gas==""):
        raise ValueError("Error: The plasma gas value is not valid")
    match plasma_gas:
        case "n2":
            inputs_object.plasma_gas = "nitrogen2"
        case "air":
            inputs_object.plasma_gas = "air_13"
        case "nitrogen2":
            inputs_object.plasma_gas = "nitrogen2"
        case "air_13":
            inputs_object.plasma_gas = "air_13"
        case "air_11":
            inputs_object.plasma_gas = "air_11"
        case _:
            inputs_object.plasma_gas = std_values.plasma_gas #We set the default value
            warnings += "Plasma gas invalid, set to STD|"
    try:
        mpp.Mixture(inputs_object.plasma_gas) #We check if the mixture is valid
    except:
        raise ValueError("Error: The plasma gas value is not valid or is in an invalid folder")
    # Conversion factors:
    P_CF = df.P_CF[ncase] #Static pressure conversion factor, float
    if (is_valid_data(P_CF) == False):
        inputs_object.P_CF = std_values.P_CF #We set the default value
        warnings += "P_CF invalid, set to STD|"
    else:
        inputs_object.P_CF = df.P_CF[ncase] #Static pressure conversion factor, float
    inputs_object.P *= inputs_object.P_CF #We convert the pressure to the right unit
    match P_used:
        case "Pdyn":
            PD_CF = df.PD_CF[ncase] #Dynamic pressure conversion factor, float
            if (is_valid_data(PD_CF) == False):
                inputs_object.PD_CF = std_values.PD_CF #We set the default value
                warnings += "PD_CF invalid, set to STD|"
            else:
                inputs_object.PD_CF = PD_CF #Dynamic pressure conversion factor, float
            inputs_object.Pdyn = Pdyn*inputs_object.PD_CF #We convert the dynamic pressure to the right unit
            inputs_object.Pstag = inputs_object.Pdyn + inputs_object.P #We calculate the stagnation pressure
        case "Pstag":
            PS_CF = df.PS_CF[ncase] #Stagnation pressure conversion factor, float
            if (is_valid_data(PS_CF) == False):
                inputs_object.PS_CF = std_values.PS_CF #We set the default value
                warnings += "PS_CF invalid, set to STD|"
            else:
                inputs_object.PS_CF = PS_CF #Dynamic pressure conversion factor, float
            inputs_object.Pstag = Pstag*inputs_object.PS_CF #We convert the dynamic pressure to the right unit
            inputs_object.Pdyn = inputs_object.Pstag - inputs_object.P #We calculate the stagnation pressure
        case "Both":
            PD_CF = df.PD_CF[ncase] #Dynamic pressure conversion factor, float
            if (is_valid_data(PD_CF) == False):
                inputs_object.PD_CF = std_values.PD_CF #We set the default value
                warnings += "PD_CF invalid, set to STD|"
            else:
                inputs_object.PD_CF = PD_CF #Dynamic pressure conversion factor, float
            PS_CF = df.PS_CF[ncase] #Stagnation pressure conversion factor, float
            if (is_valid_data(PS_CF) == False):
                inputs_object.PS_CF = std_values.PS_CF #We set the default value
                warnings += "PS_CF invalid, set to STD|"
            else:
                inputs_object.PS_CF = PS_CF #Dynamic pressure conversion factor, float
            inputs_object.Pdyn = Pdyn*inputs_object.PD_CF #We convert the dynamic pressure to the right unit
            inputs_object.Pstag = Pstag*inputs_object.PS_CF #We convert the dynamic pressure to the right unit
            if (abs(inputs_object.Pstag-inputs_object.P - inputs_object.Pdyn) > P_eps):
                raise ValueError("Error: The stagnation pressure and dynamic pressure values are not consistent")
    Q_CF = df.Q_CF[ncase] #Heat flux conversion factor, float
    if (is_valid_data(Q_CF) == False):
        inputs_object.Q_CF = std_values.Q_CF #We set the default value
        warnings += "Q_CF invalid, set to STD|"
    else:
        inputs_object.Q_CF = df.Q_CF[ncase] #Heat flux conversion factor, float
    inputs_object.q *= inputs_object.Q_CF #We convert the heat flux to the right unit
    # Initials:
    T_0 = df.T_0[ncase] #Initial temperature, float
    if (is_valid_data(T_0) == False):
        initials_object.T_0 = std_values.T_0 #We set the default value
        warnings += "T_0 invalid, set to STD|"
    else:
        initials_object.T_0=df.T_0[ncase] #Initial temperature, float
    Tt_0=df.Tt_0[ncase] #Initial total temperature, float
    if (is_valid_data(Tt_0) == False):
        initials_object.Tt_0 = std_values.Tt_0
        warnings += "Tt_0 invalid, set to STD|"
    else:
        initials_object.Tt_0=df.Tt_0[ncase] #Initial total temperature, float
    u_0=df.u_0[ncase] #Initial velocity, float
    if (is_valid_data(u_0) == False):
        initials_object.u_0 = std_values.u_0
        warnings += "u_0 invalid, set to STD|"
    else:
        initials_object.u_0=df.u_0[ncase] #Initial velocity, float
    Pt_0 = df.Pt_0[ncase] #Initial total pressure, float
    if (is_valid_data(Pt_0) == False):
        if (Pt_0 == 0):
            initials_object.Pt_0 = inputs_object.Pstag
        else:
            initials_object.Pt_0 = std_values.Pt_0
            if (initials_object.Pt_0 == 0):
                initials_object.Pt_0 = inputs_object.Pstag
            warnings += "Pt_0 invalid, set to STD|"
    else:
        initials_object.Pt_0=df.Pt_0[ncase] #Initial total pressure, float
    # Probes:
    Tw = df.Tw[ncase] #Wall temperature, float
    if (is_valid_data(Tw) == False):
        probes_object.Tw = std_values.Tw
        warnings += "Tw invalid, set to STD|"
    else:
        probes_object.Tw=df.Tw[ncase] #Wall temperature, float
    Rp = df.Rp[ncase] #Pitot external radius, float
    if (is_valid_data(Rp) == False):
        probes_object.Rp = std_values.Rp
        warnings += "Rp invalid, set to STD|"
    else:
        probes_object.Rp=df.Rp[ncase] * MM_TO_M #Pitot external radius, float
    Rm = df.Rm[ncase] #Flux probe external radius, float
    if (is_valid_data(Rm) == False):
        probes_object.Rm = std_values.Rm
        warnings += "Rm invalid, set to STD|"
    else:
        probes_object.Rm=df.Rm[ncase] * MM_TO_M #Flux probe external radius, float
    Rj = df.Rj[ncase] #Plasma jet radius, float
    if (is_valid_data(Rj) == False):
        probes_object.Rj = std_values.Rj
        warnings += "Rj invalid, set to STD|"
    else:
        probes_object.Rj=df.Rj[ncase] * MM_TO_M #Plasma jet radius, float
    stagtype = df.stagtype[ncase] #Stagnation type, string->integer
    if (pd.isna(stagtype)):
        probes_object.stagtype = std_values.stagtype
        warnings += "stagtype invalid, set to STD|"
    else:
        match stagtype:
            case "flat":
                probes_object.stagtype = 0
            case _:
                probes_object.stagtype = std_values.stagtype
                warnings += "stagtype invalid or not yet implemented, set to STD|"
    hflaw = df.hflaw[ncase] #Heat flux law, string->integer
    if (pd.isna(hflaw)):
        probes_object.hflaw = std_values.hflaw
        warnings += "hflaw invalid, set to STD|"
    else:
        match hflaw:
            case "exact":
                probes_object.hflaw = 0
            case _:
                probes_object.hflaw = std_values.hflaw
                warnings += "hflaw invalid or not yet implemented, set to STD|"
    barker = df.barker[ncase] #Barker correct, string->integer
    if (pd.isna(barker)):
        probes_object.barker = std_values.barker
        warnings += "barker invalid, set to STD|"
    else:
        match barker:
            case "none":
                probes_object.barker = 0
            case "homann":
                probes_object.barker = 1
            case "carleton":
                probes_object.barker = 2
            case _:
                probes_object.barker = std_values.barker
                warnings += "barker invalid or not yet implemented, set to STD|"
    match probes_object.stagtype:
        case 0:
            l=Rm/Rj
            if(l<=1):
                den=2-l-1.68*pow((l-1),2)-1.28*pow((l-1),3)
                stagvar=1/den
            else:
                stagvar=1
        case _:
            raise ValueError("Error: Check the code, you should not be here")
    probes_object.stagvar=stagvar #Stagnation variable, float
    # Barker and Pt_0 check:
    if (probes_object.barker == 0 and initials_object.Pt_0 != inputs_object.Pstag):
        initials_object.Pt_0 = inputs_object.Pstag
        warnings += "Pt_0 not consistent with the barker correction, set to Pstag|"
    # Settings:
    p = df.p[ncase] #Number of point for the boundary layer eta discretization, integer
    if (is_valid_data(p) == False):
        settings_object.p = std_values.p
        warnings += "p invalid, set to STD|"
    else:
        if(int(p)==p):
            settings_object.p=int(df.p[ncase]) #Number of point for the boundary layer eta discretization, integer
        else:
            settings_object.p = std_values.p
            warnings += "p invalid, set to STD|"
    max_hf_iter = df.max_hf_iter[ncase] #Maximum number of iterations for the heat transfer
    if (is_valid_data(max_hf_iter) == False):
        settings_object.max_hf_iter = std_values.max_hf_iter
        warnings += "max_hf_iter invalid, set to STD|"
    else:
        if(int(max_hf_iter)==max_hf_iter):
            settings_object.max_hf_iter=df.max_hf_iter[ncase] #Maximum number of iterations for the heat transfer
        else:
            settings_object.max_hf_iter = std_values.max_hf_iter
            warnings += "max_hf_iter invalid, set to STD|"
    hf_conv = df.hf_conv[ncase] #Convergence criteria for the heat transfer
    if (pd.isna(hf_conv) or (isinstance(hf_conv, np.float64) == False) or hf_conv<=0):
        settings_object.hf_conv = std_values.hf_conv
        warnings += "hf_conv invalid, set to STD|"
    else:
        settings_object.hf_conv=df.hf_conv[ncase] #Convergence criteria for the heat transfer
    use_prev_ite = df.use_prev_ite[ncase] #Use previous iteration for the heat transfer
    if (pd.isna(use_prev_ite)):
        settings_object.use_prev_ite = std_values.use_prev_ite
        warnings += "use_prev_ite invalid, set to STD|"
    else:
        use_prev_ite = use_prev_ite.lower() #We convert the string to lower case
        match use_prev_ite:
            case "yes":
                settings_object.use_prev_ite = 1
            case "no":
                settings_object.use_prev_ite = 0
            case _:
                settings_object.use_prev_ite = std_values.use_prev_ite
                warnings += "use_prev_ite invalid, set to STD|"
    newton_conv = df.newton_conv[ncase] #Convergence criteria for the newton solver
    if (pd.isna(newton_conv) or (isinstance(newton_conv, np.float64) == False) or newton_conv<=0):
        settings_object.newton_conv = std_values.newton_conv
        warnings += "newton_conv invalid, set to STD|"
    else:
        settings_object.newton_conv=df.newton_conv[ncase] #Convergence criteria for the newton solver
    max_newton_iter = df.max_newton_iter[ncase] #Maximum number of iterations for the newton solver
    if (is_valid_data(max_newton_iter) == False):
        settings_object.max_newton_iter = std_values.max_newton_iter
        warnings += "max_newton_iter invalid, set to STD|"
    else:
        if(int(max_newton_iter)==max_newton_iter):
            settings_object.max_newton_iter=df.max_newton_iter[ncase] #Maximum number of iterations for the newton solver
        else:
            settings_object.max_newton_iter = std_values.max_newton_iter
            warnings += "max_newton_iter invalid, set to STD|"
    jac_diff = df.jac_diff[ncase] #Main newton jabobian finite difference epsilon
    if (pd.isna(jac_diff) or (isinstance(jac_diff, np.float64) == False) or jac_diff<=0):
        settings_object.jac_diff = std_values.jac_diff
        warnings += "jac_diff invalid, set to STD|"
    else:
        settings_object.jac_diff=df.jac_diff[ncase] #Main newton jabobian finite difference epsilon
    max_T_relax = df.max_T_relax[ncase] #Maximum value for the temperature used for relaxation
    if (is_valid_data(max_T_relax) == False):
        settings_object.max_T_relax = std_values.max_T_relax
        warnings += "max_T_relax invalid, set to STD|"
    else:
        settings_object.max_T_relax=df.max_T_relax[ncase] #Maximum value for the temperature used for relaxation
    min_T_relax = df.min_T_relax[ncase] #Minimum value for the temperature used for relaxation
    if (is_valid_data(min_T_relax) == False):
        settings_object.min_T_relax = std_values.min_T_relax
        warnings += "min_T_relax invalid, set to STD|"
    else:
        settings_object.min_T_relax=df.min_T_relax[ncase] #Minimum value for the temperature used for relaxation
    log_warning_hf = df.log_warning_hf[ncase] #Log warning for the heat flux
    if (pd.isna(log_warning_hf)):
        settings_object.log_warning_hf = std_values.log_warning_hf
        warnings += "log_warning_hf invalid, set to STD|"
    else:
        log_warning_hf = log_warning_hf.lower() #We convert the string to lower case
        match log_warning_hf:
            case "yes":
                settings_object.log_warning_hf = 1
            case "no":
                settings_object.log_warning_hf = 0
            case _:
                settings_object.log_warning_hf = std_values.log_warning_hf
                warnings += "log_warning_hf invalid, set to STD|"
    eta_max = df.eta_max[ncase] #Maximum value for the boundary layer eta
    if (is_valid_data(eta_max) == False):
        settings_object.eta_max = std_values.eta_max
        warnings += "eta_max invalid, set to STD|"
    else:
        settings_object.eta_max=df.eta_max[ncase] #Minimum value for the temperature used for relaxation
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
