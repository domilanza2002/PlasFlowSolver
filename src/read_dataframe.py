#.................................................
#   READ_DATAFRAME.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This project file is needed to read the
#   dataframe from the xlsx file
#.................................................
import pandas as pd #Library to read the xlsx file
import classes as classes_file #Module that contains the classes of the program
import bash_run as bash_run_file #Module to check if the bash.pfs file is present

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
    print("Please input the name of the excel file with the data:") #we ask the user to choose an input file
    input_file_name = input("Filename: ") 
    # we check if the extension is .xlsx, otherwise we throw an error
    if (input_file_name[-5:] != ".xlsx"): #if the extension is not .xlsx
        #We add the extension to the file name
        input_file_name = input_file_name+".xlsx"
    return input_file_name #we return the input filename

def read_dataframe(bash_run):
    """This function reads the dataframe from the xlsx file
    Inputs:
        bash_run: boolean, True if the bash.pfs file is present, False otherwise
    Returns:
        string: df_object, the dataframe from the xlsx file
        string: output_filename, the name of the output file
    """
    #.................................................
    #   This function reads the dataframe from the xlsx file
    #.................................................
    #   INPUTS:
    #   bash_run: boolean, True if the bash.pfs file is present, False otherwise
    #.................................................
    #   OUTPUTS:
    #   df:the dataframe from the xlsx file
    #   output_filename: the name of the output file
    #.................................................
    #Variables:
    input_filename = None #name of the input file
    df = None #the dataframe object read from the xlsx file
    df_inputs = None #the dataframe for the inputs
    df_cf=None #the dataframe for the conversion factors
    df_ic=None #the dataframe for the initial conditions
    df_probes=None #the dataframe for the probes settings
    df_settings=None #the dataframe for the settings
    file_found = None #variable to check if the file is found, boolean
    #Variables to be read from all sheet
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
    log_warning_hf = None #Log warning heat flux, string
    eta_max = None #Eta max, float
    #Variables to return
    df_object = classes_file.dataframe_xlsx_class() #I create the dataframe object to be returned
    output_filename = None #Name of the output file
    #I set the file_found variable to False
    file_found = False
    #I check if the bash.pfs file is present
    if (bash_run == True): #If the bash.pfs file is present
        input_filename = bash_run_file.retrieve_filename() #I retrieve the filename from the bash.pfs file
        try: #I try to read the file
            df = pd.read_excel(input_filename, engine="openpyxl",header=[0,1]) #I read the excel file
            file_found = True #If the file is found, we set the variable to True
        except:
            print("Error: the file in bash.pfs does not exist or is not an xlsx file")
            print("The program will continue in manual mode")
    #I ask for the input file
    while (file_found == False):
        input_filename = prompt_input_file() #I prompt the input file
        try: #I try to read the file
            df = pd.read_excel(input_filename, engine="openpyxl",header=[0,1]) #I read the excel file
            file_found = True #If the file is found, we set the variable to True
            continue
        except:
            print("Error: the file does not exist or is not an xlsx file")
            continue
    #I set the output filename
    output_filename = input_filename[:-5]+"_out.xlsx" #we set the output filename
    #Now I need to analyze the dataframe
    #Inputs:
    df_inputs=df["Inputs"]
    n = df_inputs.shape[0] #Number of the test
    #Comment:
    comment = df_inputs['Comment'] #Comment
    #Pressure:
    P = df_inputs['P [Pa]'] #Pressure
    #Dynamic pressure:
    Pdyn = df_inputs['Pdyn [Pa]'] #Dynamic pressure
    #Stagnation pressure:
    Pstag = df_inputs['Pstag [Pa]'] #Stagnation pressure
    #Heat flux:
    q = df_inputs['Heat flux [W/m^2]'] #Heat flux
    #Plasma gas:
    plasma_gas = df_inputs['Plasma gas'] #Plasma gas
    #Conversion factors:
    df_cf=df["Input conversion factors"]
    #Static pressure conversion factor:
    P_CF = df_cf['Pressure CF'] #Static pressure conversion factor
    #Dynamic pressure conversion factor:
    PD_CF = df_cf['Pdyn CF'] #Dynamic pressure conversion factor
    #Stagnation pressure conversion factor:
    PS_CF = df_cf['Pstag CF'] #Stagnation pressure conversion factor
    #Heat flux conversion factor:
    Q_CF = df_cf['Heat flux CF'] #Heat flux conversion factor
    #Initial conditions:
    df_ic=df["Initial conditions"]
    #Initial static temperature:
    T_0 = df_ic['T_0 [K]'] #Initial static temperature
    #Initial total temperature:
    Tt_0 = df_ic['Tt_0 [K]'] #Initial total temperature
    #Initial velocity:
    u_0 = df_ic['u_0 [m/s]'] #Initial velocity
    #Initial total pressure:
    Pt_0 = df_ic['Pt_0 [Pa]'] #Initial total pressure
    #Probes settings:
    df_probes=df["Probes settings"]
    #Wall temperature:
    Tw = df_probes['Wall T [K]'] #Wall temperature
    #Pitot external radius:
    Rp = df_probes['Rp [mm]'] #Pitot external radius
    #Flux probe external radius:
    Rm = df_probes['Rm [mm]'] #Flux probe external radius
    #Plasma jet radius:
    Rj = df_probes['Rj [mm]'] #Plasma jet radius
    #Stagnation type:
    stagtype = df_probes['StagPoint type'] #Stagnation type
    #Heat flux law:
    hflaw = df_probes['Heat flux law'] #Heat flux law
    #Barker correction:
    barker = df_probes['Barker correction'] #Barker correction
    #Settings:
    df_settings=df["Settings"]
    #Number of point for the boundary layer eta discretization:
    p = df_settings['BL points'] #Number of point for the boundary layer eta discretization
    #Maximum number of iterations for the heat flux:
    max_hf_iter = df_settings['Max hf iter'] #Maximum number of iterations for the heat flux
    #Convergence criteria for the heat flux:
    hf_conv = df_settings['Hf conv'] #Convergence criteria for the heat flux
    #Use previous iteration for the heat transfer:
    use_prev_ite = df_settings['Use prev hf iter'] #Use previous iteration for the heat transfer
    #Convergence criteria for the newton solver:
    newton_conv = df_settings['Newton conv'] #Convergence criteria for the newton solver
    #Maximum number of iterations for the newton solver:
    max_newton_iter = df_settings['Max Newton iter'] #Maximum number of iterations for the newton solver
    #Main newton jacobian finite difference epsilon:
    jac_diff = df_settings['Jac diff'] #Main newton jacobian finite difference epsilon
    #Maximum value for the temperature used for relaxation:
    max_T_relax = df_settings['Max T relax'] #Maximum value for the temperature used for relaxation
    #Minimum value for the temperature used for relaxation:
    min_T_relax = df_settings['Min T relax'] #Minimum value for the temperature used for relaxation
    #Log warning heat flux:
    log_warning_hf = df_settings['Log warning hf'] #Log warning heat flux
    #Eta max:
    eta_max = df_settings['Eta max'] #Eta max
    #I now save the variables in the dataframe object
    df_object.n = n #Number of the test, integer
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
    df_object.log_warning_hf = log_warning_hf #Log warning heat flux, string
    df_object.eta_max = eta_max #Eta max, float
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